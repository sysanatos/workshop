-- Active: 1681090621303@@10.66.5.20@5432@analysis_db@public
select 
	source_trans_date,
	case 
		when business_type = 'CROSS_1_1' then '跨境付款(离岸换汇)' 
		when business_type = 'CROSS_1_2' then '跨境人民币付款' 
		when business_type = 'CROSS_1_3' then '跨境人民币收款' 
		when business_type = 'CROSS_1_4' then '网关与支付单报送' 
		when business_type = 'CROSS_1_5' then '网关b2b支付'
		else 'UNKNOWN' 
	end as business_type,
	sum(total_trans_amt) as total_trans_amt,
	sum(total_commission_amt + total_other_income_amt + total_income_amt) as total_income_amt,
	sum(total_cost_amt) as total_cost_amt
from anl_cross_business_group_by 
where 
	source_trans_date = '20230310'
group by 
	source_trans_date,
	business_type
	;

/*
		when business_type = 'CROSS_1_1' then '跨境付款(离岸换汇)' 
		when business_type = 'CROSS_1_2' then '跨境人民币付款' 
		when business_type = 'CROSS_1_3' then '跨境人民币收款' 
		when business_type = 'CROSS_1_4' then '网关与支付单报送' 
		when business_type = 'CROSS_1_5' then '网关b2b支付'
*/
-- business_type_test_summary
SELECT 
    source_trans_date as 日期,
    COALESCE(sum(trans_count), 0) as 笔数,
    COALESCE(SUM(total_trans_amt), 0) as 交易额,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_1' THEN total_trans_amt ELSE 0 END), 0) as 跨境付款（离岸换汇）,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_2' THEN total_trans_amt ELSE 0 END), 0) as 跨境人民币付款,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_3' THEN total_trans_amt ELSE 0 END), 0) as 跨境人民币收款,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_4' THEN total_trans_amt ELSE 0 END), 0) as 网关与支付单报送,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_5' THEN total_trans_amt ELSE 0 END), 0) as 网关b2b支付,
    sum(total_commission_amt + total_other_income_amt + total_income_amt) as 收入,
    sum(total_cost_amt) as 成本,
    sum(total_commission_amt + total_other_income_amt + total_income_amt - total_cost_amt) as 毛利
FROM anl_cross_business_group_by 
WHERE 
    source_trans_date LIKE '202303%'
GROUP BY 
    source_trans_date
ORDER BY
    source_trans_date 
    ;


--CROSS TRANS TABLE2 daily v1
select
    source_trans_date,
    case
        when business_type = 'CROSS_1_1' then '跨境付款(离岸换汇)'
        when business_type = 'CROSS_1_2' then '跨境人民币付款'
        when business_type = 'CROSS_1_3' then '跨境人民币收款'
        when business_type = 'CROSS_1_4' then '网关与支付单报送'
        when business_type = 'CROSS_1_5' then '网关b2b支付'
        else 'UNKNOWN'
    end as business_type,
    sum(trans_count) as total_trans_count,
    sum(total_trans_amt) as total_trans_amt,
    sum(
        total_commission_amt + total_other_income_amt + total_income_amt
    ) as total_income_amt,
    sum(total_cost_amt) as total_cost_amt
from
    anl_cross_business_group_by
where
    source_trans_date like '202303%'
group by
    source_trans_date,
    business_type
order by
    source_trans_date,
    business_type;

