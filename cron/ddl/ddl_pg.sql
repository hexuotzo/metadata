create table hive_table_maintain
(
  id serial PRIMARY KEY,
  db_name varchar(50) not null ,
  table_name varchar(100) not null,
  table_desc_maintain varchar(100) null,
  usage_desc text,
  create_time timestamp,
  update_time timestamp
);


create table hive_table_info
(
  tbl_id integer PRIMARY KEY,
  tbl_name varchar(100) not null,
  db_id integer default 0,
  db_name varchar(50) not null ,
  tbl_type varchar(25) default null,
  tbl_owner varchar(25) default null,
  create_time varchar(25) default null,
  is_online integer default 0,
  offline_time varchar(25) default null,
  update_time varchar(25) default null,
  location varchar(500) default null,
  partition varchar(100) default null,
  tbl_comment varchar(200) default null
);

create table hive_table_extend
(
  id serial PRIMARY KEY,
  tbl_id integer default 0,
  storage_format varchar(50) default null,
  compression varchar(50) default null,
  last_ddl_time timestamp default null,
  create_time timestamp,
  update_time timestamp
);


create table hive_table_example
(
  id serial PRIMARY KEY,
  tbl_id integer default 0,
  column_field varchar(2000) default null,
  column_data text default null,
  create_time timestamp,
  update_time timestamp
);


create table hive_table_column_info
(
  id serial PRIMARY KEY,
  column_id varchar(50) default null,
  cd_id integer default 0,
  integer_idx integer default 0,
  column_name varchar(100) default null,
  column_type varchar(500) default null,
  column_desc varchar(100) default null,
  tbl_id integer default 0,
  table_name varchar(200) default null,
  db_id integer default 0,
  db_name varchar(50) default null,
  create_time timestamp,
  update_time timestamp
);

create table hive_table_capacity
(
  id serial PRIMARY KEY,
  tbl_id integer default 0,
  storage bigint default 0,
  storage_unit varchar(10) default null,
  records bigint default 0,
  last_ddl_time integer default 0,
  calculate_date date,
  storage_type integer default 0,
  create_time timestamp
);


create table hive_table_all_storage
(
  id serial PRIMARY KEY,
  file_dir varchar(100) default null,
  total_size varchar(50) default null,
  used_size varchar(50) default null,
  use_percent varchar(50) default null,
  calculate_date date,
  create_time timestamp
);


create table hive_search_log
(
  id serial PRIMARY KEY,
  index_id integer default 0,
  db_name varchar(50) default null,
  table_name varchar(150) default null,
  author_id integer default 0,
  create_time timestamp
);


create table hive_search_index
(
  id serial PRIMARY KEY,
  db_id integer default 0,
  db_name varchar(255) default null,
  table_id integer default 0,
  table_name varchar(255) default null,
  table_name_split varchar(255) default null,
  is_online integer default 0,
  column_names text default null,
  column_names_split text default null,
  table_content varchar(1000) default null,
  column_content varchar(1000) default null,
  table_sort_priority integer,
  create_time timestamp,
  update_time timestamp
);


create table hive_schedule_status
(
  id serial PRIMARY KEY,
  schedule_type varchar(20) default null,
  table_name varchar(50) default null,
  status varchar(20) default null,
  execute_date date,
  start_time timestamp,
  end_time timestamp,
  create_time timestamp
);



create table hive_rule_execute_num
(
  id serial PRIMARY KEY,
  rule_id integer default 0,
  calculate_date date,
  result_num bigint default 0,
  create_time timestamp
);


create table hive_rule_execute_log
(
  id serial PRIMARY KEY,
  rule_id integer default 0,
  status integer default 0,
  error_msg varchar(2000),
  start_time timestamp default null,
  end_time timestamp default null,
  execute_seconds integer default 0,
  execute_sql varchar(2000) default null,
  create_time timestamp
);



create table hive_column_maintain
(
  id serial PRIMARY KEY,
  db_name varchar(50) default null,
  table_name varchar(100) default null,
  column_idx integer default 0,
  column_desc_maintain varchar(200) default null,
  create_time timestamp,
  update_time timestamp
);


create table hive_org_info
(
  id serial PRIMARY KEY,
  name varchar(100) default null,
  create_time timestamp,
  update_time timestamp
);


create table hive_owner_org
(
  id serial PRIMARY KEY,
  owner_name varchar(100) default null,
  org_id integer default 0,
  create_time timestamp,
  update_time timestamp
);


create table makefile_tag_relations_test
(
  id serial PRIMARY KEY,
  tag varchar(100) default null,
  tag_rely varchar(100) default null,
  source varchar(100) default null,
  scheduling varchar(100) default null,
  host varchar(100) default null,
  created timestamp
);
