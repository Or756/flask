@app.route('/webhook', methods=['POST'])
def respond():
    try:
        data = request.json
        app.logger.info(f"Received data: {data}")

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

        app.logger.info("Data inserted into database successfully")

        return {'message': 'Data received and stored.'}, 201
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        raise
