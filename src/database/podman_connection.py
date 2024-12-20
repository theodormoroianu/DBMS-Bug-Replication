import subprocess, logging, time, atexit, os
import podman.client as client
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from podman.domain.containers import Container

from .config import DatabaseTypeAndVersion, DatabaseConnection
from . import helpers
from custom_exceptions import DatabaseVersionNotFoundError

WAIT_FOR_CONNECTION_TIMEOUT_S = 60


class RunningContainer:
    """
    A class that represents a running container.
    """

    def __init__(
        self,
        container: Container,
        db_and_version: DatabaseTypeAndVersion,
        db_connection: DatabaseConnection,
        custom_args: Optional[List[str]] = None,
    ):
        self.container = container
        self.db_and_version = db_and_version
        self.db_connection = db_connection
        self.custom_args = custom_args


class PodmanConnection:
    """
    Starts and stops the podman server, and provides the necessary context for the application.
    """

    _instance = None

    @staticmethod
    def free_resources():
        """
        Stops the podman server.
        """
        if PodmanConnection._instance is not None:
            del PodmanConnection._instance
            PodmanConnection._instance = None

    @staticmethod
    def get_instance():
        """
        Returns the singleton instance of the PodmanConnection.
        """
        if PodmanConnection._instance is None:
            PodmanConnection._instance = PodmanConnection()
        return PodmanConnection._instance

    def __init__(self):
        """
        This:
            1. Starts the podman service.
            2. Initializes the podman client.
        """
        # Start the server.
        logging.info("Starting the podman daemon...")
        self.podman_server_proc = subprocess.Popen(
            ["podman", "system", "service", "--time=0"]
        )

        # Start the client. It might take a few seconds for the server
        # to become reachable.
        logging.info("Connecting to the podman daemon...")
        self.podman_client = client.PodmanClient()
        time_before = time.time()
        while time.time() - time_before < 5:
            try:
                if not self.podman_client.ping():
                    raise ConnectionError()
                break
            except Exception:
                time.sleep(0.1)
                logging.info("Waiting for the podman daemon to start...")
        else:
            logging.error("Connection to the podman daemon failed.")
            print("Error connecting to the podman daemon.")
            print("Please make sure that podman is installed.")
            raise ConnectionError("Error connecting to the podman daemon.")

        # Mapping from containerID to container object
        self.containers: Dict[str, RunningContainer] = {}

        # Containers that are running but not currently used.
        # We check that the db is reachable before using it, to avoid
        # providing a crashed DB to the user.
        self.unused_containers: Dict[
            DatabaseTypeAndVersion, List[Tuple[Container, DatabaseConnection]]
        ] = defaultdict(list)

        # Map storing for each container the number of log lines to ignore (mostly the ones generated
        # by the database server starting up)
        self.log_characters_to_ignore: Dict[str, int] = defaultdict(int)

    def _get_image_and_tag(
        self, db_and_version: DatabaseTypeAndVersion
    ) -> Tuple[str, str]:
        """
        Get the image name and tag for a specific database type and version.
        If neccecary, the image is pulled from a registry.
        """

        local_image, local_tag = None, None

        # Try to run the image locally (if present).
        logging.info(f"Trying to find the image for {db_and_version} locally...")
        for image, tag in db_and_version.to_docker_hub_images_and_tags():
            try:
                self.podman_client.images.get(f"{image}:{tag}")
                local_image, local_tag = image, tag
                logging.info(f"Found image {image}:{tag} locally.")
                break
            except Exception:
                pass

        # Not present locally, we need to pull it.
        if local_image is None:
            logging.info(
                f"Image {db_and_version} not found locally. Trying to pull it..."
            )
            for image, tag in db_and_version.to_docker_hub_images_and_tags():
                try:
                    self.podman_client.images.pull(
                        repository=f"docker.io/{image}", tag=tag
                    )
                    self.podman_client.images.get(f"{image}:{tag}")
                    logging.info(f"Image {image}:{tag} pulled successfully.")
                    local_image, local_tag = image, tag
                    break
                except Exception:
                    pass

        # Still not present, we can't do anything.
        if local_image is None:
            logging.error(
                f"Image {db_and_version} not found. Maybe it needs to be built?"
            )
            raise DatabaseVersionNotFoundError(
                database_type=db_and_version.database_type.value,
                version=db_and_version.version,
            )

        return local_image, local_tag

    def create_container(
        self,
        db_and_version: DatabaseTypeAndVersion,
        create_fresh_container: bool,
        custom_args: Optional[List[str]] = None,
    ) -> Tuple[str, DatabaseConnection]:
        """
        Creates a container for the given database type and version.
        returns the container id and the database connection.

        :param db_and_version: The database type and version to create the container for.
        :param create_fresh_container: If a fresh container should be created (if false, an old container\
            can be re-used).
        """
        logging.debug(f"new container for {db_and_version} requested.")

        # Maybe we have a container that is not currently used.
        if (
            self.unused_containers[db_and_version]
            and not create_fresh_container
            and not custom_args
        ):
            logging.info(f"Re-using a container for {db_and_version}.")
            container, db_connection = self.unused_containers[db_and_version].pop()
            self.containers[container.id] = RunningContainer(
                container, db_and_version, db_connection, custom_args
            )
            return container.id, db_connection

        # Get the image and tag
        local_image, local_tag = self._get_image_and_tag(db_and_version)

        # Create the container
        host_port = helpers.get_free_port()
        container_port = db_and_version.database_type.used_port()

        # Environment variables for the container
        environment = {
            "MYSQL_ALLOW_EMPTY_PASSWORD": "yes",
            "MARIADB_ALLOW_EMPTY_ROOT_PASSWORD": "yes",
        }

        try:
            container = self.podman_client.containers.create(
                image=f"{local_image}:{local_tag}",
                ports={f"{container_port}/tcp": host_port},
                environment=environment,
                auto_remove=False,
                command=custom_args,
                # This seems to not be required. Adding a network_mode="bridge" will make the container
                # think it's running in a different network, and it will make mysql servers unreachable.
                # network_mode="bridge",
            )
        except Exception as e:
            logging.info(
                "Unable to create the container. Maybe the image is not built?"
            )
            # Log the error and raise a new one
            logging.error(e)
            print(
                f"Unable to create the container. Image {local_image}:{local_tag} cannot be started."
            )
            raise e

        container.start()
        logging.info(f"Container {container.id} started on port {host_port}")

        db_connection = DatabaseConnection(
            db_and_version, host="127.0.0.1", port=host_port, user="root"
        )

        # Save the container in our list of running containers
        self.containers[container.id] = RunningContainer(
            container, db_and_version, db_connection, custom_args
        )

        # make sure that the DB is reachable
        time_before = time.time()
        logging.info("Waiting for the database server to start...")
        while time.time() - time_before < WAIT_FOR_CONNECTION_TIMEOUT_S:
            try:
                db_connection.to_connection().ping()
                break
            except Exception as e:
                time.sleep(0.1)
        else:
            logging.error("Connection to the database server failed.")
            print("Error connecting to the database server.")
            print("Please make sure that the database server is running:")
            print(
                f"Image used: {local_image}:{local_tag} (container id: {container.id})"
            )
            input("Press Enter to continue...")
            raise ConnectionError("Error connecting to the database server.")
        logging.info("Database server started.")

        # Mark the log lines to ignore
        self.log_characters_to_ignore[container.id] = len(self.get_logs(container.id))

        return container.id, db_connection

    def get_logs(self, container_id: str) -> str:
        """
        Get the logs of the container. If some lines are marked to
        be skipped (see `log_lines_to_ignore`), they are skipped.
        """
        running_container = self.containers[container_id]
        logs = running_container.container.logs(stdout=True, stderr=True)
        logs_dump = (
            logs.decode() if isinstance(type(logs), bytes) else b"".join(logs).decode()
        )
        return logs_dump[self.log_characters_to_ignore[container_id] :]

    def stop_container(self, container_id: str, try_reuse: bool = True):
        """
        Stops the container with the given id.
        If `try_reuse` is True, the container is tested to check if it can be re-used.

        :param container_id: The id of the container to stop.
        :param try_reuse: If the container should be tested for re-use.
        """
        running_container = self.containers[container_id]
        logging.debug(
            f"Stopping container {container_id} of type {running_container.db_and_version} (try-reuse = {try_reuse})..."
        )
        try:
            # If we can't reuse it, throw an exception.
            if not try_reuse or running_container.custom_args is not None:
                raise ValueError("Container can't be re-used (imposed by testcase).")

            # Try to re-use container
            # Make a few SQL queries to check if the DB is still alive
            conn = running_container.db_connection.to_connection()
            conn.ping()
            cursor = conn.cursor()
            cursor.execute("drop database if exists testdb;")
            cursor.execute("create database testdb;")
            cursor.execute("create table testdb.testtable (a int);")
            cursor.execute("insert into testdb.testtable values (1);")
            cursor.execute("drop table testdb.testtable;")

            self.unused_containers[running_container.db_and_version].append(
                (running_container.container, running_container.db_connection)
            )
            self.log_characters_to_ignore[container_id] += len(
                self.get_logs(container_id)
            )
            logging.debug(f"Recycling container {container_id}.")
            del self.containers[container_id]
        except Exception as e:
            logging.debug(f"Error re-using container {container_id}: {e}")
            # Can't re-use container. Try to stop it.
            try:
                running_container.container.stop(timeout=0)
                running_container.container.remove(v=True)
            except Exception:
                try:
                    running_container.container.remove(v=True)
                except Exception:
                    # The container cannot be deleted, most probably because
                    # it has already been deleted. Silently ignore the error.
                    logging.info(
                        f"Skipping deletion of container {container_id} because of failure..."
                    )
            del self.containers[container_id]
            del self.log_characters_to_ignore[container_id]

    # run when the object is deleted
    def __del__(self):
        """
        Stops the podman server.
        """
        logging.info("Cleaning containers...")
        containers_ids = []
        for _, running_container in self.containers.items():
            containers_ids.append(running_container.container.id)
        for _, l in self.unused_containers.items():
            for container, _ in l:
                containers_ids.append(container.id)
        for container_id in containers_ids:
            os.system(f"podman kill {container_id} > /dev/null")
            os.system(f"podman rm {container_id} > /dev/null")

        self.podman_server_proc.kill()


atexit.register(PodmanConnection.free_resources)
