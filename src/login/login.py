import boto3
import base64
import hashlib
import hmac
import os
import json

def get_secret_hash(username, client_id, client_secret):
    msg = username + client_id
    dig = hmac.new(client_secret.encode(), msg.encode(), hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

def handler(event, context):
    body = json.loads(event.get('body', '{}'))
    username = body['username']
    password = body['password']

    client_id = os.environ['COGNITO_CLIENT_ID']
    client_secret = os.environ['COGNITO_CLIENT_SECRET']
    region = os.environ.get('AWS_REGION', 'us-east-1')

    client = boto3.client('cognito-idp', region_name=region)

    try:
        resp = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
                'SECRET_HASH': get_secret_hash(username, client_id, client_secret)
            },
            ClientId=client_id
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "id_token": resp['AuthenticationResult']['IdToken'],
                "access_token": resp['AuthenticationResult']['AccessToken'],
                "expires_in": resp['AuthenticationResult']['ExpiresIn']
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except client.exceptions.NotAuthorizedException:
        return {"statusCode": 401, "body": json.dumps({"message": "Invalid credentials"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
