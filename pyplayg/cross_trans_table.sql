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

group by 

order by 

;
