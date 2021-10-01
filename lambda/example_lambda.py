import json
import urllib3

model_server = 'http://3.250.54.137:8080/health_charges/'

# Expecting to interface to/from Lex
def lambda_handler(event, context):
    slots = event['currentIntent']['slots']

    req_customer = {'age': int(slots['age']),
                    'gender_code': int(slots['gender_code']),
                    'bmi': float(slots['bmi']),
                    'children': int(slots['children']),
                    'smoker_code': int(slots['smoker_code'])
                   }

    http = urllib3.PoolManager()

    prediction = http.request('POST',
                        model_server,
                        body = json.dumps(req_customer),
                        headers = {'Content-Type': 'application/json'},
                        retries = False)
    print(req_customer)
    
    print(prediction.data)

    response = {"dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
        "message": {
            "contentType": "PlainText",
            "content": "Health Charges Catagory is: " + str(json.loads(prediction.data)["class"]),
        }}}

    return response
