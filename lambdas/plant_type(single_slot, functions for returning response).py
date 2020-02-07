import json

def lambda_handler(event, context):
    
    # SLOT - PLANT_TYPE
    plant_type = event['currentIntent']['slots']['type_of_plant']
    
    # FORMING OUTPUT BASED ON PLANT_TYPE
    if(plant_type == "indoor"):
        # INDOOR
        message = "You can buy an eradium or a cactus."
        return close_intent(message)
    else:
        # OUTDOOR
        message = "You can buy a palm or any flowering plant."
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