/*
WITH 
    dates AS (
        SELECT DISTINCT source_trans_date
        FROM anl_cross_business_group_by
        WHERE source_trans_date LIKE '202303%'
    ),
    types AS (
        SELECT DISTINCT business_type
        FROM anl_cross_business_group_by
    )
SELECT 
    dates.source_trans_date AS 日期,
    types.business_type AS 业务类型,
    COALESCE(SUM(total_trans_amt), 0) AS 交易额,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_1' THEN total_trans_amt ELSE 0 END), 0) AS 跨境付款(离岸换汇),
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_2' THEN total_trans_amt ELSE 0 END), 0) AS 跨境人民币付款,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_3' THEN total_trans_amt ELSE 0 END), 0) AS 跨境人民币收款,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_4' THEN total_trans_amt ELSE 0 END), 0) AS 网关与支付单报送,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_5' THEN total_trans_amt ELSE 0 END), 0) AS 网关b2b支付,
    COALESCE(SUM(total_commission_amt + total_other_income_amt + total_income_amt), 0) AS 收入,
    COALESCE(SUM(total_cost_amt), 0) AS 成本,
    COALESCE(SUM(total_commission_amt + total_other_income_amt + total_income_amt - total_cost_amt), 0) AS 毛利
FROM 
    dates
    CROSS JOIN types
    LEFT JOIN anl_cross_business_group_by ON dates.source_trans_date = anl_cross_business_group_by.source_trans_date AND types.business_type = anl_cross_business_group_by.business_type
GROUP BY 
    dates.source_trans_date,
    types.business_type
ORDER BY 
    dates.source_trans_date,
    types.business_type;
*/

--CROSS TRANS TABLE DAILY V2
SELECT 
    source_trans_date AS date,
--    types.business_type AS 业务类型,
    case
        when business_type = 'CROSS_1_1' then '跨境付款(离岸换汇)'
        when business_type = 'CROSS_1_2' then '跨境人民币付款'
        when business_type = 'CROSS_1_3' then '跨境人民币收款'
        when business_type = 'CROSS_1_4' then '网关与支付单报送'
        when business_type = 'CROSS_1_5' then '网关b2b支付'
        else 'UNKNOWN'
    end as business_type,
    COALESCE(SUM(total_trans_amt), 0) AS 交易金额,
    COALESCE(SUM(total_commission_amt + total_other_income_amt + total_income_amt), 0) AS 收入,
    COALESCE(SUM(total_cost_amt), 0) AS 成本,
    COALESCE(SUM(total_commission_amt + total_other_income_amt + total_income_amt - total_cost_amt), 0) AS 毛利
FROM 
    anl_cross_business_group_by
--    (SELECT DISTINCT source_trans_date FROM anl_cross_business_group_by WHERE source_trans_date LIKE '202303%') AS dates
--    CROSS JOIN (SELECT DISTINCT business_type FROM anl_cross_business_group_by) AS types
--    LEFT JOIN anl_cross_business_group_by ON dates.source_trans_date = anl_cross_business_group_by.source_trans_date AND types.business_type = anl_cross_business_group_by.business_type
GROUP BY 
    date,
    business_type
--    dates.source_trans_date,
--    types.business_type
ORDER BY 
    date,
    business_type
--    dates.source_trans_date,
--    types.business_type;
    ;

/*
--SELECT DATE_TRUNC('month', CURRENT_DATE);
--select DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month';

select to_char(days, YYYYMMDD) WHERE days BETWEEN DATE_TRUNC('month', CURRENT_DATE) AND DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month';
select to_char(DATE_TRUNC('month', CURRENT_DATE), 'YYYYMMDD');
select date_trunc('month', CURRENT_DATE);

select date(t) from generate_series(DATE_TRUNC('month', CURRENT_DATE) , DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month') as t;
*/
SELECT date(t) 
FROM generate_series(DATE_TRUNC('month', CURRENT_DATE - 1), DATE_TRUNC('month', CURRENT_DATE - 1) + INTERVAL '1 month' - INTERVAL '1 day', INTERVAL '1 day') as t;

