import time
import streamlit as st
import pandas as pd
import numpy as np

from IPython.display import display

st.set_page_config(
    page_title="My test streamlit page",
    page_icon="random",
    layout="wide",
    initial_sidebar_state="collapsed",
)



st.title('This is the first test with streamlit')

st.write("creating a dataframe **test_data**:")
df = pd.DataFrame({
    '1st column': [1, 2, 3, 4, 5],
    '2st column': [10, 20, 30, 40, 50],
    '3st column': [100, 200, 300, 400, 500]
})
df

char_data = pd.DataFrame(
    np.random.randn(50, 5),
    columns=['A', 'B', 'C', 'D', 'E'])
st.write("char_data: line table test")
st.line_chart(char_data)


st.write("**Database** test")

import psycopg2
# Connect to PostgreSQL database
pg_conn = psycopg2.connect(
    host="10.66.5.20",
    database="analysis_db",
    user="data_analysis",
    password="data_analysis"
)
pg_query1 = """
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

"""
pg_query2 = """
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
"""

#print table1
pg_df_test1 = pd.read_sql(pg_query1, pg_conn)
pg_df_test1

#display table2
pg_df_test2 = pd.read_sql(pg_query2, pg_conn)

#table pivot doesn't work, i don't know why...
'''
pg_df_test2 = pd.pivot_table(pg_df_test2, 
                            values=[u'当天交易量', u'前一天交易量', u'当天收入', u'前一天收入', u'当天毛利', u'前一天毛利', u'交易量日环比', u'收入日环比', u'毛利日环比'], 
                            index=[ u'日期', u'业务类型'])
'''
pg_df_test2
#display(pg_df_test2)
#we don't have display...

#table width test, to be countinue
'''
#set dataframe width, try to use user-defined session width
@st.cache_data
#pg_df_test = pd.read_sql(pg_query, pg_conn)
def load_data():
    pg_df_test2 = pd.read_sql(pg_query2, pg_conn)
    return pg_df_test2

st.checkbox("Use container width", value=False, key="use_container_width")
#pg_df_test = pd.read_sql(pg_query, pg_conn)

df_test = load_data()

'''
'''
st.dataframe(df_test, use_container_width=st.session_state.use_container_width)
df_test
'''

option = st.selectbox('Select option', ('simple', 'full'))
'It will show as your choice:', option

side_option = st.sidebar.selectbox('Select side option', ('left', 'right'))
'Your choice:', side_option

