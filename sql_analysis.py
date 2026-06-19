import pandas as pd
import sqlite3
import random
from datetime import datetime, timedelta

def create_sample_data():
    products = ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse', 'Printer', 'Speaker']
    categories = ['Electronics', 'Accessories', 'Peripherals', 'Audio']
    customers = [f'Customer_{i}' for i in range(1, 21)]
    
    data = []
    for i in range(1, 101):
        order = {
            'order_id': i,
            'customer_name': random.choice(customers),
            'product': random.choice(products),
            'category': random.choice(categories),
            'quantity': random.randint(1, 5),
            'price': round(random.uniform(10, 500), 2),
            'order_date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
            'status': random.choice(['Delivered', 'Shipped', 'Pending', 'Cancelled'])
        }
        data.append(order)
    
    return pd.DataFrame(data)

def create_database(df):
    conn = sqlite3.connect(':memory:')
    df.to_sql('orders', conn, index=False, if_exists='replace')
    return conn

def run_query(conn, query, description):
    print(f"\n📋 {description}")
    print("-" * 50)
    print(f"SQL: {query}")
    print("-" * 50)
    
    result = pd.read_sql_query(query, conn)
    print(result)
    print("-" * 50)
    
    return result

def main():
    print("\n" + "=" * 60)
    print("   SQL DATA ANALYSIS")
    print("=" * 60)

    print("\n[1] Creating Sample Dataset...")
    df = create_sample_data()
    conn = create_database(df)
    
    print(f"✅ {len(df)} orders loaded into database")
    print(f"   Columns: {', '.join(df.columns)}")

    print("\n[2] Running SQL Queries...")

    run_query(conn, 
        "SELECT * FROM orders LIMIT 5",
        "SELECT - View first 5 rows"
    )

    run_query(conn,
        "SELECT * FROM orders WHERE status = 'Delivered'",
        "WHERE - Filter delivered orders"
    )

    run_query(conn,
        "SELECT * FROM orders WHERE price > 200 ORDER BY price DESC",
        "ORDER BY - Filter expensive items (price > 200)"
    )

    run_query(conn,
        "SELECT category, COUNT(*) as total_orders, SUM(quantity) as total_items, AVG(price) as avg_price " +
        "FROM orders GROUP BY category",
        "GROUP BY - Category summary (count, sum, avg)"
    )

    run_query(conn,
        "SELECT customer_name, COUNT(*) as orders, SUM(quantity * price) as total_spent " +
        "FROM orders GROUP BY customer_name ORDER BY total_spent DESC LIMIT 5",
        "GROUP BY - Top 5 customers by spending"
    )

    run_query(conn,
        "SELECT product, COUNT(*) as times_ordered, SUM(quantity) as total_quantity, AVG(price) as avg_price " +
        "FROM orders GROUP BY product ORDER BY total_quantity DESC LIMIT 5",
        "GROUP BY - Top 5 products by quantity sold"
    )

    run_query(conn,
        "SELECT status, COUNT(*) as count, AVG(price) as avg_price " +
        "FROM orders GROUP BY status",
        "GROUP BY - Order status summary"
    )

    run_query(conn,
        "SELECT customer_name, COUNT(*) as orders, SUM(quantity * price) as total_spent " +
        "FROM orders GROUP BY customer_name HAVING total_spent > 500",
        "HAVING - Customers with total spending > 500"
    )

    run_query(conn,
        "SELECT strftime('%Y-%m', order_date) as month, COUNT(*) as orders, SUM(quantity * price) as revenue " +
        "FROM orders GROUP BY month ORDER BY month",
        "GROUP BY - Monthly order trends"
    )

    print("\n[3] Advanced Analysis:")
    print("-" * 50)
    
    total_revenue = run_query(conn,
        "SELECT SUM(quantity * price) as total_revenue FROM orders",
        "Total Revenue"
    )
    
    avg_order_value = run_query(conn,
        "SELECT AVG(quantity * price) as avg_order_value FROM orders",
        "Average Order Value"
    )
    
    top_product = run_query(conn,
        "SELECT product, SUM(quantity * price) as revenue FROM orders " +
        "GROUP BY product ORDER BY revenue DESC LIMIT 1",
        "Top Product by Revenue"
    )

    conn.close()

    print("\n" + "=" * 60)
    print("   SQL ANALYSIS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()