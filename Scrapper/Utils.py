
import requests
from urllib.parse import urlparse

def is_valid_url(url: str):
        result = urlparse(url)
        if result.scheme in ['http','https']:
            print('Valid Url ✅')
            return True
        else:
            print('Invalid Url ❌')
      
def url_info(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=3)
        print(f"Status Code:--> {response.status_code}")
        
        if response.status_code == 200:
            return True
        elif response.status_code == 403:
            print("Bot detected")
            return False
        elif response.status_code == 401:
            print("Unauthorised or Forbidden(login required)")
            return False
        elif response.status_code == 503:
            print("Services Unavailable")
            return False
        elif response.status_code == 429:
            print("Too many requests")
            return False
    except requests.exceptions.Timeout:
        print("Request timed out. Server took too long to respond.")
        return False
    except requests.exceptions.ConnectionError:
        print("Website is firewall Protected\nneed `PROXIES`to aceess it\n\n\=====================\n\nACCESS DENIED \n\n\=====================")
        print("Conatact this tool owner for more info👍")
        return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")
        return False

