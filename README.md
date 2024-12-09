
# Menufy Scraper

A Python-based web scraper that extracts restaurant and menu data from Menufy order URLs. The extracted data includes restaurant name, address, geographic location, cuisines, and menu items (with details like name, price, description, and image URL).

---

## Features

- Scrapes restaurant information and menu data from a given Menufy order URL.
- Handles errors gracefully, with logs stored in an `error.log` file.
- Outputs data in JSON format.
- Includes unit tests for validating functionality.
- AWS Lambda compatible for serverless deployments.

---

## Requirements

- Python 3.8 or higher
- Libraries: `requests`, `beautifulsoup4`

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd menufy_scraper
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Run the Scraper Locally

To run the scraper locally, execute the following command:

```bash
python3 scraper.py --url <MENUFY_URL> --output <OUTPUT_JSON>
```

**Example:**

```bash
python3 scraper.py --url https://coralspring.kuboasianstreetfood.com/ --output output.json
```

This will scrape the data and save it to `output.json`.

---

### Run Locally for AWS Lambda Simulation

To test the Lambda handler locally, use the provided test script:

1. Create a test event JSON:
   ```json
   {
     "url": "https://coralspring.kuboasianstreetfood.com/"
   }
   ```

2. Run the local test script:
   ```bash
   python3 test_lambda_local.py
   ```

---

## Deploy to AWS Lambda

1. **Prepare the Deployment Package**
   - Install dependencies locally in a `package` folder:
     ```bash
     pip install -r requirements.txt -t ./package
     ```
   - Add the scraper files to the package:
     ```bash
     cp scraper.py lambda_function.py ./package
     ```
   - Create a deployment ZIP file:
     ```bash
     cd package
     zip -r ../deployment.zip .
     cd ..
     ```

2. **Upload to AWS Lambda**
   - Navigate to the [AWS Lambda Console](https://console.aws.amazon.com/lambda).
   - Create a new Lambda function with Python 3.8 runtime.
   - Upload the `deployment.zip` file.
   - Set the handler to `lambda_function.lambda_handler`.

3. **Test the Lambda Function**
   - Use the following test payload in the Lambda console:
     ```json
     {
       "url": "https://coralspring.kuboasianstreetfood.com/"
     }
     ```

4. **Invoke via AWS CLI**
   - You can invoke the Lambda function using the AWS CLI:
     ```bash
     aws lambda invoke          --function-name MenufyScraper          --payload '{"url": "https://coralspring.kuboasianstreetfood.com/"}'          response.json
     ```

---

### Output Format

The scraper outputs a JSON file in the following format:

```json
{
    "restaurant": {
        "name": "Restaurant Name",
        "address": "123 Main St",
        "locality": "City",
        "region": "State",
        "postal_code": "12345",
        "country": "Country",
        "geo": {
            "latitude": "12.34",
            "longitude": "56.78"
        },
        "cuisines": ["Cuisine1", "Cuisine2"]
    },
    "menu": [
        {
            "category": "Category Name",
            "items": [
                {
                    "id": "12345",
                    "name": "Item Name",
                    "description": "Item Description",
                    "price": 9.99,
                    "image_url": "https://example.com/image.png"
                }
            ]
        }
    ]
}
```

---

## Run Tests

To run the unit tests, execute:

```bash
python3 -m unittest test_scraper.py
```

---

## Error Handling

- Errors encountered during execution are logged to `error.log`.
- Common issues like missing elements or invalid URLs are handled gracefully.

---

## Dependencies

The required libraries are listed in `requirements.txt`:

```
requests
beautifulsoup4
```

Install them using:

```bash
pip install -r requirements.txt
```

---
