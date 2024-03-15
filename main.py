# main.py

from flask import Flask
from database.db import db_connection
from flask_restx import Api
from modules.clients.client_route import client_bp
from modules.payments.payment_route import payment_bp
from modules.products.product_route import product_bp
from modules.stores.store_route import store_bp

# Create the Flask application
app = Flask(__name__)

# Configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/design"

# Initialize the app with the database extension
db_connection.init_app(app)

# Create all database tables
with app.app_context():
    db_connection.create_all()

# Initialize Flask-Restx
api = Api(version='1.0', title='Client API', description='APIs for clients')

# Initialize the app with the API extension
api.init_app(app)

# Register the blueprints with Flask-Restx
api.add_namespace(store_bp)
api.add_namespace(product_bp)
api.add_namespace(client_bp)
api.add_namespace(payment_bp)

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
