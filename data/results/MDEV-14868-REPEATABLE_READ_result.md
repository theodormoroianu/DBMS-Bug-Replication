# Bug ID MDEV-14868-REPEATABLE_READ

## Description

Link:                     https://jira.mariadb.org/browse/MDEV-14868
Original isolation level: REPEATABLE READ
Tested isolation level:   REPEATABLE READ
Description:              Rollbacks make the server crash.


## Details
 * Database: mariadb-10.2.12-encrypted-logs
 * Number of scenarios: 1
 * Initial setup script: Yes

## Results
### Scenario 0
 * Instruction #0:
     - Instruction:  SET GLOBAL TRANSACTION ISOLATION LEVEL REPEATABLE READ;
     - Transaction: conn_0
     - Output: None
     - Executed order: 0
     - Affected rows / Warnings: 0 / 0
 * Instruction #1:
     - Instruction:  BEGIN;
     - Transaction: conn_0
     - Output: None
     - Executed order: 1
     - Affected rows / Warnings: 0 / 0
 * Instruction #2:
     - Instruction:  INSERT INTO t VALUES (REPEAT('a', 20000));
     - Transaction: conn_0
     - Output: None
     - Executed order: 2
     - Affected rows / Warnings: 1 / 0
 * Instruction #3:
     - Instruction:  SAVEPOINT sp;
     - Transaction: conn_0
     - Output: None
     - Executed order: 3
     - Affected rows / Warnings: 0 / 0
 * Instruction #4:
     - Instruction:  INSERT INTO t VALUES (REPEAT('a', 20000));
     - Transaction: conn_0
     - Output: None
     - Executed order: 4
     - Affected rows / Warnings: 1 / 0
 * Instruction #5:
     - Instruction:  ROLLBACK TO sp;
     - Transaction: conn_0
     - Output: None
     - Executed order: 5
     - Affected rows / Warnings: 0 / 0
 * Instruction #6:
     - Instruction:  COMMIT;
     - Transaction: conn_0
     - Output: ERROR: 2013 (HY000): Lost connection to MySQL server during query
     - Executed order: Not executed
     - Affected rows / Warnings: -1 / 0

 * Container logs:
   > mysqld: /server/server/sql/log.cc:7070: int MYSQL_BIN_LOG::write_cache(THD*, IO_CACHE*): Assertion `!writer.checksum_len || writer.remains == 0' failed.
   > 240719 15:18:39 [ERROR] mysqld got signal 6 ;
   > This could be because you hit a bug. It is also possible that this binary
   > or one of the libraries it was linked against is corrupt, improperly built,
   > or misconfigured. This error can also be caused by malfunctioning hardware.
   > To report this bug, see https://mariadb.com/kb/en/reporting-bugs
   > We will try our best to scrape up some info that will hopefully help
   > diagnose the problem, but since we have already crashed, 
   > something is definitely wrong and this may fail.
   > Server version: 10.2.12-MariaDB-debug-log
   > key_buffer_size=134217728
   > read_buffer_size=131072
   > max_used_connections=1
   > max_threads=153
   > thread_count=8
   > It is possible that mysqld could use up to 
   > key_buffer_size + (read_buffer_size + sort_buffer_size)*max_threads = 467348 K  bytes of memory
   > Hope that's ok; if not, decrease some variables in the equation.
   > Thread pointer: 0x62a000060270
   > Attempting backtrace. You can use the following information to find out
   > where mysqld died. If you see no messages after this, something went
   > terribly wrong...
   > stack_bottom = 0x7f8b273fecc0 thread_stack 0x49000
   > /usr/lib/x86_64-linux-gnu/libasan.so.2(+0x4a077)[0x7f8b41afa077]
   > /usr/local/mysql/bin/mysqld(my_print_stacktrace+0xab)[0x556c9ad76547]
   > /usr/local/mysql/bin/mysqld(handle_fatal_signal+0x8da)[0x556c99d62b36]
   > /lib/x86_64-linux-gnu/libpthread.so.0(+0x11390)[0x7f8b4058c390]
   > /lib/x86_64-linux-gnu/libc.so.6(gsignal+0x38)[0x7f8b3f945438]
   > /lib/x86_64-linux-gnu/libc.so.6(abort+0x16a)[0x7f8b3f94703a]
   > /lib/x86_64-linux-gnu/libc.so.6(+0x2dbe7)[0x7f8b3f93dbe7]
   > /lib/x86_64-linux-gnu/libc.so.6(+0x2dc92)[0x7f8b3f93dc92]
   > mysys/stacktrace.c:267(my_print_stacktrace)[0x556c99fdef2e]
   > sql/log.cc:7072(MYSQL_BIN_LOG::write_cache(THD*, st_io_cache*))[0x556c99fe4563]
   > sql/log.cc:7811(MYSQL_BIN_LOG::trx_group_commit_leader(MYSQL_BIN_LOG::group_commit_entry*))[0x556c99fe265d]
   > sql/log.cc:7612(MYSQL_BIN_LOG::write_transaction_to_binlog_events(MYSQL_BIN_LOG::group_commit_entry*))[0x556c99fe15b1]
   > sql/log.cc:7286(MYSQL_BIN_LOG::write_transaction_to_binlog(THD*, binlog_cache_mngr*, Log_event*, bool, bool, bool))[0x556c99fdfec4]
   > sql/log.cc:1740(binlog_flush_cache(THD*, binlog_cache_mngr*, Log_event*, bool, bool, bool))[0x556c99fc428b]
   > sql/log.cc:1848(binlog_commit_flush_xid_caches(THD*, binlog_cache_mngr*, bool, unsigned long long))[0x556c99fc4d56]
   > sql/log.cc:9573(MYSQL_BIN_LOG::log_and_order(THD*, unsigned long long, bool, bool, bool))[0x556c99fed1f0]
   > sql/handler.cc:1460(ha_commit_trans(THD*, bool))[0x556c99d6b7a0]
   > sql/transaction.cc:307(trans_commit(THD*))[0x556c99afd6d6]
   > /usr/local/mysql/bin/mysqld(_Z21mysql_execute_commandP3THD+0x10439)[0x556c997ca134]
   > sql/sql_parse.cc:5544(mysql_execute_command(THD*))[0x556c997d83dc]
   > sql/sql_parse.cc:1807(dispatch_command(enum_server_command, THD*, char*, unsigned int, bool, bool))[0x556c997b41fc]
   > sql/sql_parse.cc:1360(do_command(THD*))[0x556c997b13ab]
   > sql/sql_connect.cc:1335(do_handle_one_connection(CONNECT*))[0x556c99acd02a]
   > sql/sql_connect.cc:1242(handle_one_connection)[0x556c99acca32]
   > /lib/x86_64-linux-gnu/libpthread.so.0(+0x76ba)[0x7f8b405826ba]
   > /lib/x86_64-linux-gnu/libc.so.6(clone+0x6d)[0x7f8b3fa1751d]
   > Trying to get some variables.
   > Some pointers may be invalid and cause the dump to abort.
   > Query (0x62b000000288): COMMIT
   > Connection ID (thread ID): 11
   > Status: NOT_KILLED
   > Optimizer switch: index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,index_merge_sort_intersection=off,engine_condition_pushdown=off,index_condition_pushdown=on,derived_merge=on,derived_with_keys=on,firstmatch=on,loosescan=on,materialization=on,in_to_exists=on,semijoin=on,partial_match_rowid_merge=on,partial_match_table_scan=on,subquery_cache=on,mrr=off,mrr_cost_based=off,mrr_sort_keys=off,outer_join_with_cache=on,semijoin_with_cache=on,join_cache_incremental=on,join_cache_hashed=on,join_cache_bka=on,optimize_join_buffer_size=off,table_elimination=on,extended_keys=on,exists_to_in=on,orderby_uses_equalities=on,condition_pushdown_for_derived=on
   > The manual page at http://dev.mysql.com/doc/mysql/en/crashing.html contains
   > information that should help you find out what is causing the crash.
   > ASAN:SIGSEGV
   > =================================================================
   > ==1==ERROR: AddressSanitizer: SEGV on unknown address 0x000000000000 (pc 0x7f8b3f9471a6 bp 0x556c9b179700 sp 0x7f8b273fa690 T32)
   >     #0 0x7f8b3f9471a5 in abort (/lib/x86_64-linux-gnu/libc.so.6+0x371a5)
   >     #1 0x7f8b3f93dbe6  (/lib/x86_64-linux-gnu/libc.so.6+0x2dbe6)
   >     #2 0x7f8b3f93dc91 in __assert_fail (/lib/x86_64-linux-gnu/libc.so.6+0x2dc91)
   >     #3 0x556c99fdef2d in MYSQL_BIN_LOG::write_cache(THD*, st_io_cache*) /server/server/sql/log.cc:7070
   >     #4 0x556c99fe4562 in MYSQL_BIN_LOG::write_transaction_or_stmt(MYSQL_BIN_LOG::group_commit_entry*, unsigned long long) /server/server/sql/log.cc:8078
   >     #5 0x556c99fe265c in MYSQL_BIN_LOG::trx_group_commit_leader(MYSQL_BIN_LOG::group_commit_entry*) /server/server/sql/log.cc:7811
   >     #6 0x556c99fe15b0 in MYSQL_BIN_LOG::write_transaction_to_binlog_events(MYSQL_BIN_LOG::group_commit_entry*) /server/server/sql/log.cc:7612
   >     #7 0x556c99fdfec3 in MYSQL_BIN_LOG::write_transaction_to_binlog(THD*, binlog_cache_mngr*, Log_event*, bool, bool, bool) /server/server/sql/log.cc:7286
   >     #8 0x556c99fc428a in binlog_flush_cache /server/server/sql/log.cc:1740
   >     #9 0x556c99fc4d55 in binlog_commit_flush_xid_caches /server/server/sql/log.cc:1848
   >     #10 0x556c99fed1ef in MYSQL_BIN_LOG::log_and_order(THD*, unsigned long long, bool, bool, bool) /server/server/sql/log.cc:9573
   >     #11 0x556c99d6b79f in ha_commit_trans(THD*, bool) /server/server/sql/handler.cc:1460
   >     #12 0x556c99afd6d5 in trans_commit(THD*) /server/server/sql/transaction.cc:307
   >     #13 0x556c997ca133 in mysql_execute_command(THD*) /server/server/sql/sql_parse.cc:5544
   >     #14 0x556c997d83db in mysql_parse(THD*, char*, unsigned int, Parser_state*, bool, bool) /server/server/sql/sql_parse.cc:7900
   >     #15 0x556c997b41fb in dispatch_command(enum_server_command, THD*, char*, unsigned int, bool, bool) /server/server/sql/sql_parse.cc:1805
   >     #16 0x556c997b13aa in do_command(THD*) /server/server/sql/sql_parse.cc:1360
   >     #17 0x556c99acd029 in do_handle_one_connection(CONNECT*) /server/server/sql/sql_connect.cc:1335
   >     #18 0x556c99acca31 in handle_one_connection /server/server/sql/sql_connect.cc:1241
   >     #19 0x7f8b405826b9 in start_thread (/lib/x86_64-linux-gnu/libpthread.so.0+0x76b9)
   >     #20 0x7f8b3fa1751c in clone (/lib/x86_64-linux-gnu/libc.so.6+0x10751c)
   > AddressSanitizer can not provide additional info.
   > SUMMARY: AddressSanitizer: SEGV ??:0 abort
   > Thread T32 created by T0 here:
   >     #0 0x7f8b41ae6253 in pthread_create (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x36253)
   >     #1 0x556c9adbe156 in spawn_thread_noop /server/server/mysys/psi_noop.c:187
   >     #2 0x556c995c5d3f in inline_mysql_thread_create /server/server/include/mysql/psi/mysql_thread.h:1239
   >     #3 0x556c995da09f in create_thread_to_handle_connection(CONNECT*) /server/server/sql/mysqld.cc:6423
   >     #4 0x556c995da79f in create_new_thread /server/server/sql/mysqld.cc:6493
   >     #5 0x556c995db7dc in handle_connections_sockets() /server/server/sql/mysqld.cc:6768
   >     #6 0x556c995d95e2 in mysqld_main(int, char**) /server/server/sql/mysqld.cc:6042
   >     #7 0x556c995c42df in main /server/server/sql/main.cc:25
   >     #8 0x7f8b3f93083f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2083f)
   > ==1==ABORTING