import boto3
import pytest
import os
from lambda_function import lambda_handler

# Point to AWS if testing live (or to moto if mocking)
os.environ['TABLE_NAME'] = 'Users'

# Sample valid event
valid_event = {
    "first_name": "Jan",
    "last_name": "Kowalski",
    "email": "jan.kowalski@example.com"
}

# Sample invalid event (missing email)
invalid_event = {
    "first_name": "Jan",
    "last_name": "Kowalski"
}

def test_lambda_with_valid_input():
    response = lambda_function.lambda_handler(valid_event, None)
    assert response["statusCode"] == 200
    assert "inserted successfully" in response["body"]

def test_lambda_missing_email():
    response = lambda_function.lambda_handler(invalid_event, None)
    assert response["statusCode"] == 400
    assert "email is required" in response["body"]

