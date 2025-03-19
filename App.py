import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import mysql.connector
import pymysql

# tab1,tab2 = st.tabs(['Given Query','Created Query'])
st.title("   Order Details Analysis  ")
input = st.sidebar.selectbox('Query', ["Top 10 highest revenue generating products",
                  'Top 5 cities with the highest profit margins',
                  'The total discount given for each category',
                  'The average sale price per product category',
                  'The region with the highest average sale price',
                  'The total profit per category',
                  'The top 3 segments with the highest quantity of orders',
                  'The average discount percentage given per region',
                  'The product category with the highest total profit',
                  'The total revenue generated per year',
                  'The top 5 sub catogery with highest quantity of orders',
                  'The top 5 cities with the highest sales',
                  'The top 3 sub category having profit greater than total average',
                  'The 2 least revenue generating cities',
                  'The order count for the 10 products having no profit',
                  'The top 5 postal code with average discount percentage',
                  'The top 5 postal code with products having more profit',
                  'The products with top 2 ship_modes',
                  'The ship_modes with higher profits',
                  'The top 3 products having more availablity']
                  )


details = {'Top 10 highest revenue generating products':"""SELECT product_id, SUM(quantity * sale_price) as total_revenue 
             FROM products GROUP BY product_id ORDER BY total_revenue DESC LIMIT 10""",
         'Top 5 cities with the highest profit margins':"""SELECT o.city,p.profit AS profit_margin
  FROM orders o JOIN products p ON o.order_id = p.order_id
             order by profit_margin desc limit 5""",
         'The total discount given for each category':"""SELECT o.category, SUM(p.discount) AS total_discount
        FROM orders o JOIN products p ON o.order_id = p.order_id GROUP BY o.category order by total_discount""",
        'The average sale price per product category' : """SELECT o.category, AVG(p.sale_price) AS average_sale_price
        FROM orders o JOIN products p ON o.order_id = p.order_id GROUP BY o.category order by average_sale_price""",
        'The region with the highest average sale price' : """SELECT o.region, AVG(p.sale_price) AS average_sale_price
        FROM orders o JOIN products p ON o.order_id = p.order_id GROUP BY o.region order by average_sale_price""",
         'The total profit per category':"""SELECT o.category, sum(p.profit) AS Total_profit
        FROM orders o JOIN products p ON o.order_id = p.order_id  GROUP BY o.category order by Total_profit""",
        'The top 3 segments with the highest quantity of orders' : """SELECT o.segment, sum(p.quantity) AS Quantity
        FROM orders o JOIN products p ON o.order_id = p.order_id GROUP BY o.segment order by Quantity desc limit 3""",
        'The average discount percentage given per region' : """SELECT o.region, avg(p.discount) AS Discount
        FROM orders o JOIN products p ON o.order_id = p.order_id GROUP BY o.region order by Discount desc""",
        'The product category with the highest total profit' : """SELECT o.category, sum(p.profit) AS Profit
        FROM orders o JOIN products p ON o.order_id = p.order_id GROUP BY o.category order by Profit desc limit 1""",
        'The total revenue generated per year' : """SELECT Year(STR_TO_DATE(TRIM(o.order_date), '%m/%d/%Y')) AS Year, ROUND(SUM(p.quantity * p.sale_price),2) AS Total_Revenue
        FROM orders o Join products p ON o.order_id = p.order_id group by Year order by Total_Revenue desc""",
        'The top 5 sub catogery with highest quantity of orders' : """SELECT o.sub_category, SUM(p.quantity) AS Quantity
        from orders o Join products p ON o.order_id = p.order_id group  by sub_category order by Quantity desc limit 5""",
        'The top 5 cities with the highest sales' : """SELECT o.city, ROUND(SUM(p.quantity * p.sale_price),2) AS Revenue
        from orders o Join products p ON o.order_id = p.order_id group by city order by Revenue desc limit 5""",
        'The top 3 sub category having profit greater than total average' : """SELECT o.sub_category, SUM(p.profit) AS total_profit
        FROM orders o join products p on o.order_id = p.order_id GROUP BY sub_category HAVING SUM(p.profit) > (AVG(p.profit))
        ORDER BY total_profit DESC LIMIT 3""",
        'The 2 least revenue generating cities' : """SELECT o.city, Round(SUM(p.quantity * p.sale_price),2) as total_revenue 
        FROM orders o join products p GROUP BY o.city Having total_revenue>0 ORDER BY total_revenue ASC LIMIT 2""",
        'The order count for the 10 products having no profit' : """SELECT product_id, COUNT(*) AS count
        FROM products WHERE profit = 0 or profit <0 GROUP BY product_id order by count desc limit 10""",
        'The top 5 postal code with average discount percentage' : """select o.postal_code, AVG(p.discount_percent) as Discount_percent
        from orders o Join products p on o.order_id = p.order_id Group by postal_code order by Discount_percent desc limit 5""",
        'The top 5 postal code with products having more profit' : """select o.postal_code, sum(p.profit) as Profit
        from orders o Join products p on o.order_id = p.order_id Group by postal_code order by Profit desc limit 5""",
        'The products with top 2 ship_modes' : """select o.ship_mode, count(*) As Count
        from orders o Join products p on o.order_id = p.order_id Group by o.ship_mode order by Count desc limit 2""",
        'The ship_modes with higher profits' : """select o.ship_mode, Avg(p.profit) As Profit
        from orders o Join products p on o.order_id = p.order_id Group by o.ship_mode having o.ship_mode!='Not Available' order by Profit desc limit 2""",
        'The top 3 products having more availablity' : """select p.product_id, count(*) As Availability
        from orders o Join products p on o.order_id = p.order_id Group by o.postal_code order by Availability desc limit 3"""
        }

query_sql = details[input]

mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database='Order_Details',
        autocommit = True)
mycursor = mydb.cursor()
mycursor.execute(query_sql)
result = mycursor.fetchall()
df = pd.DataFrame(result, columns=[i[0] for i in mycursor.description])

st.table(df)  # Display the DataFrame as a table
column_names = list(df.columns)

fig, ax = plt.subplots()
ax.plot(df[column_names[0]], df[column_names[1]])
ax.set_xlabel(column_names[0])
ax.set_ylabel(column_names[1])
ax.set_title(f"Chart based on Query: {input}")
st.pyplot(fig)