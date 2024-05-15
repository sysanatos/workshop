-- a mysql PROCEDURE to cut history data into a history table
DELIMITER $$
CREATE PROCEDURE `pro_cut_data_his`(tableName VARCHAR(255), columnNName VARCHAR(255))
begin
DECLARE histableName VARCHAR(255);
-- set @histableName = concat(@tableName, '_his_', date_format(now(),'%Y%m'));
set @histableName = concat(@tableName, '_his');
set @orderDate = date_format(CURDATE(), "%Y%m%d");
-- set @orderDate = date_format(CURDATE(), "%y%m%d");
set @insql = concat('insert into ', @histableName, ' select * from ', @tableName, ' where ' @columnNName ' like ' @orderDate '%;');
prepare stmt from @insql;
EXECUTE stmt;
deallocate prepare stmt;
end
$$
DELIMITER ;


