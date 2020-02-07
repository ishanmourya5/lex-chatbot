import json
import boto3

def lambda_handler(event, context):
    
    # CONNECT WITH DYNAMO DB    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('plant_orders')
    
    # SCANNING THE TABLE
    table_scan = table.scan()
    
    # SLOT - ORDER_NO
    order_id = event['currentIntent']['slots']['order_no']
    
    # CHECKING FOR THE ORDER_NO IN THE DYNAMODB TABLE
    flag = False 
    status = ""
    for order in table_scan['Items']:
        if(order['order_id'] == order_id):
            flag = True
            status = order['status']
            break
        
    # ORDER_NO NOT FOUND IN DB - ASK USER FOR ANOTHER ORDER_NO
    if(not flag):
        message = "This is not a valid order number, please enter a valid order number."
        session_attributes = event['sessionAttributes']
        return elicit_slot(message, "order_no",event, session_attributes)
        
    # ORDER_NO FOUND IN THE DB - PROVIDE THE USER WITH STATUS OF THE ORDER AS FETCHED FROM DB AND ADD THIS ORDER_NO TO SESSION ATTRIBUTES
    else:
        message = "Status of order " + order_id + " is - " + status
        session_attributes = event['sessionAttributes']                         # GETTING ALREADY PRESENT SESSION ATTRIBUTES LIST FROM EVENT
        session_attributes['order_no'] = order_id                               # ADDING NEW ENTRY TO THIS LIST
        return close_intent(message, session_attributes)    
    
# FUNCTION FOR CLOSE INTENT - WITH SESSION ATTRIBUTES
def close_intent(message, session_attributes):
    response = {
        "sessionAttributes": session_attributes,
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
        
# FUNCTION FOR ELICIT_SLOT - WITH SESSION ATTRIBUTES        
def elicit_slot(message, slot_name, event, session_attributes):
    response = {
        "sessionAttributes": session_attributes,
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