WITH all_dates AS (
  SELECT date(t) AS date
  FROM generate_series(DATE_TRUNC('month', CURRENT_DATE), DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month' - INTERVAL '1 day', INTERVAL '1 day') as t
)
SELECT 
  all_dates.date,
  'A' AS row_name,
  NULL AS value
FROM all_dates
UNION ALL
SELECT 
  all_dates.date,
  'B' AS row_name,
  NULL AS value
FROM all_dates
UNION ALL
SELECT 
  all_dates.date,
  'C' AS row_name,
  NULL AS value
FROM all_dates
UNION ALL
SELECT 
  all_dates.date,
  'D' AS row_name,
  NULL AS value
FROM all_dates
UNION ALL
SELECT 
  all_dates.date,
  'E' AS row_name,
  NULL AS value
FROM all_dates
ORDER BY date, row_name
;



-- CROSS_TABLE_2_TEST
select 
	today.source_trans_date as 日期,
    case
        when today.business_type = 'CROSS_1_1' then '跨境付款(离岸换汇)'
        when today.business_type = 'CROSS_1_2' then '跨境人民币付款'
        when today.business_type = 'CROSS_1_3' then '跨境人民币收款'
        when today.business_type = 'CROSS_1_4' then '网关与支付单报送'
        when today.business_type = 'CROSS_1_5' then '网关b2b支付'
        else 'UNKNOWN'
    end as 业务类型,
    COALESCE(SUM(today.total_trans_amt), 0) as 当天交易量,
    COALESCE(SUM(yesterday.total_trans_amt), 0) as 前一天交易量,
    COALESCE(SUM(today.total_commission_amt + today.total_other_income_amt + today.total_income_amt), 0) AS 当天收入,
    COALESCE(SUM(yesterday.total_commission_amt + yesterday.total_other_income_amt + yesterday.total_income_amt), 0) AS 前一天收入,
    COALESCE(SUM(today.total_commission_amt + today.total_other_income_amt + today.total_income_amt - total_cost_amt), 0) AS 当天毛利,
    COALESCE(SUM(yesterday.total_commission_amt + yesterday.total_other_income_amt + yesterday.total_income_amt - total_cost_amt), 0) AS 前一天毛利,
    case when 前一天交易量 = 0 then '100.00%' else cast((当天交易量 / 前一天交易量 - 1) * 100 as decimal(10,2)) || '%' end as 交易量日环比，
    case when 前一天交易量 = 0 then '100.00%' else cast((当天收入 / 前一天收入 - 1) * 100 as decimal(10,2)) || '%' end as 收入日环比，
    case when 前一天交易量 = 0 then '100.00%' else cast((当天毛利 / 前一天毛利 - 1) * 100 as decimal(10,2)) || '%' end as 毛利日环比
from
	anl_cross_business_group_by as today	
left join
	anl_cross_business_group_by as yesterday 
on today.source_trans_date = yesterday.source_trans_date - 1
where 
    today.source_trans_date BETWEEN to_char((DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 day')::DATE, 'YYYYMMDD') AND to_char((current_date - interval '1 day')::DATE, 'YYYYMMDD') 
group by 
    日期,
    业务类型,
    交易量日环比,
    收入日环比，
    毛利日环比
order by 
    日期,
    业务类型
;

/* DECLARE @CurrentMonth DATE = DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0)

IF EXISTS (SELECT * FROM TableName WHERE DateColumn = @CurrentMonth)
BEGIN
  UPDATE TableName
  SET Column1 = SUM(Column1), Column2 = SUM(Column2), ... 
  WHERE DateColumn = @CurrentMonth
END 
ELSE
BEGIN
  INSERT INTO TableName (DateColumn, Column1, Column2, ...)
  SELECT @CurrentMonth, SUM(Column1), SUM(Column2), ...
  FROM TableName
  WHERE MONTH(DateColumn) = MONTH(@CurrentMonth) AND YEAR(DateColumn) = YEAR(@CurrentMonth)
END
 */


-- business_type_test_summary
/* 
SELECT 
    source_trans_date as 日期,
    COALESCE(sum(trans_count), 0) as 笔数,
    COALESCE(SUM(total_trans_amt), 0) as 交易额,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_1' THEN total_trans_amt ELSE 0 END), 0) as 跨境付款（离岸换汇）,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_2' THEN total_trans_amt ELSE 0 END), 0) as 跨境人民币付款,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_3' THEN total_trans_amt ELSE 0 END), 0) as 跨境人民币收款,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_4' THEN total_trans_amt ELSE 0 END), 0) as 网关与支付单报送,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_5' THEN total_trans_amt ELSE 0 END), 0) as 网关b2b支付,
    sum(total_commission_amt + total_other_income_amt + total_income_amt) as 收入,
    sum(total_cost_amt) as 成本,
    sum(total_commission_amt + total_other_income_amt + total_income_amt - total_cost_amt) as 毛利
FROM anl_cross_business_group_by 
WHERE 
    source_trans_date LIKE '202303%'
GROUP BY 
    source_trans_date
ORDER BY
    source_trans_date 
    ;
 */

SELECT 
--  source_trans_date
    to_char(current_date, 'YYYYMM') || '00' as 日期,
    COALESCE(sum(trans_count), 0) as 笔数,
    COALESCE(SUM(total_trans_amt), 0) as 交易额,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_1' THEN total_trans_amt ELSE 0 END), 0) as 跨境付款（离岸换汇）,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_2' THEN total_trans_amt ELSE 0 END), 0) as 跨境人民币付款,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_3' THEN total_trans_amt ELSE 0 END), 0) as 跨境人民币收款,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_4' THEN total_trans_amt ELSE 0 END), 0) as 网关与支付单报送,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_5' THEN total_trans_amt ELSE 0 END), 0) as 网关b2b支付,
    sum(total_commission_amt + total_other_income_amt + total_income_amt) as 收入,
    sum(total_cost_amt) as 成本,
    sum(total_commission_amt + total_other_income_amt + total_income_amt - total_cost_amt) as 毛利
