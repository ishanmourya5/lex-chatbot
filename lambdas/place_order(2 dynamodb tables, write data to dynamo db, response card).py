import json
import boto3

def lambda_handler(event, context):
   
    # SLOT - PLANT_NAME
    plant_name = event['currentIntent']['slots']['plants_name']
    
    # CONNECT WITH DYNAMO DB    
    dynamodb = boto3.resource('dynamodb')
    
    # CONNECT WITH 2 DYNAMODB TABLES
    table = dynamodb.Table('plant_orders')
    table2 = dynamodb.Table('plant_prices')
    
    # SEARCHING FOR THE SIMILAR PLANT NAMES IN THE TABLE
    matching_plants = []
    table_scan = table2.scan()
    for plant in table_scan['Items']:
        if(plant_name in plant['plant_name']):
            matching_plant = {
                "text" : plant['plant_name'],
                "value" : plant['plant_name']
            }
            matching_plants.append(matching_plant)
    
    # NO MATCHING PLANT FOUND - ASK USER AGAIN FOR A PLANT NAME
    if(len(matching_plants)==0):
        return elicit_slot("No matchinh plant found, please enter another plant name", "plants_name", event)
    
    # ONLY ONE MATCHING PLANT IS FOUND - PLACE THE ORDER AND INFORM USER
    elif(len(matching_plants)==1):
        
        # ADDING ORDER DETAILS TO THE TABLE 
        item = {}
        item['order_id'] = "1234"
        item['plant_name'] = plant_name
        table.put_item(Item = item)
    
        # INFORMING USER OF THE ORDER
        message = "Your order for " + plant_name + " has been placed with order id " + item['order_id']
        return close_intent(message)
    
    # NUMBER OF MATCHING PLANTS IS >1 AND <=5 - SHOW RESPONSE CARD TO THE USER TO SELECT A PLANT NAME
    elif(len(matching_plants)<=5):
        message = "Select a plant."
        slot_name = "plants_name"
        
        # FORMING A RESPONSE CONTAINING RESPONSE CARD
        response = {
            "dialogAction": {
                "type": "ElicitSlot",
                "message": {
                    "contentType": "PlainText",
                    "content": message
                },
                "intentName": event['currentIntent']['name'],
                "slots": event['currentIntent']['slots'],
                "slotToElicit" : slot_name,
                "responseCard": {
                    "version": 1,
                    "contentType": "application/vnd.amazonaws.card.generic",
                    "genericAttachments": [
                        {
                            "title":"Plant name",
                            "subTitle":"Please select one of the following - ",
                            "imageUrl":None,
                            "attachmentLinkUrl":None,
                            "buttons":matching_plants
                        } 
                    ] 
                }
            }
        }
        return response 
    
    # NUMBER OF MATCHING PLANTS IS >5 - ASK THE USER TO PROVIDE A MORE SPECIFIC PLANT NAME 
    else:
        return elicit_slot("Lots of entries found matching with this name, please be more specific", "plants_name", event)
        
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