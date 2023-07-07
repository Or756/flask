from flask import Flask, request
import os
import psycopg2
from urllib.parse import urlparse
import datetime

app = Flask(__name__)

def get_conn():
    result = urlparse(os.getenv("DATABASE_URL"))
    database = result.path[1:]
    hostname = result.hostname
    conn = psycopg2.connect(
        database = database,
        host = hostname
    )
    return conn

@app.route('/webhook', methods=['POST'])
def respond():
    data = request.json
    conn = get_conn()
    cur = conn.cursor()

    date = datetime.datetime.strptime(data['date'], '%m/%d/%Y').date()  # date string should be converted to date object

    cur.execute("""
        INSERT INTO salesdata (product, units_sold, revenue, cost, profit, date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data['product'], data['units_sold'], data['revenue'], data['cost'], data['profit'], date))

    conn.commit()
    cur.close()
    conn.close()

    return {'message': 'Data received and stored.'}, 201

if __name__ == '__main__':
    app.run(debug=True)
