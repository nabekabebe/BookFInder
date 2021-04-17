from flask_restplus import Api

API = Api(
    title="Book API",
    version='1.0',
    description="This Api provides endpoint for accessing books and their reviews."
)
