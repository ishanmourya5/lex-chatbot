import json

def lambda_handler(event, context):
   
   message = "We deal in plants, flowers, pots and garden accessories."
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
