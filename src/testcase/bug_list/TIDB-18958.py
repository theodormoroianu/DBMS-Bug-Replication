import context
import testcase.bug as bug
import database.config as db_config
from testcase.helpers import DEFAULT_ISOLATION_LEVEL, IsolationLevel

ORIGINAL_ISOLATION_LEVEL = DEFAULT_ISOLATION_LEVEL
BUG_ID = "TIDB-18958"
LINK = "https://github.com/pingcap/tidb/issues/18958"
DB_AND_VERSION = db_config.DatabaseTypeAndVersion(
    db_config.DatabaseType.TIDB, "v4.0.4.tikv"
)

DESCRIPTION = """Duplicate key is ignored in insert The insert statement should fail."""

SETUP_SQL_SCRIPT = """
create table t (
    c_int       int auto_increment,
    c_double    double,
    c_decimal   decimal(12, 6),
    c_string    varchar(40) collate utf8_general_ci,
    c_datetime  datetime,
    c_timestamp timestamp,
    c_enum      enum ('a', 'b', 'c', 'd', 'e'),
    c_set       set ('1', '2', '3', '4', '5'),
    c_json      json,
    primary key (c_int),
    unique key (c_string),
    key (c_enum),
    key (c_set),
    key (c_timestamp),
    key (c_datetime),
    key (c_decimal)
);
insert into t (`c_int`, `c_double`, `c_decimal`, `c_string`, `c_datetime`, `c_timestamp`, `c_enum`, `c_set`, `c_json`) values
  (1, 0.718657, 91.150000, 'red curtain', '2020-01-02 02:00:00', '2020-01-03 21:11:41', 'd', '1', '{\"datetime\": \"2019-12-27 05:00:00\", \"enum\": \"a\", \"int\": 20, \"set\": \"1,2,3\", \"str\": \"ivory crest\"}')
, (2, 0.070684, 74.820000, 'gold sloth', '2019-12-26 03:00:00', '2019-12-26 18:02:54', 'e', '2', '{\"datetime\": \"2020-01-04 02:00:00\", \"enum\": \"a\", \"int\": 16, \"set\": \"5\", \"str\": \"cream spider\"}')
, (3, 0.490952, 85.290000, 'blue roach', '2020-01-03 14:00:00', '2019-12-25 03:47:00', 'd', '1,4', '{\"datetime\": \"2020-01-04 12:00:00\", \"enum\": \"c\", \"int\": 18, \"set\": \"2\", \"str\": \"light seer\"}')
, (4, 0.427215, 55.340000, 'cerulean ant', '2020-01-03 18:00:00', '2019-12-29 17:11:56', 'a', '1,2,5', '{\"datetime\": \"2019-12-25 21:00:00\", \"enum\": \"d\", \"int\": 11, \"set\": \"4,5\", \"str\": \"orange cat\"}')
, (5, 0.88423, 80.510000, 'black seer', '2020-01-07 06:00:00', '2020-01-06 09:41:17', 'e', '1,3', '{\"datetime\": \"2020-01-04 04:00:00\", \"enum\": \"c\", \"int\": 8, \"set\": \"4,5\", \"str\": \"light bard\"}')
, (6, 0.263039, 6.790000, 'orange crest', '2020-01-04 12:00:00', '2019-12-27 05:27:06', 'e', '1,4', '{\"datetime\": \"2020-01-03 20:00:00\", \"enum\": \"b\", \"int\": 3, \"set\": \"2,5\", \"str\": \"gray warrior\"}')
, (7, 0.444086, 47.430000, 'cyan bard', '2020-01-06 06:00:00', '2020-01-04 04:39:49', 'd', '5', '{\"datetime\": \"2020-01-03 06:00:00\", \"enum\": \"e\", \"int\": 16, \"set\": \"1,4\", \"str\": \"light fly\"}')
, (8, 0.709668, 94.560000, 'yellow speaker', '2020-01-04 04:00:00', '2020-01-02 19:24:03', 'd', '2,3,4,5', '{\"datetime\": \"2019-12-30 13:00:00\", \"enum\": \"e\", \"int\": 4, \"set\": \"1,2,3\", \"str\": \"green vulture\"}')
, (9, 0.899852, 80.660000, 'pink warrior', '2020-01-04 16:00:00', '2020-01-02 15:02:03', 'd', '1,3,5', '{\"datetime\": \"2019-12-27 13:00:00\", \"enum\": \"e\", \"int\": 14, \"set\": \"1,4,5\", \"str\": \"dark kangaroo\"}')
, (10, 0.277686, 24.880000, 'black cat', '2020-01-06 14:00:00', '2020-01-06 03:57:43', 'd', '1,3', '{\"datetime\": \"2020-01-06 10:00:00\", \"enum\": \"c\", \"int\": 6, \"set\": \"2\", \"str\": \"gray carpet\"}')
, (11, 0.365868, 97.450000, 'azure bard', '2019-12-29 03:00:00', '2019-12-31 09:48:56', 'a', '4,5', '{\"datetime\": \"2019-12-25 19:00:00\", \"enum\": \"c\", \"int\": 3, \"set\": \"1,2,4,5\", \"str\": \"white singer\"}')
, (12, 0.136982, 14.990000, 'green seer', '2019-12-29 07:00:00', '2019-12-25 03:56:42', 'c', '1,3,4', '{\"datetime\": \"2019-12-27 05:00:00\", \"enum\": \"d\", \"int\": 6, \"set\": \"4\", \"str\": \"navy witch\"}')
, (13, 0.716163, 85.410000, 'gray scourge', '2020-01-03 06:00:00', '2019-12-29 17:30:24', 'e', '3,5', '{\"datetime\": \"2019-12-29 21:00:00\", \"enum\": \"b\", \"int\": 18, \"set\": \"1,2,3,4\", \"str\": \"silver sloth\"}')
, (14, 0.319057, 73.440000, 'dark fly', '2020-01-06 04:00:00', '2020-01-05 02:16:03', 'b', '3,4,5', '{\"datetime\": \"2019-12-26 05:00:00\", \"enum\": \"e\", \"int\": 2, \"set\": \"1,2,3,4\", \"str\": \"ivory fly\"}')
, (15, 0.45908, 77.550000, 'silver vulture', '2019-12-29 09:00:00', '2019-12-30 16:06:20', 'd', '3', '{\"datetime\": \"2019-12-31 07:00:00\", \"enum\": \"a\", \"int\": 20, \"set\": \"2,3,4\", \"str\": \"dark sloth\"}')
, (16, 0.846275, 6.020000, 'red kangaroo', '2019-12-30 03:00:00', '2020-01-02 15:00:37', 'a', '3,5', '{\"datetime\": \"2020-01-05 20:00:00\", \"enum\": \"b\", \"int\": 6, \"set\": \"1,5\", \"str\": \"white vulture\"}')
, (20, 0.939371, 47.980000, 'gray mistress', '2020-01-07 02:00:00', '2019-12-28 12:00:28', 'd', '1', '{\"datetime\": \"2020-01-05 02:00:00\", \"enum\": \"b\", \"int\": 6, \"set\": \"2,4\", \"str\": \"cerulean curtain\"}')
;
"""


def get_scenarios(isolation_level: IsolationLevel):
    return [
        f"""
        conn_0> SET GLOBAL TRANSACTION ISOLATION LEVEL {isolation_level.value};
        conn_0> begin;
        conn_0> update t set c_string = 'gray mistress' where c_int = 10;
        conn_0> insert into t values (10, 0.133544, 0.39, 'cyan fly', '2020-01-05 20:00:00', '2020-01-02 14:21:55', 'c', '1,2,5', '{{"int":18,"str":"cyan trader","datetime":"2020-01-07 08:00:00","enum":"b","set":"2,3"}}');
        conn_0> commit;
        conn_0> select * from t where c_int = 10;
        """,
        """
        conn_0> update t set c_string = 'gray mistress' where c_int = 10;
        conn_0> insert into t values (10, 0.133544, 0.39, 'cyan fly', '2020-01-05 20:00:00', '2020-01-02 14:21:55', 'c', '1,2,5', '{{"int":18,"str":"cyan trader","datetime":"2020-01-07 08:00:00","enum":"b","set":"2,3"}}');
        conn_0> select * from t where c_int = 10;
        """,
    ]
