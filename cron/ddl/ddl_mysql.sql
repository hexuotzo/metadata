CREATE TABLE `hive_column_maintain` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `db_name` varchar(50) NOT NULL COMMENT '数据库名',
  `table_name` varchar(100) NOT NULL COMMENT '表名',
  `column_idx` int(10) NOT NULL DEFAULT '0' COMMENT '列的排序id,用来代替列名，防止字段修改关联不上的问题',
  `column_desc_maintain` varchar(200) DEFAULT NULL COMMENT '列描述维护信息',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_db_table_column` (`db_name`,`table_name`,`column_idx`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='hive列名手动维护';

CREATE TABLE `hive_org_info` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '组织名称',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_name` (`name`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='组织表';

CREATE TABLE `hive_owner_org` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `owner_name` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT 'owner名称',
  `org_id` int(10) DEFAULT '0' COMMENT '组织id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_org_owner` (`owner_name`,`org_id`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户组织关系表';

CREATE TABLE `hive_quality_rule` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `rule_name` varchar(50) CHARACTER SET utf8mb4 NOT NULL COMMENT '规则名称',
  `rule_type` tinyint(1) NOT NULL COMMENT '规则类型1-表级2-字段级3-自定义sql',
  `db_name` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '数据库名',
  `table_name` varchar(200) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '表名',
  `column_name` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '列名',
  `custom_sql` varchar(2000) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '自定义sql',
  `sampling_mode` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '采样方式count,sum,avg,max,min,空值，0值，重复值',
  `filter_condition` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '过滤条件',
  `check_type` tinyint(1) DEFAULT '0' COMMENT '校验类型1-数值型2-波动率型',
  `check_mode` tinyint(1) unsigned DEFAULT '0' COMMENT '校验方式与固定值比较，昨天对比，7天平均值，30天平均值',
  `compare_mode` varchar(50) DEFAULT NULL COMMENT '比较方式 > ,>=,<,<=,=,!=,rise,decline',
  `excepted_value` bigint(20) unsigned DEFAULT '0' COMMENT '期望值',
  `percent_min` int(10) unsigned DEFAULT '0' COMMENT '波动率百分比最小值',
  `rule_desc` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '规则描述',
  `status` varchar(10) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '状态on,0ff',
  `warning_mode` tinyint(1) unsigned DEFAULT '0' COMMENT '报警方式1-邮件2-短信',
  `warning_receiver` varchar(200) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '报警接收人',
  `execute_type` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '1-系统统一执行2-自定义时间执行',
  `execute_hour` varchar(20) CHARACTER SET utf8mb4 DEFAULT '' COMMENT '执行时间',
  `create_user` varchar(50) CHARACTER SET utf8mb4 NOT NULL COMMENT '创建人',
  `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='数据质量规则表';

CREATE TABLE `hive_rule_execute_log` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `rule_id` int(10) NOT NULL DEFAULT '0' COMMENT '规则id',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '执行状态0-未执行1-执行中2-执行完成3-触发预警4-执行错误',
  `error_msg` varchar(2000) DEFAULT '' COMMENT '错误内容',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL,
  `execute_seconds` int(10) NOT NULL DEFAULT '0' COMMENT '执行时长',
  `execute_sql` varchar(2000) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '执行sql',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='规则执行日志表';

CREATE TABLE `hive_rule_execute_num` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `rule_id` int(10) DEFAULT '0' COMMENT '规则id',
  `calculate_date` date DEFAULT NULL COMMENT '计算日期',
  `result_num` bigint(20) NOT NULL DEFAULT '0' COMMENT '执行结果条数',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `rule_date` (`rule_id`,`calculate_date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='规则执行结果表';

CREATE TABLE `hive_schedule_status` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `schedule_type` varchar(20) DEFAULT NULL COMMENT '调度类型makefile,azkaban',
  `table_name` varchar(50) DEFAULT NULL COMMENT '表名',
  `status` varchar(20) DEFAULT NULL COMMENT '执行状态 success,not begin',
  `execute_date` date DEFAULT NULL COMMENT '执行日期',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_type_date` (`schedule_type`,`table_name`,`execute_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='调度执行依赖状态表';

CREATE TABLE `hive_search_index` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `db_id` int(11) NOT NULL DEFAULT '0' COMMENT '数据库id',
  `db_name` varchar(255) DEFAULT NULL COMMENT '搜索内容的所属数据库',
  `table_id` int(11) NOT NULL DEFAULT '0' COMMENT '表id',
  `table_name` varchar(255) DEFAULT NULL COMMENT '表名',
  `table_name_split` varchar(255) DEFAULT NULL COMMENT '表名,用空格替换下划线',
  `is_online` tinyint(4) DEFAULT '1' COMMENT '是否在线1正常0-下线',
  `column_names` varchar(4000) DEFAULT NULL COMMENT '表所有字段',
  `column_names_split` varchar(4000) DEFAULT NULL COMMENT '所有字段名称，,用空格替换下划线',
  `table_content` varchar(1000) DEFAULT NULL COMMENT '表搜索内容',
  `column_content` varchar(5000) DEFAULT NULL COMMENT '字段搜索内容',
  `table_sort_priority` int(11) NOT NULL DEFAULT '0' COMMENT '表的排序优先级权重（0，1，2）表示低、中、高，默认0',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `position_id` (`db_id`,`table_id`),
  FULLTEXT KEY `ft_table_column_content` (`table_content`,`column_content`),
  FULLTEXT KEY `table_name_2` (`table_name`,`column_names`,`table_content`,`column_content`),
  FULLTEXT KEY `table_name` (`table_content`,`column_content`,`table_name_split`,`column_names_split`)
) ENGINE=InnoDB AUTO_INCREMENT=15715 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='hive索引信息表';

