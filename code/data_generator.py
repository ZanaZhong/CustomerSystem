import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import random

# MariaDB connection configuration
db_config = {
    "host": "localhost",
    "user": "test",
    "password": "test",
    "database": "pretest",
}

def initialize_tables(cursor):
    """Create the necessary tables if they don't exist."""
    customers_table = """
    CREATE TABLE IF NOT EXISTS customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        created_at DATETIME NOT NULL
    );
    """
    transactions_table = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        transaction_date DATETIME NOT NULL,
        borrow_fee INT NOT NULL,
        transaction_count INT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    );
    """
    cursor.execute(customers_table)
    cursor.execute(transactions_table)
    print("Tables initialized (if they didn't exist).")

def random_date(start_date, end_date):
    """Generate a random date within a range."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def create_customers(cursor, count=1000):
    """Insert random customer data."""
    for i in range(count):
        name = f"Customer{i+1}"
        email = f"customer{i+1}@example.com"
        created_at = random_date(datetime.now() - timedelta(days=365*2), datetime.now())
        cursor.execute(
            "INSERT IGNORE INTO customers (name, email, created_at) VALUES (%s, %s, %s)",
            (name, email, created_at.strftime('%Y-%m-%d %H:%M:%S')),
        )

# def create_transactions(cursor, count=5000):
#     """Insert random transaction data."""
#     cursor.execute("SELECT id, created_at FROM customers")
#     customers = cursor.fetchall()
#     customer_transaction_count = {} 
    
#     for _ in range(count):
#         customer = random.choice(customers)
#         # get customer id & create date
#         customer_id = customer[0]
#         customer_created_at = customer[1]
#         amount = round(random.uniform(10, 1000), 2)
#         borrow_fee = amount * (round(random.uniform(0, 1), 2))

#         # transaction_date after account's create date & within 18 months
#         max_transaction_date = min(customer_created_at + timedelta(days=18*30), datetime.now())
#         transaction_date = random_date(customer_created_at, max_transaction_date)

#         # count customer transaction's times
#         if customer_id not in customer_transaction_count:
#             customer_transaction_count[customer_id] = 0
#         customer_transaction_count[customer_id] += 1
#         transaction_count = customer_transaction_count[customer_id]


#         cursor.execute(
#             """
#             INSERT INTO transactions1 (customer_id, amount, transaction_date, borrow_fee, transaction_count)
#             VALUES (%s, %s, %s, %s, %s)
#             """,
#             (customer_id, amount, transaction_date.strftime('%Y-%m-%d %H:%M:%S'), borrow_fee, transaction_count)
#         )

def create_transactions(cursor, count=5000):
    """Insert random transaction data."""
    cursor.execute("SELECT id, created_at FROM customers")
    customers = cursor.fetchall()
    
    transactions = []  # List to store all the generated transactions
    
    # Generate transactions for each customer
    for _ in range(count):
        customer = random.choice(customers)
        # get customer id & create date
        customer_id = customer[0]
        customer_created_at = customer[1]
        amount = round(random.uniform(10, 1000), 2)
        borrow_fee = amount * (round(random.uniform(0, 1), 2))

        # transaction_date after account's create date & within 18 months
        max_transaction_date = min(customer_created_at + timedelta(days=18*30), datetime.now())
        transaction_date = random_date(customer_created_at, max_transaction_date)
        
        transactions.append({
            "customer_id": customer_id,
            "amount": amount,
            "borrow_fee": borrow_fee,
            "transaction_date": transaction_date
        })
    
    # Sort transactions by transaction_date (chronological order)
    transactions.sort(key=lambda x: x["transaction_date"])

    # Calculate the transaction_count for each customer (based on the sorted transaction dates)
    transaction_counts = {}
    for tx in transactions:
        customer_id = tx["customer_id"]
        if customer_id not in transaction_counts:
            transaction_counts[customer_id] = 0
        transaction_counts[customer_id] += 1
        # transaction_counts = transaction_counts[customer_id]
        tx["transaction_count"] = transaction_counts[customer_id]

    # Insert sorted transactions into the database
    for tx in transactions:
        # print(tx)
        cursor.execute(
            """
            INSERT INTO transactions (customer_id, amount, borrow_fee, transaction_date, transaction_count)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                tx["customer_id"], 
                tx["amount"], 
                tx["borrow_fee"],
                tx["transaction_date"].strftime('%Y-%m-%d %H:%M:%S'),
                tx["transaction_count"]
            )
        )

def main():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Initialize tables
        initialize_tables(cursor)

        # Generate customer data
        print("Generating customers...")
        create_customers(cursor)

        # Generate transaction data
        print("Generating transactions...")
        create_transactions(cursor)

        # Commit changes
        connection.commit()
        print("Data generation completed successfully!")
    except Error as e:
        print(f"Error: {e}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    main()