FROM anl_cross_business_group_by 
WHERE 
    source_trans_date BETWEEN to_char((DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 day')::DATE, 'YYYYMMDD') AND to_char((current_date - interval '1 day')::DATE, 'YYYYMMDD') 
GROUP BY
    日期
    ;


select (DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 day')::DATE;
SELECT (current_date - interval '1 day')::DATE;
-- insert if not exists else update
/*  
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...)
ON CONFLICT (column_name)
DO UPDATE SET column1 = value1, column2 = value2, ...;
*/

/* 
SELECT column_name1, column_name2 FROM table_name WHERE condition1
UNION
SELECT column_name1, column_name2 FROM table_name WHERE condition2; 
*/

---------------------------------------------------------------------------THIS IS A LINE, BLOW IS FINAL WORK-------------------------------------------------------------------------------
--CROSS TABLE 1 FINAL VERSION
SELECT 
    source_trans_date as 日期,
    COALESCE(sum(trans_count), 0) as 笔数,
    COALESCE(SUM(total_trans_amt), 0) as 交易额,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_1' THEN total_trans_amt ELSE 0 END), 0) as 跨境付款（离岸换汇）,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_2' THEN total_trans_amt ELSE 0 END), 0) as 跨境人民币付款,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_3' THEN total_trans_amt ELSE 0 END), 0) as 跨境人民币收款,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_4' THEN total_trans_amt ELSE 0 END), 0) as 网关与支付单报送,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_5' THEN total_trans_amt ELSE 0 END), 0) as 网关b2b支付,
    sum(total_commission_amt + total_other_income_amt + total_income_amt) as 收入,
    sum(total_cost_amt) as 成本,
    sum(total_commission_amt + total_other_income_amt + total_income_amt - total_cost_amt) as 毛利
FROM anl_cross_business_group_by 
WHERE 
    source_trans_date LIKE '202304%'
GROUP BY 
    日期
UNION
SELECT 
    '0汇总' AS 日期,
--    to_char(current_date, 'YYYYMM') || '00' as 日期,
    COALESCE(sum(trans_count), 0) as 笔数,
    COALESCE(SUM(total_trans_amt), 0) as 交易额,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_1' THEN total_trans_amt ELSE 0 END), 0) as 跨境付款（离岸换汇）,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_2' THEN total_trans_amt ELSE 0 END), 0) as 跨境人民币付款,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_3' THEN total_trans_amt ELSE 0 END), 0) as 跨境人民币收款,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_4' THEN total_trans_amt ELSE 0 END), 0) as 网关与支付单报送,
    COALESCE(SUM(CASE WHEN business_type = 'CROSS_1_5' THEN total_trans_amt ELSE 0 END), 0) as 网关b2b支付,
    sum(total_commission_amt + total_other_income_amt + total_income_amt) as 收入,
    sum(total_cost_amt) as 成本,
    sum(total_commission_amt + total_other_income_amt + total_income_amt - total_cost_amt) as 毛利
