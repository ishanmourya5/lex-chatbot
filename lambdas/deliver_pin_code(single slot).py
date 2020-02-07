import json

def lambda_handler(event, context):
    
    # SLOT - PIN_CODE 
    pin_code = event['currentIntent']['slots']['pincode']
    
    # VALIDATING PIN_CODE - CHECKING IF THE PIN_CODE IS VALID, I.E.- IT'S HAVING 6 DIGITS
    if(len(pin_code)!=6):
        message = "Its an invalid pincode, please enter a pincode of 6 digits."
        slot_name = "pincode"
        
        # FORMING JSON TO BE SENT AS RESPONSE TO LEX
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
    
    # FORMING RESULT ON THE BASIS OF VALUE OF PIN_CODE
    # CASE 1 - PIN_CODE STARTS WITH '8'
    if(pin_code[0] == '8'):
        message = "Yes we can deliver to " + pin_code
    
    # CASE 2 - PIN_CODE DOESN'T START WITH '8' 
    else:
        message = "Sorry, we can't deliver to " + pin_code
    
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
