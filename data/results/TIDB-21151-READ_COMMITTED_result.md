# Bug ID TIDB-21151-READ_COMMITTED

## Description

Link:                     https://github.com/pingcap/tidb/issues/21151
Original isolation level: REPEATABLE READ
Tested isolation level:   READ COMMITTED
Description:              Gets warnings when running in a transaction.


## Details
 * Database: tidb-v4.0.8.tikv
 * Number of scenarios: 1
 * Initial setup script: Yes

## Results
### Scenario 0
 * Instruction #0:
     - Instruction:  SET GLOBAL TRANSACTION ISOLATION LEVEL repeatable read;
     - Transaction: conn_0
     - Output: None
     - Executed order: 0
     - Affected rows / Warnings: 0 / 0
 * Instruction #1:
     - Instruction:  SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
     - Transaction: conn_0
     - Output: None
     - Executed order: 1
     - Affected rows / Warnings: 0 / 0
 * Instruction #2:
     - Instruction:  BEGIN;
     - Transaction: conn_0
     - Output: None
     - Executed order: 2
     - Affected rows / Warnings: 0 / 0
 * Instruction #3:
     - Instruction:  select /*+ NO_INDEX_MERGE() */ * from t where a > 3 or b > 3;
     - Transaction: conn_0
     - Output: [(2, 10, 4, 4)]
     - Executed order: 3
     - Affected rows / Warnings: 1 / 0
 * Instruction #4:
     - Instruction:  select /*+ USE_INDEX_MERGE(t, ia, ib) */ * from t where a > 3 or b > 3;
     - Transaction: conn_0
     - Output: [(2, 10, 4, 4)]
     - Executed order: 4
     - Affected rows / Warnings: 1 / 0
 * Instruction #5:
     - Instruction:  BEGIN;
     - Transaction: conn_1
     - Output: None
     - Executed order: 5
     - Affected rows / Warnings: 0 / 0
 * Instruction #6:
     - Instruction:  update t set value = 11 where id = 2;
     - Transaction: conn_1
     - Output: None
     - Executed order: 6
     - Affected rows / Warnings: 1 / 0
 * Instruction #7:
     - Instruction:  COMMIT;
     - Transaction: conn_1
     - Output: None
     - Executed order: 7
     - Affected rows / Warnings: 0 / 0
 * Instruction #8:
     - Instruction:  select /*+ NO_INDEX_MERGE() */ * from t where a > 3 or b > 3;
     - Transaction: conn_0
     - Output: [(2, 11, 4, 4)]
     - Executed order: 8
     - Affected rows / Warnings: 1 / 0
 * Instruction #9:
     - Instruction:  select /*+ USE_INDEX_MERGE(t, ia, ib) */ * from t where a > 3 or b > 3;
     - Transaction: conn_0
     - Output: [(2, 10, 4, 4)]
     - Executed order: 9
     - Affected rows / Warnings: 1 / 0
 * Instruction #10:
     - Instruction:  COMMIT;
     - Transaction: conn_0
     - Output: None
     - Executed order: 10
     - Affected rows / Warnings: 0 / 0

 * Container logs:
   > [2024/07/12 09:26:15.922 +00:00] [INFO] [session.go:2161] ["CRUCIAL OPERATION"] [conn=7] [schemaVersion=32] [cur_db=] [sql="drop database if exists testdb;"] [user=root@10.88.0.6]
   > [2024/07/12 09:26:15.933 +00:00] [INFO] [ddl_worker.go:261] ["[ddl] add DDL jobs"] ["batch count"=1] [jobs="ID:55, Type:drop schema, State:none, SchemaState:none, SchemaID:50, TableID:0, RowCount:0, ArgLen:0, start time: 2024-07-12 09:26:15.9 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0; "]
   > [2024/07/12 09:26:15.933 +00:00] [INFO] [ddl.go:487] ["[ddl] start DDL job"] [job="ID:55, Type:drop schema, State:none, SchemaState:none, SchemaID:50, TableID:0, RowCount:0, ArgLen:0, start time: 2024-07-12 09:26:15.9 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"] [query="drop database if exists testdb;"]
   > [2024/07/12 09:26:15.937 +00:00] [INFO] [ddl_worker.go:588] ["[ddl] run DDL job"] [worker="worker 3, tp general"] [job="ID:55, Type:drop schema, State:none, SchemaState:none, SchemaID:50, TableID:0, RowCount:0, ArgLen:0, start time: 2024-07-12 09:26:15.9 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"]
   > [2024/07/12 09:26:15.954 +00:00] [INFO] [domain.go:127] ["diff load InfoSchema success"] [usedSchemaVersion=32] [neededSchemaVersion=33] ["start time"=700.511µs] [phyTblIDs="[]"] [actionTypes="[]"]
   > [2024/07/12 09:26:16.003 +00:00] [INFO] [ddl_worker.go:777] ["[ddl] wait latest schema version changed"] [worker="worker 3, tp general"] [ver=33] ["take time"=52.750878ms] [job="ID:55, Type:drop schema, State:running, SchemaState:write only, SchemaID:50, TableID:0, RowCount:0, ArgLen:0, start time: 2024-07-12 09:26:15.9 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"]
   > [2024/07/12 09:26:16.005 +00:00] [INFO] [ddl_worker.go:588] ["[ddl] run DDL job"] [worker="worker 3, tp general"] [job="ID:55, Type:drop schema, State:running, SchemaState:write only, SchemaID:50, TableID:0, RowCount:0, ArgLen:0, start time: 2024-07-12 09:26:15.9 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"]
   > [2024/07/12 09:26:16.020 +00:00] [INFO] [domain.go:127] ["diff load InfoSchema success"] [usedSchemaVersion=33] [neededSchemaVersion=34] ["start time"=689.197µs] [phyTblIDs="[]"] [actionTypes="[]"]
   > [2024/07/12 09:26:16.069 +00:00] [INFO] [ddl_worker.go:777] ["[ddl] wait latest schema version changed"] [worker="worker 3, tp general"] [ver=34] ["take time"=52.514952ms] [job="ID:55, Type:drop schema, State:running, SchemaState:delete only, SchemaID:50, TableID:0, RowCount:0, ArgLen:0, start time: 2024-07-12 09:26:15.9 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"]
   > [2024/07/12 09:26:16.071 +00:00] [INFO] [ddl_worker.go:588] ["[ddl] run DDL job"] [worker="worker 3, tp general"] [job="ID:55, Type:drop schema, State:running, SchemaState:delete only, SchemaID:50, TableID:0, RowCount:0, ArgLen:0, start time: 2024-07-12 09:26:15.9 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"]
   > [2024/07/12 09:26:16.089 +00:00] [INFO] [domain.go:127] ["diff load InfoSchema success"] [usedSchemaVersion=34] [neededSchemaVersion=35] ["start time"=742.626µs] [phyTblIDs="[]"] [actionTypes="[]"]
   > [2024/07/12 09:26:16.139 +00:00] [INFO] [ddl_worker.go:777] ["[ddl] wait latest schema version changed"] [worker="worker 3, tp general"] [ver=35] ["take time"=53.04079ms] [job="ID:55, Type:drop schema, State:done, SchemaState:none, SchemaID:50, TableID:0, RowCount:0, ArgLen:0, start time: 2024-07-12 09:26:15.9 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"]
   > [2024/07/12 09:26:16.142 +00:00] [INFO] [delete_range.go:105] ["[ddl] add job into delete-range table"] [jobID=55] [jobType="drop schema"]
   > [2024/07/12 09:26:16.143 +00:00] [INFO] [ddl_worker.go:367] ["[ddl] finish DDL job"] [worker="worker 3, tp general"] [job="ID:55, Type:drop schema, State:synced, SchemaState:none, SchemaID:50, TableID:0, RowCount:0, ArgLen:0, start time: 2024-07-12 09:26:15.9 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"]
   > [2024/07/12 09:26:16.154 +00:00] [INFO] [ddl.go:519] ["[ddl] DDL job is finished"] [jobID=55]
   > [2024/07/12 09:26:16.154 +00:00] [INFO] [domain.go:632] ["performing DDL change, must reload"]
   > [2024/07/12 09:26:16.157 +00:00] [INFO] [session.go:2161] ["CRUCIAL OPERATION"] [conn=7] [schemaVersion=35] [cur_db=] [sql="create database testdb;"] [user=root@10.88.0.6]
   > [2024/07/12 09:26:16.177 +00:00] [INFO] [ddl_worker.go:261] ["[ddl] add DDL jobs"] ["batch count"=1] [jobs="ID:57, Type:create schema, State:none, SchemaState:none, SchemaID:56, TableID:0, RowCount:0, ArgLen:1, start time: 2024-07-12 09:26:16.15 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0; "]
   > [2024/07/12 09:26:16.177 +00:00] [INFO] [ddl.go:487] ["[ddl] start DDL job"] [job="ID:57, Type:create schema, State:none, SchemaState:none, SchemaID:56, TableID:0, RowCount:0, ArgLen:1, start time: 2024-07-12 09:26:16.15 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"] [query="create database testdb;"]
   > [2024/07/12 09:26:16.181 +00:00] [INFO] [ddl_worker.go:588] ["[ddl] run DDL job"] [worker="worker 3, tp general"] [job="ID:57, Type:create schema, State:none, SchemaState:none, SchemaID:56, TableID:0, RowCount:0, ArgLen:0, start time: 2024-07-12 09:26:16.15 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"]
   > [2024/07/12 09:26:16.195 +00:00] [INFO] [domain.go:127] ["diff load InfoSchema success"] [usedSchemaVersion=35] [neededSchemaVersion=36] ["start time"=1.102241ms] [phyTblIDs="[]"] [actionTypes="[]"]
   > [2024/07/12 09:26:16.245 +00:00] [INFO] [ddl_worker.go:777] ["[ddl] wait latest schema version changed"] [worker="worker 3, tp general"] [ver=36] ["take time"=52.876103ms] [job="ID:57, Type:create schema, State:done, SchemaState:public, SchemaID:56, TableID:0, RowCount:0, ArgLen:1, start time: 2024-07-12 09:26:16.15 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"]
   > [2024/07/12 09:26:16.248 +00:00] [INFO] [ddl_worker.go:367] ["[ddl] finish DDL job"] [worker="worker 3, tp general"] [job="ID:57, Type:create schema, State:synced, SchemaState:public, SchemaID:56, TableID:0, RowCount:0, ArgLen:0, start time: 2024-07-12 09:26:16.15 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"]
   > [2024/07/12 09:26:16.259 +00:00] [INFO] [ddl.go:519] ["[ddl] DDL job is finished"] [jobID=57]
   > [2024/07/12 09:26:16.259 +00:00] [INFO] [domain.go:632] ["performing DDL change, must reload"]
   > [2024/07/12 09:26:16.262 +00:00] [INFO] [session.go:2161] ["CRUCIAL OPERATION"] [conn=7] [schemaVersion=36] [cur_db=testdb] [sql="create table t (id int primary key, value int, a int not null, b int not null,\n    index ia (a),  index ib (b));"] [user=root@10.88.0.6]
   > [2024/07/12 09:26:16.280 +00:00] [INFO] [ddl_worker.go:261] ["[ddl] add DDL jobs"] ["batch count"=1] [jobs="ID:59, Type:create table, State:none, SchemaState:none, SchemaID:56, TableID:58, RowCount:0, ArgLen:1, start time: 2024-07-12 09:26:16.25 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0; "]
   > [2024/07/12 09:26:16.280 +00:00] [INFO] [ddl.go:487] ["[ddl] start DDL job"] [job="ID:59, Type:create table, State:none, SchemaState:none, SchemaID:56, TableID:58, RowCount:0, ArgLen:1, start time: 2024-07-12 09:26:16.25 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"] [query="create table t (id int primary key, value int, a int not null, b int not null,\n    index ia (a),  index ib (b));"]
   > [2024/07/12 09:26:16.285 +00:00] [INFO] [ddl_worker.go:588] ["[ddl] run DDL job"] [worker="worker 3, tp general"] [job="ID:59, Type:create table, State:none, SchemaState:none, SchemaID:56, TableID:58, RowCount:0, ArgLen:0, start time: 2024-07-12 09:26:16.25 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"]
   > [2024/07/12 09:26:16.302 +00:00] [INFO] [domain.go:127] ["diff load InfoSchema success"] [usedSchemaVersion=36] [neededSchemaVersion=37] ["start time"=2.212233ms] [phyTblIDs="[58]"] [actionTypes="[8]"]
   > [2024/07/12 09:26:16.351 +00:00] [INFO] [ddl_worker.go:777] ["[ddl] wait latest schema version changed"] [worker="worker 3, tp general"] [ver=37] ["take time"=52.883646ms] [job="ID:59, Type:create table, State:done, SchemaState:public, SchemaID:56, TableID:58, RowCount:0, ArgLen:1, start time: 2024-07-12 09:26:16.25 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"]
   > [2024/07/12 09:26:16.355 +00:00] [INFO] [ddl_worker.go:367] ["[ddl] finish DDL job"] [worker="worker 3, tp general"] [job="ID:59, Type:create table, State:synced, SchemaState:public, SchemaID:56, TableID:58, RowCount:0, ArgLen:0, start time: 2024-07-12 09:26:16.25 +0000 UTC, Err:<nil>, ErrCount:0, SnapshotVersion:0"]
   > [2024/07/12 09:26:16.366 +00:00] [INFO] [ddl.go:519] ["[ddl] DDL job is finished"] [jobID=59]
   > [2024/07/12 09:26:16.369 +00:00] [INFO] [domain.go:632] ["performing DDL change, must reload"]
   > [2024/07/12 09:26:16.369 +00:00] [INFO] [split_region.go:60] ["split batch regions request"] ["split key count"=1] ["batch count"=1] ["first batch, region ID"=2] ["first split key"=74800000000000003a]
   > [2024/07/12 09:26:16.369 +00:00] [INFO] [peer.rs:469] ["on split"] [split_keys="key 7480000000000000FF3A00000000000000F8"] [peer_id=3] [region_id=2]
   > [2024/07/12 09:26:16.370 +00:00] [INFO] [cluster_worker.go:125] ["alloc ids for region split"] [region-id=48] [peer-ids="[49]"]
   > [2024/07/12 09:26:16.370 +00:00] [INFO] [pd.rs:507] ["try to batch split region"] [task=batch_split] [region="id: 2 start_key: 7480000000000000FF3400000000000000F8 region_epoch { conf_ver: 1 version: 23 } peers { id: 3 store_id: 1 }"] [new_region_ids="[new_region_id: 48 new_peer_ids: 49]"] [region_id=2]
   > [2024/07/12 09:26:16.373 +00:00] [INFO] [apply.rs:1172] ["execute admin command"] [command="cmd_type: BatchSplit splits { requests { split_key: 7480000000000000FF3A00000000000000F8 new_region_id: 48 new_peer_ids: 49 } right_derive: true }"] [index=66] [term=6] [peer_id=3] [region_id=2]
   > [2024/07/12 09:26:16.373 +00:00] [INFO] [apply.rs:1752] ["split region"] [keys="key 7480000000000000FF3A00000000000000F8"] [region="id: 2 start_key: 7480000000000000FF3400000000000000F8 region_epoch { conf_ver: 1 version: 23 } peers { id: 3 store_id: 1 }"] [peer_id=3] [region_id=2]
   > [2024/07/12 09:26:16.375 +00:00] [INFO] [peer.rs:1758] ["notify pd with split"] [split_count=2] [peer_id=3] [region_id=2]
   > [2024/07/12 09:26:16.375 +00:00] [INFO] [peer.rs:1800] ["insert new region"] [region="id: 48 start_key: 7480000000000000FF3400000000000000F8 end_key: 7480000000000000FF3A00000000000000F8 region_epoch { conf_ver: 1 version: 24 } peers { id: 49 store_id: 1 }"] [region_id=48]
   > [2024/07/12 09:26:16.375 +00:00] [INFO] [peer.rs:159] ["create peer"] [peer_id=49] [region_id=48]
   > [2024/07/12 09:26:16.376 +00:00] [INFO] [raft.rs:783] ["became follower at term 5"] [term=5] [raft_id=49] [region_id=48]
   > [2024/07/12 09:26:16.376 +00:00] [INFO] [split_region.go:157] ["batch split regions complete"] ["batch region ID"=2] ["first at"=74800000000000003a] ["first new region left"="{Id:48 StartKey:7480000000000000ff3400000000000000f8 EndKey:7480000000000000ff3a00000000000000f8 RegionEpoch:{ConfVer:1 Version:24} Peers:[id:49 store_id:1 ]}"] ["new region count"=1]
   > [2024/07/12 09:26:16.376 +00:00] [INFO] [raft.rs:285] [newRaft] [peers="[(49, Progress { matched: 5, next_idx: 6, state: Probe, paused: false, pending_snapshot: 0, pending_request_snapshot: 0, recent_active: false, ins: Inflights { start: 0, count: 0, buffer: [] } })]"] ["last term"=5] ["last index"=5] [applied=5] [commit=5] [term=5] [raft_id=49] [region_id=48]
   > [2024/07/12 09:26:16.376 +00:00] [INFO] [split_region.go:209] ["split regions complete"] ["region count"=1] ["region IDs"="[48]"]
   > [2024/07/12 09:26:16.376 +00:00] [INFO] [raw_node.rs:222] ["RawNode created with id 49."] [id=49] [raft_id=49] [region_id=48]
   > [2024/07/12 09:26:16.376 +00:00] [INFO] [raft.rs:1177] ["starting a new election"] [term=5] [raft_id=49] [region_id=48]
   > [2024/07/12 09:26:16.376 +00:00] [INFO] [raft.rs:833] ["became pre-candidate at term 5"] [term=5] [raft_id=49] [region_id=48]
   > [2024/07/12 09:26:16.376 +00:00] [INFO] [cluster.go:542] ["region Version changed"] [region-id=2] [detail="StartKey Changed:{7480000000000000FF3400000000000000F8} -> {7480000000000000FF3A00000000000000F8}, EndKey:{}"] [old-version=23] [new-version=24]
   > [2024/07/12 09:26:16.376 +00:00] [INFO] [raft.rs:902] ["49 received message from 49"] [term=5] [msg=MsgRequestPreVote] [from=49] [id=49] [raft_id=49] [region_id=48]
   > [2024/07/12 09:26:16.376 +00:00] [INFO] [cluster_worker.go:217] ["region batch split, generate new regions"] [region-id=2] [origin="id:48 start_key:\"7480000000000000FF3400000000000000F8\" end_key:\"7480000000000000FF3A00000000000000F8\" region_epoch:<conf_ver:1 version:24 > peers:<id:49 store_id:1 >"] [total=1]
   > [2024/07/12 09:26:16.376 +00:00] [INFO] [raft.rs:807] ["became candidate at term 6"] [term=6] [raft_id=49] [region_id=48]
   > [2024/07/12 09:26:16.376 +00:00] [INFO] [raft.rs:902] ["49 received message from 49"] [term=6] [msg=MsgRequestVote] [from=49] [id=49] [raft_id=49] [region_id=48]
   > [2024/07/12 09:26:16.376 +00:00] [INFO] [raft.rs:874] ["became leader at term 6"] [term=6] [raft_id=49] [region_id=48]
   > [2024/07/12 09:26:17.415 +00:00] [INFO] [set.go:216] ["set global var"] [conn=8] [name=tx_isolation] [val=REPEATABLE-READ]
   > [2024/07/12 09:26:17.418 +00:00] [INFO] [set.go:216] ["set global var"] [conn=8] [name=transaction_isolation] [val=REPEATABLE-READ]