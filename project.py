!pip install pymysql
import streamlit as st
import pymysql
import pandas as pd
def get_db_connection():
    return pymysql.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",   # e.g., "localhost"
        user="2UUkERace9vWJvM.root",   # e.g., "root"
        password="csTRyi9ITkoTl4XY",
        database="RAMYA",
        ssl_verify_cert=True,
        ssl_verify_identity=True,
        cursorclass=pymysql.cursors.DictCursor
    )
def execute_query(query):
    conn = get_db_connection()  # Establish connection
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()  # Fetch all results
            return pd.DataFrame(result)  # Convert to DataFrame for display
    finally:
        conn.close()  # Ensure connection is closed

# Streamlit UI
st.title("RETAIL ORDER ANALYSIS")

# Query options
query_options = {
    "Top 10 Revenue Generating Products": """
        select
           list.order_id,
           PROJECT.product_id,
           PROJECT.profit
           FROM list
           LEFT JOIN PROJECT on list.order_id = PROJECT.order_id
           ORDER BY PROJECT.profit DESC
           LIMIT 10;
    """,
    "Top 5 Revenue Generating Cities": """
        select 
          l.city,p.profit
          from list l
          join PROJECT p on l.order_id = p.order_id
          order by p.profit desc
          limit 5;
          
    """,
    "Total discount given for each category": """
        select count(*),l.category,sum(p.discount)
          from list l
          join PROJECT p on l.order_id = p.order_id
          group by l.category
    """,
    "Average sale price per product category": """
        select l.category,avg(p.sale_price)
          from list l
          right join PROJECT p on l.order_id = p.order_id
          group by l.category
    """,
    "Region with the highest average sale price": """
        select l.region,avg(p.sale_price)
          from list l
          right join PROJECT p on l.order_id = p.order_id
          group by l.region
          order by avg(p.sale_price) desc
          limit 1;
    """,
    "Total profit per category": """
        select l.category,sum(p.profit)
          from list l
          left join PROJECT p on l.order_id = p.order_id
          group by l.category
    """,
    "Top 3 segments with the highest quantity of orders": """
        select l.segment,count(*),sum(p.quantity)
          from list l
          join PROJECT p on l.order_id = p.order_id
          group by l.segment
          order by count(*) desc
          limit 3;
    """,
    "Average discount percentage given per region": """
        select l.region,avg(p.discount_percent)
          from list l
          join PROJECT p on l.order_id = p.order_id
          group by l.region
    """,
    "Product category with the highest total profit": """
        select l.category,sum(p.profit)
          from list l
          right join PROJECT p on l.order_id = p.order_id
          group by l.category
          order by sum(p.profit) desc
          limit 1;
    """,
    "Total revenue generated per year": """
         select year(order_date),sum(sale_price)
           from PROJECT
           group by year(order_date)
    """,
    "Least 10 cities with lowest profit margin": """
        select l.city,p.profit
          from list l
          join PROJECT p on l.order_id = p.order_id
          order by p.profit asc
          limit 10;
    """,
    "Region with least avg sale price": """
        select l.region,avg(p.sale_price)
          from list l
          right join PROJECT p on l.order_id = p.order_id
          group by l.region
          order by avg(p.sale_price) asc
          limit 1;
    """,
    "Identify the top 5 segments with the ship mode": """
        select l.segment,count(*),l.ship_mode
        from list l
        join PROJECT p on l.order_id = p.order_id
        group by l.segment,l.ship_mode
        order by count(*) desc 
        limit 5;
    """,
    "Product category with least total profit": """
        select l.category,sum(p.profit)
          from list l
          right join PROJECT p on l.order_id = p.order_id
          group by l.category
          order by sum(p.profit) asc
          limit 1;
    """,
    "Total loss generated per year":"""
        select year(order_date),
        sum(sale_price-cost_price) as total_loss
        from PROJECT
        group by year(order_date)
    """,
    "Top 5 states with highest profit": """
       select l.state,sum(p.profit)
         from list l
         join PROJECT p on l.order_id = p.order_id
         group by l.state
         order by sum(p.profit) desc
         limit 5
    """,
    "Least 5 states with lowest profit": """
       select l.state,sum(p.profit)
         from list l
         inner join PROJECT p on l.order_id = p.order_id
         group by l.state
         order by sum(p.profit) asc
         limit 5
    """,
    "Least 5 subcategory with lowest saleprice": """
       select l.sub_category,sum(p.sale_price)
         from list l
         join PROJECT p on l.order_id = p.order_id
         group by l.sub_category
         order by sum(sale_price) asc
         limit 5
    """,
    "Top 5 subcategory with sale price": """
       select l.sub_category,sum(p.sale_price)
         from list l
         left join PROJECT p on l.order_id = p.order_id
         group by l.sub_category
         order by sum(sale_price) desc
         limit 5
    """,
    "Total number of orders for each category": """
       select l.category,sum(p.quantity)
         from list l
         inner join PROJECT p on l.order_id = p.order_id
         group by l.category
    """,
    "Top 10 Productid based on shipmode": """
       select p.product_id,count(*),l.ship_mode
         from list l
         right join PROJECT p on l.order_id = p.order_id
         group by l.ship_mode,p.product_id
         order by count(*) desc
         limit 10
    """
        
    }

# Dropdown for query selection
selected_query = st.selectbox("Select a query:", list(query_options.keys()))

# Button to execute query
if st.button("Run Query"):
    st.write(f"### Results for: {selected_query}")
    df = execute_query(query_options[selected_query])
    st.dataframe(df)  # Display results in an interactive table
    if selected_query == "Top 10 Revenue Generating Products":
        st.bar_chart(df.set_index("product_id"))

    elif selected_query == "Top 5 Revenue Generating Cities":
        st.bar_chart(df.set_index("city"))

    elif selected_query == "Total discount given for each category":
        st.line_chart(df.set_index("category"))

    elif selected_query == "Average sale price per product category":
        st.bar_chart(df.set_index("category"))

    elif selected_query == "Region with the highest average sale price":
        st.line_chart(df.set_index("region"))

    elif selected_query == "Top 3 segments with the highest quantity of orders":
        st.line_chart(df.set_index("segment"))

    elif selected_query == "Average discount percentage given per region":
        st.bar_chart(df.set_index("region"))

    elif selected_query == "Least 10 cities with lowest profit margin":
        st.line_chart(df.set_index("city"))  

    elif selected_query == "Region with least avg sale price":
        st.bar_chart(df.set_index("region"))

    elif selected_query == "Identify the top 5 segments with the ship mode":
        st.line_chart(df.set_index("segment"))  

    elif selected_query == "Top 10 Productid based on shipmode":
        st.bar_chart(df.set_index("product_id"))

    else:
        st.write("No chart available for this query.")