CREATE TABLE `hive_search_log` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `index_id` int(10) NOT NULL DEFAULT '0' COMMENT '索引表id',
  `db_name` varchar(50) CHARACTER SET utf8mb4 NOT NULL COMMENT '库名',
  `table_name` varchar(150) CHARACTER SET utf8mb4 NOT NULL DEFAULT '' COMMENT '表名',
  `author_id` int(10) NOT NULL DEFAULT '0' COMMENT '浏览人id',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '浏览时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='hive表浏览日志表';

CREATE TABLE `hive_table_all_storage` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `file_dir` varchar(100) CHARACTER SET utf8mb4 NOT NULL COMMENT '文件路径',
  `total_size` varchar(50) CHARACTER SET utf8mb4 NOT NULL COMMENT '总容量大小',
  `used_size` varchar(50) CHARACTER SET utf8mb4 NOT NULL COMMENT '已使用的空间大小',
  `use_percent` varchar(50) CHARACTER SET utf8mb4 NOT NULL COMMENT '已经使用的百分比',
  `calculate_date` date DEFAULT NULL COMMENT '统计日期',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '添加时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='表存储总量';

CREATE TABLE `hive_table_capacity` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `tbl_id` int(10) NOT NULL DEFAULT '0' COMMENT '表id',
  `storage` bigint(20) NOT NULL DEFAULT '0' COMMENT '存储大小',
  `storage_unit` varchar(10) CHARACTER SET utf8mb4 DEFAULT '' COMMENT '存储单位',
  `records` bigint(20) NOT NULL DEFAULT '0' COMMENT '记录数',
  `last_ddl_time` int(10) NOT NULL DEFAULT '0' COMMENT '最后修改时间',
  `calculate_date` date DEFAULT NULL COMMENT '计算日期',
  `storage_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '存储类型1-增量2-全量',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '添加时间',
  PRIMARY KEY (`id`),
  KEY `idx_tbl_id` (`tbl_id`,`calculate_date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='表空间存储';

