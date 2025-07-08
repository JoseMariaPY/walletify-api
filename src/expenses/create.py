import json
import os
import uuid
from datetime import datetime
import boto3
from src.utils.common import money_data

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["EXPENSES_TABLE"])

def handler(event, context):
    try:
        # Extraer el user ID desde el token Cognito
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]
        body = json.loads(event.get("body", "{}"))
        expense_id = str(uuid.uuid4())
        money = body.get("money")
        # Validar la moneda
        if money.upper() not in [m["name"] for m in money_data]:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Moneda no válida"})
            }
        if not body.get("amount") or not isinstance(body["amount"], (int, float)):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "El campo 'amount' es obligatorio y debe ser un número"})
            }
        # Preparar el ítem para guardar en DynamoDB
        item = {
            "PK": f"USER#{user_id}",
            "SK": f"EXPENSE#{expense_id}",
            "money": money.upper(),
            "amount": body.get("amount"),
            "category_id": body.get("category_id", "CATEGORY#default"),
            "date": body.get("date", datetime.utcnow().date().isoformat()),
            "description": body.get("description", "Sin descripción")
        }
        # Guardar en DynamoDB
        table.put_item(Item=item)
        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Expense created successfully",
                "expense_id": expense_id
            })
        }
    except Exception as e:
        print("Error in create expense:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }
