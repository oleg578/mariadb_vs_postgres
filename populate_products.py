import sys
import random
import string
import re
try:
    import psycopg2
    from psycopg2.extras import execute_batch
except ImportError:
    psycopg2 = None
    execute_batch = None
try:
    import mysql.connector
except ImportError:
    mysql = None


def random_name(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def main(dsn):
    if dsn.startswith("mysql://"):
        if mysql is None:
            print("mysql-connector-python is required for MariaDB/MySQL support. Install with 'pip install mysql-connector-python'.")
            sys.exit(1)
        match = re.match(r"mysql://(.*?):(.*?)@(.*?):(\d+)/(.*)", dsn)
        if not match:
            print("Invalid MySQL DSN format.")
            sys.exit(1)
        user, password, host, port, db = match.groups()
        conn = mysql.connector.connect(
            user=user, password=password, host=host, port=port, database=db)
        cur = conn.cursor()
        insert_sql = "INSERT INTO product (name, price, quantity) VALUES (%s, %s, %s)"
        db_type = "mysql"
    else:
        if psycopg2 is None:
            print(
                "psycopg2 is required for PostgreSQL support. Install with 'pip install psycopg2'.")
            sys.exit(1)
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()
        insert_sql = "INSERT INTO product (name, price, quantity) VALUES (%s, %s, %s)"
        db_type = "postgres"
    def batch_insert(cur, sql, data):
        if db_type == "mysql":
            return cur.executemany(sql, data)
        else:
            if execute_batch is None:
                print("psycopg2 is required for batch inserts in PostgreSQL. Install with 'pip install psycopg2'.")
                sys.exit(1)
            return execute_batch(cur, sql, data)
    products = []
    for _ in range(10_000_000):
        name = random_name(10)
        price = round(random.uniform(1, 1000), 2)
        quantity = random.randint(1, 100)
        products.append((name, price, quantity))
        if len(products) == 10000:
            batch_insert(cur, insert_sql, products)
            conn.commit()
            products = []
    if products:
        batch_insert(cur, insert_sql, products)
        conn.commit()
    cur.close()
    conn.close()


# DSN examples for docker containers in this project:
# PostgreSQL: "dbname=shop user=admin password=admin host=localhost port=5432"
# MariaDB:   "mysql://admin:admin@localhost:3306/shop"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python populate_products.py <DSN>\n"
              "DSN examples for docker containers in this project:\n"
              "PostgreSQL: 'dbname=shop user=admin password=admin host=localhost port=5432'\n"
              "MariaDB:   'mysql://admin:admin@localhost:3306/shop'")
        sys.exit(1)
    main(sys.argv[1])
