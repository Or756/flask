from flask import Flask, request
import datetime
import os
import psycopg2

# Initialize the Flask app
app = Flask(__name__)

# Ensure the DATABASE_URL environment variable is set
DATABASE_URL = os.environ.get('postgresql://postgres:ecA5266cG2CB62D6G43abFED6641aGb3@viaduct.proxy.rlwy.net:55714/railway')
if not DATABASE_URL:
    raise EnvironmentError('The DATABASE_URL environment variable is not set.')

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.route('/webhook', methods=['POST'])
def respond():
    try:
        data = request.json
        app.logger.info(f"Received data: {data}")

        conn = get_conn()
        cur = conn.cursor()

        date = datetime.datetime.strptime(data['date'], '%m/%d/%Y').date()

        cur.execute("""
            INSERT INTO salesdata (product, units_sold, revenue, cost, profit, date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['product'], data['units_sold'], data['revenue'], data['cost'], data['profit'], date))

        conn.commit()
        cur.close()
        conn.close()
        app.logger.info("Data inserted into database successfully")
        return {'message': 'Data received and stored.'}, 201

    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
