import time
import mariadb


def measure_query_time(conn_params, query, iterations=1000):
    conn = mariadb.connect(**conn_params)
    cur = conn.cursor()
    times = []
    for _ in range(iterations):
        start = time.time()
        cur.execute(query)
        cur.fetchall()
        end = time.time()
        times.append(end - start)
    cur.close()
    conn.close()
    avg_time = sum(times) / len(times)
    return avg_time


if __name__ == "__main__":
    conn_params = {
        "user": "admin",
        "password": "admin",
        "host": "localhost",
        "port": 3306,
        "database": "shop"
    }
    query = "SELECT id FROM product WHERE id > 100 LIMIT 1"
    avg = measure_query_time(conn_params, query, iterations=1000)
    print(f"Average execution time over 1000 runs: {avg:.6f} seconds")
    print(f"Average time for 1 query: {avg/1000:.8f} seconds")
