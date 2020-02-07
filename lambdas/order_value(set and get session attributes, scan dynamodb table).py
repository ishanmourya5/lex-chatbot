import json
import boto3

def lambda_handler(event, context):
    
    # CONNECT WITH DYNAMODB    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('plant_orders')
    
    # SCANNING THE TABLE
    table_scan = table.scan()

    # CHECKING FOR ORDER_NO
    order_id = ""
    
    # CASE 1 - ORDER_NO IS PROVIDED IN THE SLOT - USE THIS ORDER_NO
    if(event['currentIntent']['slots']['order_no'] != None):
        order_id = event['currentIntent']['slots']['order_no']
        
    # CASE 2 - ORDER_NO IS NOT IN THE SLOT BUT IS IN THE SESSION ATTRIBUTES - USE THIS ORDER_NO
    elif("order_no" in event['sessionAttributes']):
        order_id = event['sessionAttributes']['order_no']
        
    # CASE 3 - ORDER_NO IS NEITHER IN THE SLOT NOR IN THE SESSION ATTRIBUTES - ASK USER FOR AN ORDER_NO
    else:
        return elicit_slot("Please provide an order number.", "order_no", event, event['sessionAttributes'])
    
    
    # CHECKING FOR THE ORDER_NO IN THE DYNAMODB TABLE
    flag = False 
    value = ""
    for order in table_scan['Items']:
        if(order['order_id'] == order_id):
            flag = True
            value = order['value']
            break
    
    # ORDER_NO NOT FOUND IN DB - ASK USER FOR ANOTHER ORDER_NO
    if(not flag):
        message = "This is not a valid order number, please enter a valid order number."
        session_attributes = event['sessionAttributes']
        return elicit_slot(message, "order_no",event, session_attributes)
        
    # ORDER_NO FOUND IN THE DB - PROVIDE THE USER WITH VALUE OF THE ORDER AS FETCHED FROM DB AND ADD THIS ORDER_NO TO SESSION ATTRIBUTES
    else:
        message = "Total value of order " + order_id + " is - " + value + "$"
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
        
# FUNCTION FOR ELICIT_SLOT  - WITH SESSION ATTRIBUTES
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