import json
import os
import uuid
from datetime import datetime
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["EXPENSES_TABLE"])

def handler(event, context):
    try:
        # Extraer el user ID desde el token Cognito
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]

        # Parsear el body del request
        body = json.loads(event.get("body", "{}"))

        # Generar ID único para el gasto
        expense_id = str(uuid.uuid4())

        # Preparar el ítem para guardar en DynamoDB
        item = {
            "PK": f"USER#{user_id}",
            "SK": f"EXPENSE#{expense_id}",
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
                "message": "Gasto creado con éxito",
                "expense_id": expense_id
            })
        }

    except Exception as e:
        print("Error al crear gasto:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Error interno del servidor"})
        }
