import json
from scraper import scrape_menufy

def lambda_handler(event, context):
    """
    AWS Lambda entry point for scraping Menufy data.
    """
    # Extract the URL from the event payload
    url = event.get("url")
    if not url:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "URL is required in the request"})
        }
    
    try:
        # Scrape the data from the given URL
        data = scrape_menufy(url)
        if not data:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "No data found at the provided URL"})
            }
        
        return {
            "statusCode": 200,
            "body": json.dumps(data)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
