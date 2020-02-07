import json
import boto3

def lambda_handler(event, context):
    
    # SLOT - PLANT NAME
    plant_name = event['currentIntent']['slots']['plant_name']
    
    # CONNECT WITH DYNAMO DB    
    dynamodb = boto3.resource('dynamodb')
    
    # SPECIFY OUR TABLE NAME FROM DYNAMODB
    table = dynamodb.Table('plant_prices')
    
    # SCANNING THE TABLE
    table_scan = table.scan()
    print(table_scan)
    
    # CHECKING FOR THE REQUIRED PLANT NAME IN THE TABLE SCAN RESULT 
    price = 0
    flag = False
    for plant in table_scan['Items']:
        if(plant['plant_name'] == plant_name):
            price = plant['price']
            flag = True
            break
    
    # PLANT NOT FOUND
    if(not flag):
        message = plant_name + " is not available with us, please search for another plant."
        return elicit_slot(message, "plant_name", event)
        
    # PLANT FOUND
    else:
        message = "Price for " + plant_name + " is " + price + "$"
        return close_intent(message)

# FUNCTION FOR CLOSE INTENT
def close_intent(message):
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": message
            }
        }
    }
    return response
        
# FUNCTION FOR ELICIT_SLOT
def elicit_slot(message, slot_name, event):
    response = {
        "dialogAction": {
            "type": "ElicitSlot",
            "message": {
                "contentType": "PlainText",
                "content": message
            },
            "intentName": event['currentIntent']['name'],
            "slots": event['currentIntent']['slots'],
            "slotToElicit" : slot_name
        }
    }
    return response 