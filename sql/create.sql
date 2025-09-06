-- chat_quant.stock_data_day definition

CREATE TABLE `stock_data_day` (
  `stock_code` varchar(100) NOT NULL DEFAULT '' COMMENT '股票代码',
  `data_date` date NOT NULL DEFAULT '0000-00-00' COMMENT '日期',
  `open` decimal(10,4) DEFAULT NULL COMMENT '开盘',
  `close` decimal(10,4) DEFAULT NULL COMMENT '收盘',
  `high` decimal(10,4) DEFAULT NULL COMMENT '最高',
  `low` decimal(10,4) DEFAULT NULL COMMENT '最低',
  `volume` bigint(20) DEFAULT NULL COMMENT '成交量',
  `turnover` decimal(10,4) DEFAULT NULL COMMENT '成交额',
  `amplitude` decimal(10,4) DEFAULT NULL COMMENT '振幅',
  `change_rate` decimal(10,4) DEFAULT NULL COMMENT '涨跌幅',
  `change_amount` decimal(10,4) DEFAULT NULL COMMENT '涨跌额',
  `turnover_rate` decimal(10,4) DEFAULT NULL COMMENT '换手率',
  `import_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`stock_code`,`data_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;