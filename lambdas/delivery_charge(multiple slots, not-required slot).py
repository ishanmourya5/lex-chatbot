import json

def lambda_handler(event, context):
    
    # SLOT - PINCODE 
    pin_code = event['currentIntent']['slots']['pincode']
    # PINCODE VALIDATION
    if(len(pin_code)!=6):
        return elicit_slot("Invalid pincode, please enter a 6 digit pincode", "pincode", event)
    
    # SLOT - AMOUNT_OF_ORDER
    # CHECKING IF THE SLOT IS EMPTY CAUSE THIS HAS NOT BENN SET AS A REQUIRED SLOT IN LEX CONSOLE
    if(event['currentIntent']['slots']['amount_of_order'] == None):
        return elicit_slot("Please enter the approximate amount of order.", "amount_of_order", event)
    amount_of_order = event['currentIntent']['slots']['amount_of_order']
    
    # FORMING OUTPUT BASED ON SLOT VALUE
    if(int(amount_of_order)<100):
        return close_intent("Delivery charges - 5$.")
    else:
        return close_intent("You will get free delivery.")

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