FROM anl_cross_business_group_by 
WHERE 
    source_trans_date BETWEEN to_char((DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 day')::DATE, 'YYYYMMDD') AND to_char((current_date - interval '1 day')::DATE, 'YYYYMMDD') 
GROUP BY
    日期
ORDER BY
    日期 
    ;

-- CROSS TABLE 2
-- This is a rewritable version below
/*
select 
	fv.日期,
	case
        when fv.业务类型 = 'CROSS_1_1' then '跨境付款(离岸换汇)'
        when fv.业务类型 = 'CROSS_1_2' then '跨境人民币付款'
        when fv.业务类型 = 'CROSS_1_3' then '跨境人民币收款'
        when fv.业务类型 = 'CROSS_1_4' then '网关与支付单报送'
        when fv.业务类型 = 'CROSS_1_5' then '网关b2b支付'
        else 'UNKNOWN'
    end as 业务类型,	
    fv.当天交易量,
    fv.前一天交易量 as 前一天交易量,
    fv.当天收入 AS 当天收入,
    fv.前一天收入 AS 前一天收入,
    fv.当天毛利 AS 当天毛利,
    fv.前一天毛利 AS 前一天毛利,
    fv.交易量日环比 as 交易量日环比,
    fv.收入日环比 as 收入日环比,
    fv.毛利日环比 as 毛利日环比
from
(*/
select 
	today.trans_date as 日期,
--/*    
	case
        when today.business_type = 'CROSS_1_1' then '1跨境付款(离岸换汇)'
        when today.business_type = 'CROSS_1_2' then '2跨境人民币付款'
        when today.business_type = 'CROSS_1_3' then '3跨境人民币收款'
        when today.business_type = 'CROSS_1_4' then '4网关与支付单报送'
        when today.business_type = 'CROSS_1_5' then '5网关b2b支付'
        else 'UNKNOWN'
    end as 业务类型,
--*/
--	today.business_type as 业务类型,
    today.trans_amt as 当天交易量,
    yesterday.trans_amt as 前一天交易量,
    today.trans_income AS 当天收入,
    yesterday.trans_income AS 前一天收入,
    today.trans_profit AS 当天毛利,
    yesterday.trans_profit AS 前一天毛利,
    case 
	    when today.trans_amt = 0 and yesterday.trans_amt = 0 then '-'
	    when yesterday.trans_amt = 0 then '100.00%' 
	    else cast((today.trans_amt / yesterday.trans_amt - 1) * 100 as decimal(10,2)) || '%' 
	end as 交易量日环比,
    case 
	    when today.trans_income = 0 and yesterday.trans_income =0 then '-'
	    when yesterday.trans_income = 0 then '100.00%' 
	    else cast((today.trans_income / yesterday.trans_income - 1) * 100 as decimal(10,2)) || '%' 
	end as 收入日环比,
    case 
	    when today.trans_profit = 0 and yesterday.trans_profit = 0 then '-'
	    when yesterday.trans_profit = 0 then '100.00%' 
	    else cast((today.trans_profit / yesterday.trans_profit - 1) * 100 as decimal(10,2)) || '%' 
	end as 毛利日环比
from 
	(
/*----date与business_type补齐测试----*/
----begin----
	select 
		trans_time.trans_date, 
		bus.business_type, 
		COALESCE(td.trans_amt, 0) as trans_amt,
		COALESCE(td.trans_income, 0) as trans_income,
		coalesce(td.trans_profit, 0) as trans_profit
	from 
		(
		select 'CROSS_1_1' as business_type
		union
		select 'CROSS_1_2' as business_type
		union
		select 'CROSS_1_3' as business_type
		union
		select 'CROSS_1_4' as business_type
		union
		select 'CROSS_1_5' as business_type
		) bus
		left join (
			select to_char(t, 'YYYYMMDD') as trans_date from generate_series((DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 day')::DATE, (current_date - interval '1 day')::DATE, INTERVAL '1 day') as t
/*		'20230310' as tran_date
		union all
		select '20230311'
		union all
		select '20230312'
*/		
		) trans_time
		on 1=1
	left join
	(
	select 
		source_trans_date as trans_date,
		business_type as business_type,
		COALESCE(SUM(total_trans_amt), 0) as trans_amt,
		COALESCE(SUM(total_commission_amt + total_other_income_amt + total_income_amt), 0) as trans_income,
		COALESCE(SUM(total_commission_amt + total_other_income_amt + total_income_amt - total_cost_amt), 0) as trans_profit
	from anl_cross_business_group_by 
	group by 
		trans_date,
		business_type
	) td
	on bus.business_type = td.business_type 
	and trans_time.trans_date=td.trans_date
--	where 	
--	order by 1,2
----end----
	) today
left join 
	(
/*	select 
		source_trans_date as trans_date,
		business_type as business_type,
		COALESCE(SUM(total_trans_amt), 0) as trans_amt,
		COALESCE(SUM(total_commission_amt + total_other_income_amt + total_income_amt), 0) as trans_income,
		COALESCE(SUM(total_commission_amt + total_other_income_amt + total_income_amt - total_cost_amt), 0) as trans_profit
	from anl_cross_business_group_by 
--	where 
	group by 
		trans_date,
		business_type
		*/
	select 
		trans_time.trans_date, 
		bus.business_type, 
		COALESCE(td.trans_amt, 0) as trans_amt,
		COALESCE(td.trans_income, 0) as trans_income,
		coalesce(td.trans_profit, 0) as trans_profit
	from 
		(
		select 'CROSS_1_1' as business_type
		union
		select 'CROSS_1_2' as business_type
		union
		select 'CROSS_1_3' as business_type
		union
		select 'CROSS_1_4' as business_type
		union
		select 'CROSS_1_5' as business_type
		) bus
		left join (
			select to_char(t, 'YYYYMMDD') as trans_date from generate_series((DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 day')::DATE, (current_date - interval '1 day')::DATE, INTERVAL '1 day') as t
/*		'20230310' as tran_date
		union all
		select '20230311'
		union all
		select '20230312'
*/		
		) trans_time
		on 1=1
	left join
	(
	select 
		source_trans_date as trans_date,
		business_type as business_type,
		COALESCE(SUM(total_trans_amt), 0) as trans_amt,
		COALESCE(SUM(total_commission_amt + total_other_income_amt + total_income_amt), 0) as trans_income,
		COALESCE(SUM(total_commission_amt + total_other_income_amt + total_income_amt - total_cost_amt), 0) as trans_profit
	from anl_cross_business_group_by 
	group by 
		trans_date,
		business_type
	) td
	on bus.business_type = td.business_type 
	and trans_time.trans_date=td.trans_date
	) yesterday
on 
	to_date(today.trans_date, 'YYYYMMDD') = to_date(yesterday.trans_date, 'YYYYMMDD') + 1 
	and today.business_type = yesterday.business_type
where 
	yesterday.trans_date BETWEEN to_char((DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 day')::DATE, 'YYYYMMDD') AND to_char((current_date - interval '1 day')::DATE, 'YYYYMMDD')
--	today.trans_date BETWEEN to_char((DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 day')::DATE, 'YYYYMMDD') AND to_char((current_date - interval '1 day')::DATE, 'YYYYMMDD')
order by 
	日期,
--	business_type
	业务类型
	;
/*
) fv
order by 
	日期,
	业务类型
;
	*/



-- CROSS TABLE 2
-- final version
select 
	today.trans_date as 日期,
	case
		when today.business_type = 'CROSS_1_1' then '1跨境付款(离岸换汇)'
		when today.business_type = 'CROSS_1_2' then '2跨境人民币付款'
		when today.business_type = 'CROSS_1_3' then '3跨境人民币收款'
		when today.business_type = 'CROSS_1_4' then '4网关与支付单报送'
		when today.business_type = 'CROSS_1_5' then '5网关b2b支付'
		else 'UNKNOWN'
	end as 业务类型,
	today.trans_amt as 当天交易量,
	yesterday.trans_amt as 前一天交易量,
	today.trans_income as 当天收入,
	yesterday.trans_income as 前一天收入,
	today.trans_profit as 当天毛利,
	yesterday.trans_profit as 前一天毛利,
	case
		when today.trans_amt = 0
		and yesterday.trans_amt = 0 then '-'
		when yesterday.trans_amt = 0 then '100.00%'
		else cast((today.trans_amt / yesterday.trans_amt - 1) * 100 as decimal(10, 2)) || '%'
	end as 交易量日环比,
	case
		when today.trans_income = 0
		and yesterday.trans_income = 0 then '-'
		when yesterday.trans_income = 0 then '100.00%'
		else cast((today.trans_income / yesterday.trans_income - 1) * 100 as decimal(10, 2)) || '%'
	end as 收入日环比,
	case
		when today.trans_profit = 0
		and yesterday.trans_profit = 0 then '-'
		when yesterday.trans_profit = 0 then '100.00%'
		else cast((today.trans_profit / yesterday.trans_profit - 1) * 100 as decimal(10, 2)) || '%'
	end as 毛利日环比
from 
	(
	select 
		trans_time.trans_date, 
		bus.business_type, 
		coalesce(td.trans_amt, 0) as trans_amt,
		coalesce(td.trans_income, 0) as trans_income,
		coalesce(td.trans_profit, 0) as trans_profit
	from 
		(
		select
			'CROSS_1_1' as business_type
	union
		select
			'CROSS_1_2' as business_type
	union
		select
			'CROSS_1_3' as business_type
	union
		select
			'CROSS_1_4' as business_type
	union
		select
			'CROSS_1_5' as business_type
		) bus
	left join (
		select
			to_char(t, 'YYYYMMDD') as trans_date
		from
			generate_series((DATE_TRUNC('month', CURRENT_DATE) - interval '1 day')::DATE, (current_date - interval '1 day')::DATE, interval '1 day') as t
		) trans_time
		on
		1 = 1
	left join
	(
		select
			source_trans_date as trans_date,
			business_type as business_type,
			coalesce(SUM(total_trans_amt), 0) as trans_amt,
			coalesce(SUM(total_commission_amt + total_other_income_amt + total_income_amt), 0) as trans_income,
			coalesce(SUM(total_commission_amt + total_other_income_amt + total_income_amt - total_cost_amt), 0) as trans_profit
		from
			anl_cross_business_group_by
		group by
			trans_date,
			business_type
	) td
	on
		bus.business_type = td.business_type
		and trans_time.trans_date = td.trans_date
	) today
left join 
	(
	select 
		trans_time.trans_date, 
		bus.business_type, 
		coalesce(td.trans_amt, 0) as trans_amt,
		coalesce(td.trans_income, 0) as trans_income,
		coalesce(td.trans_profit, 0) as trans_profit
	from 
		(
		select
			'CROSS_1_1' as business_type
	union
		select
			'CROSS_1_2' as business_type
	union
		select
			'CROSS_1_3' as business_type
	union
		select
			'CROSS_1_4' as business_type
	union
		select
			'CROSS_1_5' as business_type
		) bus
	left join (
		select
			to_char(t, 'YYYYMMDD') as trans_date
		from
			generate_series((DATE_TRUNC('month', CURRENT_DATE) - interval '1 day')::DATE, (current_date - interval '1 day')::DATE, interval '1 day') as t
		) trans_time
		on
		1 = 1
	left join
	(
		select
			source_trans_date as trans_date,
			business_type as business_type,
			coalesce(SUM(total_trans_amt), 0) as trans_amt,
			coalesce(SUM(total_commission_amt + total_other_income_amt + total_income_amt), 0) as trans_income,
			coalesce(SUM(total_commission_amt + total_other_income_amt + total_income_amt - total_cost_amt), 0) as trans_profit
		from
			anl_cross_business_group_by
		group by
			trans_date,
			business_type
	) td
	on
		bus.business_type = td.business_type
		and trans_time.trans_date = td.trans_date
	) yesterday
on 
	to_date(today.trans_date, 'YYYYMMDD') = to_date(yesterday.trans_date, 'YYYYMMDD') + 1
	and today.business_type = yesterday.business_type
where 
	yesterday.trans_date between to_char((DATE_TRUNC('month', CURRENT_DATE) - interval '1 day')::DATE, 'YYYYMMDD') and to_char((current_date - interval '1 day')::DATE, 'YYYYMMDD')
order by 
	日期,
	业务类型
	;



