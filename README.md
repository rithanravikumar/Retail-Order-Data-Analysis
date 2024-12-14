# Retail-Order-Data-Analysis

Retail order data analysis involves examining and interpreting data related to customer orders in a retail environment. The goal is to uncover patterns, trends, and insights to optimize business operations, enhance customer satisfaction, and boost profitability.

### APP LINK: (https://retail-order-data-analysis-nxh56ghavw6q58ppjcaw43.streamlit.app)

## Columns:
1. order_id: Unique identifier for each order (integer).
2. order_date: Date of the order (datetime-like string).
3. ship_mode: Shipping method (e.g., "Second Class", "Standard Class")—some missing values.
4. segment: Customer segment (e.g., "Consumer", "Corporate").
5. country: Country of the order (all entries seem to be "United States").
6. city: City where the order was placed.
7. state: State where the order was placed.
8. postal_code: Postal code of the delivery location (integer).
9. region: Region in the country (e.g., "South", "West").
10. category: Product category (e.g., "Furniture", "Office Supplies").
11. sub_category: Sub-category of the product.
12. product_id: Unique identifier for the product.
13. cost_price: Cost price of the product.
14. list_price: Listed price of the product.
15. quantity: Quantity of items ordered.
16. discount_percent: Discount percentage applied to the order.
17. discount_price: Discount amount in dollars.
18. sale_price: Final price after discount.
19. profit: Profit made from the sale.
20. year: Year of the order.
21. month: Month of the order.

## Work Flow:

1. Imported the data from the Kaggle .json file and unzipped it.
2. Converted the data into a pandas DataFrame for analysis.
3. Performed data cleaning to ensure consistency and accuracy.
4. Visualized the cleaned data using plotly.express for better insights.
5. Pushed the data to a PostgreSQL database hosted on an AWS server, using sqlalchemy and psycopg2-binary.
6. Created two tables in PostgreSQL: Product Data and Order Data, and inserted the respective data.
7. Solved queries to extract meaningful insights from the database.
8. Developed a Streamlit app using Visual Studio Code, integrating analysis results and connecting it to a GitHub repository.
9. Successfully launched the Streamlit app based on the analysis.
