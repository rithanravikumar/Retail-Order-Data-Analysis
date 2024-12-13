import pandas as pd;
import streamlit as st
import pg8000



SQL_queries = {
    "Guvi Queries": [
        {"query_name": "Top 10 Highest Revenue Generating Products","query": """
        select p.product_id,p.sub_category,round(sum(o.sale_price::numeric * o.quantity::numeric),2) as revenue 
        from product_data p join order_data o 
        on p.product_id=o.product_id group by p.product_id order by revenue desc limit 10;
    """},
    {"query_name": "Top 5 Cities with the Highest Profit Margins","query": """
        select city,avg(case when sale_price = 0 then 0 else ((profit/sale_price)*100) end)
        as profit_margin from order_data group by city order by profit_margin desc limit 5;
    """},
    {"query_name":"Total Discount Given for Each Category","query": """
        select p.category,sum(o.discount_price) as total_discount from product_data p 
        join order_data o on p.product_id=o.product_id group by p.category;
    """},
    {"query_name":"Find the average sale price per product category","query": """
        select p.category,avg(o.sale_price) as Avg_saleprice from order_data o join product_data p
        on p.product_id= o.product_id group by category;
    """},
     {"query_name":"Find the region with the highest average sale price","query": """
        select region, avg(sale_price) as avg_sales from order_data group by region order by avg_sales desc limit 1;
    """},
     {"query_name":"Find the total profit per categor","query": """
        select p.category, sum(o.profit) as total_profit from product_data p join order_data o on 
        p.product_id=o.product_id group by p.category;
    """},
     {"query_name":"Identify the top 3 segments with the highest quantity of orders","query": """
         select segment, sum(quantity) as highest_quantity  from order_data group by segment 
         order by highest_quantity desc;
    """},
     {"query_name":"Determine the average discount percentage given per region","query": """
        select region, round(avg(discount_percent),2) as avg_discount from order_data group by region;
    """},
     {"query_name":"Find the product category with the highest total profit","query": """
        select p.category, round(sum(o.profit)::numeric,2) as total_profit from product_data p join order_data o 
        on p.product_id=o.product_id group by p.category order by total_profit desc limit 1;
    """},
     {"query_name":"Calculate the total revenue generated per year","query": """
        select year, round(sum(sale_price)::numeric,2) as Revenue_per_year from order_data group by year;
    """},
    ],

    "Self Queries": [
        {"query_name":"Find total sales revenue for each region","query": """
        select region, sum(sale_price * quantity) as total_revenue from order_data group by region;
    """},
    {"query_name":"Identify regions with total profits greater than $50,000","query": """
        select region, sum(profit*quantity) as total_profit from order_data group by region
        having sum(profit*quantity) >50000;
    """},
    {"query_name":"Find the region with the highest number of orders","query": """
        select region, count(order_id) as order_count
        from order_data group by region
        order by order_count desc limit 1;
    """},
    {"query_name":"Count the total number of orders each year","query": """
       select year, count(distinct order_id) as total_orders from order_data group by year;
    """},
     {"query_name":"Count unique products in each category","query": """
        select category, count(distinct product_id) as unique_products from product_data group by category;
    """},
     {"query_name":"List top 3 states with the most orders","query": """
        select state, count(distinct order_id) as total_orders from order_data group by state order by total_orders desc limit 3;
    """},
     {"query_name":"List regions with negative profit products","query": """
        select region from order_data where profit < 0 group by region;
    """},
     {"query_name":"Determine the most frequently ordered product","query": """
        select p.product_id,p.sub_category, count(distinct o.order_id) as order_frequency from product_data p join order_data o 
        on p.product_id=o.product_id group by p.product_id order by order_frequency desc limit 1;
    """},
     {"query_name":"Identify cities with profits exceeding $10,000","query": """
        select city, sum(profit) as total_profit 
        from order_data group by city having sum(profit) > 10000 order by total_profit desc ;
    """},
     {"query_name":"Identify top 5 sub categories with the most products sold","query": """
       select p.sub_category, sum(o.quantity) as total_quantity from product_data p join order_data o on p.product_id=o.product_id
       group by p.sub_category order by total_quantity desc limit 5;
    """},
    ],

    "Business Insights": 
     [
      {"query_name":"Top-Selling Products","query": """
        select p.product_id,p.sub_category,sum(o.quantity*o.sale_price) as total_revenue,sum(o.quantity) as total_quantity_sold,
        rank() over(order by sum(o.quantity) desc) as rank 
        from product_data p join order_data o on p.product_id=o.product_id group by p.product_id;
    """},
    {"query_name":"Monthly Sales Analysis","query": """
        with y1 as (select month,year,sum(sale_price) as msa
        from order_data where year = 2023 group by month,year),
        y2 as (select month,year,sum(sale_price) as msa
        from order_data where year = 2022 group by month,year)

        select y1.month,(((y1.msa - y2.msa) / y2.msa) * 100) as sales_growth_rate from y1 y1 join y2 y2 on
        y1.month=y2.month and y1.year=y2.year+1 order by y1.month asc;
    """},
    {"query_name":"Product Performance","query": """
        select p.product_id,p.category,p.sub_category, round(sum(o.sale_price * o.quantity)::numeric,2)as total_revenue,
        round(sum(o.profit*o.quantity)::numeric,2) as total_profit, case when sum(o.sale_price) = 0 then 0 
        else round((sum(o.profit)/ sum(o.sale_price))*100) end as profit_margin,rank() over(order by round(sum(o.sale_price * o.quantity)::numeric,2) desc)
        from product_data p join order_data o on p.product_id=o.product_id group by p.product_id;
    """},
    {"query_name":"Regional Sales Analysis","query": """
       select region, round(count(distinct order_id)::numeric, 2) as total_order, round(sum(sale_price*quantity)::numeric,2) 
       as total_sale, round(sum(profit*quantity)::numeric,2) as total_profit,round((sum(profit)/ sum(sale_price))*100) as profit_margin,
       rank() over(order by round(sum(sale_price* quantity)::numeric,2) desc) from order_data group by region;
    """},
     {"query_name":"Discount Analysis","query":"""
        select product_id,sum(quantity) as total_quantity,sum(discount_percent) as total_disc_percent,
        round(sum(discount_price)::numeric,2) as total_discount,
        round(sum(sale_price)::numeric,2) as total_sale, round((sum(discount_price)::numeric/
        sum(sale_price)::numeric)* 100,2) as impacted_discount_percentage from order_data 
        group by product_id having sum(discount_percent)>20 order by impacted_discount_percentage desc;
    """}, 
]
}

# Database connection
def get_connection():
    conn = pg8000.connect(
        host = "dsrithandb.czqo46sewhyn.ap-south-1.rds.amazonaws.com",
        user = "postgres",
        password = "Awsrootroot",
        database = "retail_order",        
    )
    return conn

# Page title
st.title("SQL Query Runner - Retail Order Data Analysis")

# Sidebar for categories
selected_category = st.sidebar.selectbox("Select Query Category:", list(SQL_queries.keys()))

# Show queries in the selected category

queries = SQL_queries[selected_category]

for idx, query in enumerate(queries, start=1):
    # Display the query question
    st.markdown(f"**Query {idx}: {query['query_name']}**")  # Display the question

    # Button to run the query
    if st.button(f"Run Query {idx}"):
        try:
            # Connect to the database and execute the query
            conn = get_connection()
            df = pd.read_sql_query(query["query"], conn)  # Pass the query string
            conn.close()

            # Display the results as a table
            if not df.empty:
                st.dataframe(df)
            else:
                st.warning("Query returned no results.")
        except Exception as e:
            st.error(f"An error occurred while executing the query: {e}")
            
st.text("THANK YOU FOR VISITING MY SITE")
