import json
from lambda_function import lambda_handler

def test_lambda_handler():
    # Simulate an event with the Menufy URL
    event = {
        "url": "https://coralspring.kuboasianstreetfood.com/"
    }

    # Simulate the context (not used in this function, can be empty)
    context = {}

    # Call the Lambda handler function
    response = lambda_handler(event, context)
    
    # Print the response for verification
    print("Status Code:", response["statusCode"])
    print("Response Body:", json.dumps(json.loads(response["body"]), indent=4))

if __name__ == "__main__":
    test_lambda_handler()