CREATE TABLE `hive_table_column_info` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `column_id` varchar(50) NOT NULL DEFAULT '' COMMENT '字段id',
  `cd_id` int(10) NOT NULL DEFAULT '0',
  `integer_idx` int(10) NOT NULL DEFAULT '0' COMMENT '字段排序',
  `column_name` varchar(100) NOT NULL DEFAULT '' COMMENT '字段名称',
  `column_type` varchar(500) DEFAULT NULL COMMENT '字段类型',
  `column_desc` varchar(100) DEFAULT NULL COMMENT '字段描述',
  `tbl_id` int(10) NOT NULL DEFAULT '0' COMMENT '表id',
  `table_name` varchar(200) NOT NULL DEFAULT '' COMMENT '库表名',
  `db_id` int(10) DEFAULT '0' COMMENT '库id',
  `db_name` varchar(50) DEFAULT NULL COMMENT '库名称',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_column_tbl` (`column_id`,`tbl_id`) USING HASH,
  KEY `idx_tbl_id` (`tbl_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='元数据-字段基础信息表';

CREATE TABLE `hive_table_example` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `tbl_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '表id',
  `column_field` varchar(2000) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '字段数据',
  `column_data` text CHARACTER SET utf8mb4 COMMENT '字段数据',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='hive表数据example';

CREATE TABLE `hive_table_extend` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `tbl_id` int(10) DEFAULT NULL,
  `storage_format` varchar(50) DEFAULT NULL COMMENT '存储格式',
  `compression` varchar(50) DEFAULT NULL COMMENT '压缩格式',
  `last_ddl_time` datetime DEFAULT NULL COMMENT '最后ddl更新时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Hive信息扩展表';

CREATE TABLE `hive_table_info` (
  `tbl_id` int(11) NOT NULL DEFAULT '0' COMMENT '表id',
  `tbl_name` varchar(100) DEFAULT NULL COMMENT '表名称',
  `db_id` int(11) DEFAULT NULL COMMENT '数据库id',
  `db_name` varchar(100) DEFAULT NULL COMMENT '数据库名称',
  `tbl_type` varchar(25) DEFAULT NULL COMMENT '表类型',
  `tbl_owner` varchar(25) DEFAULT NULL COMMENT '表所有者',
  `create_time` varchar(25) DEFAULT NULL COMMENT '表创建时间',
  `is_online` int(2) DEFAULT NULL COMMENT '是否在线,0:下线，1：在线',
  `offline_time` varchar(25) DEFAULT NULL COMMENT '下线时间',
  `update_time` varchar(25) DEFAULT NULL COMMENT '最新更新时间',
  `location` varchar(500) DEFAULT NULL COMMENT '存储地址',
  `partition` varchar(100) DEFAULT NULL COMMENT '分区字段',
  `tbl_comment` varchar(200) DEFAULT NULL COMMENT '表注释',
  PRIMARY KEY (`tbl_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='hive表信息';

CREATE TABLE `hive_table_maintain` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `db_name` varchar(50) NOT NULL COMMENT '库名',
  `table_name` varchar(100) NOT NULL COMMENT '表名',
  `table_desc_maintain` varchar(100) DEFAULT NULL COMMENT '表名维护',
  `usage_desc` text COMMENT '使用描述',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_db_table_name` (`db_name`,`table_name`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='hive表名维护';


CREATE TABLE `makefile_tag_relations_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(100) DEFAULT NULL COMMENT '标记',
  `tag_rely` varchar(100) DEFAULT NULL COMMENT '标记依赖',
  `source` varchar(100) DEFAULT NULL COMMENT '执行目录',
  `scheduling` varchar(100) DEFAULT NULL COMMENT '调度频率',
  `host` varchar(100) DEFAULT NULL COMMENT '部署机器IP',
  `created` datetime DEFAULT NULL COMMENT '入库时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_key` (`source`,`tag`,`tag_rely`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2361 DEFAULT CHARSET=utf8mb4;