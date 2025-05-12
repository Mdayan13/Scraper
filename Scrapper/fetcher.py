
import requests
from bs4 import BeautifulSoup
import os

def fetch_data(url, ff):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Create directory structure if it doesn't exist
        directory = f"Data/{ff}/html"
        os.makedirs(directory, exist_ok=True)
        
        # Write the file
        with open(f"{directory}/index.html", "w", encoding="utf-8") as f:
            f.write(str(soup))
        return True
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return False