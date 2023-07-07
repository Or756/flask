from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

app = Flask(__name__)

# Retrieve the DATABASE_URL from the environment
DATABASE_URL = os.environ['DATABASE_URL']

# Configure the SQLALCHEMY_DATABASE_URI setting
app.config['DATABASE_URI'] = DATABASE_URL

db = SQLAlchemy(app)

class SalesData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(50))
    units_sold = db.Column(db.Integer)
    revenue = db.Column(db.Float)
    cost = db.Column(db.Float)
    profit = db.Column(db.Float)
    date = db.Column(db.Date)

    def __init__(self, product, units_sold, revenue, cost, profit, date):
        self.product = product
        self.units_sold = units_sold
        self.revenue = revenue
        self.cost = cost
        self.profit = profit
        self.date = date

@app.route('/webhook', methods=['POST'])
def respond():
    data = request.json
    new_data = SalesData(
        data['Product'], 
        data['Units sold'], 
        data['Revenue'], 
        data['Cost'], 
        data['Profit'], 
        datetime.datetime.strptime(data['Date'], '%m/%d/%Y')  # date string should be converted to datetime object
    )
    db.session.add(new_data)
    db.session.commit()

    return {'message': 'Data received and stored.'}, 201

# Add this at the end of your file to create tables in the database as per the models defined
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
