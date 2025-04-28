import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'Users')
table = dynamodb.Table(table_name)

def is_valid_email(email):
    if '@' not in email or '.' not in email:
        return False
    try:
        local, domain = email.split('@')
        if not local or not domain:
            return False
        if '.' not in domain:
            return False
        return True
    except ValueError:
        return False
    
def lambda_handler(event, context):
    # Validate required fields
    required_fields = ['first_name', 'last_name', 'email']
    for field in required_fields:
        if field not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": f"{field} is required"})
            }
        if "email" in event:
            email = event['email']
            if not is_valid_email(email):
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "invalid email format"})
                }

    try:
        # Write to DynamoDB
        table.put_item(Item={
            'email': event['email'],
            'first_name': event['first_name'],
            'last_name': event['last_name']
        })

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "User data inserted successfully!"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

