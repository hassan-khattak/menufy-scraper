import argparse
import json
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
import re
import traceback


# Set the log file path
LOG_FILE = "error.log"


def log_error(error_message: str):
    """
    Logs error messages with tracebacks to a file.
    """
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{error_message}\n")
        traceback.print_exc(file=log_file)


def parse_json_ld(script_tag: str) -> Dict[str, Any]:
    """
    Parses the JSON-LD script tag for restaurant information.
    """
    try:
        json_data = json.loads(script_tag)
        return {
            "name": json_data.get("name", "Not Available"),
            "address": json_data.get("address", {}).get("streetAddress", "Not Available"),
            "locality": json_data.get("address", {}).get("addressLocality", "Not Available"),
            "region": json_data.get("address", {}).get("addressRegion", "Not Available"),
            "postal_code": json_data.get("address", {}).get("postalCode", "Not Available"),
            "country": json_data.get("address", {}).get("addressCountry", "Not Available"),
            "geo": {
                "latitude": json_data.get("geo", {}).get("latitude", "Not Available"),
                "longitude": json_data.get("geo", {}).get("longitude", "Not Available"),
            },
            "cuisines": json_data.get("servesCuisine", "Not Available"),
        }
    except Exception as e:
        log_error(f"Error parsing JSON-LD: {e}")
        return {}


def scrape_menu(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """
    Scrapes the menu items and categories.
    """
    menu_categories = []
    for category in soup.select(".category"):
        try:
            category_name = category.find("h2").get_text(strip=True) if category.find("h2") else "Unknown Category"
            items = []
            for item in category.find_all("div", class_="category-item-wrapper"):
                try:
                    price_text = item.find("div", class_="category-item-price").text.strip()
                    price = float("".join(re.findall(r"\d+\.\d+|\d+", price_text)))
                    image_div = item.find("div", class_="category-item-image lazy-background-image")
                    image_url = image_div["data-src"] if image_div and "data-src" in image_div.attrs else None
                    items.append({
                        "id": (
                            item.find("a", class_="category-item")["href"].split("/")[-2]
                            if item.find("a", class_="category-item")
                            else None
                        ),
                        "name": item.find("div", class_="category-item-name").text.strip(),
                        "description": item.find("div", class_="category-item-description").text.strip() if item.find("div", class_="category-item-description") else "No description",
                        "price": price,
                        "image_url": image_url,
                    })
                except Exception as e:
                    log_error(f"Error parsing item: {e}")
            menu_categories.append({"category": category_name, "items": items})
        except Exception as e:
            log_error(f"Error parsing category: {e}")
    return menu_categories


def scrape_menufy(url: str) -> Dict[str, Any]:
    """
    Scrapes the Menufy page for restaurant and menu information.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extracting restaurant information
        script_tag = soup.find("script", {"type": "application/ld+json"})
        restaurant_info = parse_json_ld(script_tag.string if script_tag else "")

        # Extracting menu categories and items
        menu_categories = scrape_menu(soup)

        # If no data is found, log the issue
        if not restaurant_info or not menu_categories:
            error_message = f"Failed to scrape data from the URL: {url}. No valid data found."
            log_error(error_message)
            print(error_message)
            return {}

        return {
            "restaurant": restaurant_info,
            "menu": menu_categories,
        }
    except Exception as e:
        log_error(f"Error scraping Menufy URL: {e}")
        return {}



def save_to_json(data: Dict[str, Any], output_file: str) -> None:
    """
    Saves the scraped data to a JSON file.
    """
    try:
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully saved to {output_file}")
    except Exception as e:
        log_error(f"Error saving JSON: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Menufy Scraper")
    parser.add_argument("--url", required=True, help="Menufy order URL to scrape")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    args = parser.parse_args()

    scraped_data = scrape_menufy(args.url)
    if scraped_data:
        save_to_json(scraped_data, args.output)
