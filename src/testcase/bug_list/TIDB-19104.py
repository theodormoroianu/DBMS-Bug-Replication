import context
import testcase.bug as bug
import database.config as db_config
from testcase.helpers import DEFAULT_ISOLATION_LEVEL, IsolationLevel

ORIGINAL_ISOLATION_LEVEL = DEFAULT_ISOLATION_LEVEL
BUG_ID = "TIDB-19104"
LINK = "https://github.com/pingcap/tidb/issues/19104"
# Commit 7cac557b024f0aaca6825193477e5e6daea7055b
DB_AND_VERSION = db_config.DatabaseTypeAndVersion(
    db_config.DatabaseType.TIDB, "7cac557b.tikv"
)

DESCRIPTION = """Duplicate key is ignored in insert The insert statement should fail."""

SETUP_SQL_SCRIPT = """
create table t ( c_int int, c_str varchar(40), c_datetime datetime, c_timestamp timestamp, c_double double, c_decimal decimal(12, 6) , primary key(c_int, c_str) , unique key(c_int) , unique key(c_str) , unique key(c_decimal) , unique key(c_datetime) , key(c_timestamp) );
insert into t values (1, 'zen ardinghelli', '2020-02-03 18:15:17', '2020-03-11 05:47:11', 36.226534, 3.763), (2, 'suspicious joliot', '2020-01-01 22:56:37', '2020-04-07 06:19:07', 62.756537, 5.567), (3, 'keen zhukovsky', '2020-01-21 04:09:20', '2020-06-06 08:32:14', 33.115065, 1.381), (4, 'crazy newton', '2020-02-14 21:37:56', '2020-04-28 08:33:48', 44.146318, 4.249), (5, 'happy black', '2020-03-12 16:04:14', '2020-01-18 09:17:37', 41.962653, 5.959);
insert into t values (6, 'vigilant swartz', '2020-06-01 07:37:44', '2020-05-25 01:26:43', 56.352233, 2.202), (7, 'suspicious germain', '2020-04-16 23:25:23', '2020-03-17 05:06:57', 55.897698, 3.460), (8, 'festive chandrasekhar', '2020-02-11 23:40:29', '2020-04-08 10:13:04', 77.565691, 0.540), (9, 'vigorous meninsky', '2020-02-17 10:03:17', '2020-01-02 15:02:02', 6.484815, 6.292), (10, 'heuristic moser', '2020-04-20 12:18:49', '2020-06-20 20:20:18', 28.023822, 2.765);
insert into t values (11, 'sharp carver', '2020-03-01 11:23:41', '2020-03-23 17:59:05', 40.842442, 6.345), (12, 'trusting noether', '2020-03-28 06:42:34', '2020-01-27 15:33:40', 49.544658, 4.811), (13, 'objective ishizaka', '2020-01-28 17:30:55', '2020-04-02 17:45:39', 59.523930, 5.015), (14, 'sad rhodes', '2020-03-30 21:43:37', '2020-06-09 06:53:53', 87.295753, 2.413), (15, 'wonderful shockley', '2020-04-29 09:17:11', '2020-03-14 04:36:51', 6.778588, 8.497);
"""


def get_scenarios(isolation_level: IsolationLevel):
    return [
        f"""
        conn_0> SET GLOBAL TRANSACTION ISOLATION LEVEL {isolation_level.value};
        conn_0> begin;
        conn_0> insert into t values (13, 'vibrant yalow', '2020-05-15 06:59:05', '2020-05-03 05:58:45', 43.721929, 8.066), (14, 'xenodochial spence', '2020-02-13 17:28:07', '2020-04-01 12:18:30', 19.981331, 5.774), (22, 'eloquent neumann', '2020-02-10 16:00:20', '2020-03-28 00:24:42', 10.702532, 7.618) on duplicate key update c_int=values(c_int), c_str=values(c_str), c_double=values(c_double), c_timestamp=values(c_timestamp);
        conn_0> select sum((select t1.c_str from t t1 where t1.c_int = 11 and t1.c_str > t.c_str order by t1.c_decimal limit 1) is null) nulls from t order by c_str;
        conn_0> commit;
        conn_0> select sum((select t1.c_str from t t1 where t1.c_int = 11 and t1.c_str > t.c_str order by t1.c_decimal limit 1) is null) nulls from t order by c_str;
        """
    ]
