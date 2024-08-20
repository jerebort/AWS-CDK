import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Auto')

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    try:
        response = table.scan()
        autos = response.get('Items', [])
        
        #esto es para convertir los objetos Decimal en la respuesta a tipos de datos compatibles con json 
        autos = [{k: (float(v) if isinstance(v, Decimal)else v) for k, v in auto.items()}for auto in autos] 
        
        return {
            'statusCode': 200,
            'body': json.dumps(autos, default=decimal_default)
        }
    except Exception as e:
        print ("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error devolviendo los autos', 'error': str(e)})
        }
    
