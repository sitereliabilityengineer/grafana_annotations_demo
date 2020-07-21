SET GLOBAL sql_mode = '';
use grafana;

create table Metrics (
   metric_name VARCHAR(20) NOT NULL,
   timestamp_in_s BIGINT(15),
   metric_data INT(10)
);

create table annotations (
  id int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id),
   timestamp_in_s BIGINT(15),
   timeEnd BIGINT(15),
   text VARCHAR(300),
   tags VARCHAR(80)
);
