import unittest
from flask import Flask
from flask_restx import Api
from main import db_connection, store_bp, product_bp, client_bp, payment_bp

class TestMain(unittest.TestCase):
    def setUp(self):
        # Create a test Flask application
        self.app = Flask(__name__)

        # Configure the SQLite database for testing
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        db_connection.init_app(self.app)

        # Create a test client
        self.client = self.app.test_client()

        # Establish the application context
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Set up the test database
        with self.app_context:
            db_connection.create_all()

        # Initialize Flask-Restx
        self.api = Api(version='1.0', title='Client API', description='APIs for clients')
        self.api.init_app(self.app)

        # Register the blueprints with Flask-Restx
        self.api.add_namespace(store_bp)
        self.api.add_namespace(product_bp)
        self.api.add_namespace(client_bp)
        self.api.add_namespace(payment_bp)

    def tearDown(self):
        # Clean up the test database
        with self.app_context:
            db_connection.session.remove()
            db_connection.drop_all()

        # Pop the application context
        self.app_context.pop()

    def test_api_initialization(self):
        # Ensure that the Flask-Restx API is initialized correctly
        self.assertIsInstance(self.api, Api)

        # Ensure that all namespaces are added successfully
        self.assertIn(store_bp, self.api.namespaces)
        self.assertIn(product_bp, self.api.namespaces)
        self.assertIn(client_bp, self.api.namespaces)
        self.assertIn(payment_bp, self.api.namespaces)


if __name__ == '__main__':
    unittest.main()
