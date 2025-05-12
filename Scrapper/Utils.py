
import requests
from urllib.parse import urlparse
issue = "==================================================\n\n ACCESS DENIED ❌\n\n:-irst of All the tool is working properly\n:- the Error raised judt because the site you are trying to Scrap is highly secured \n:-for this you have to integrate Proxy,\n👉 Contact me  for more info my Tg address is given Above in title\n\n=================================================="
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
            print("\nBot detected🤖")
            print(issue)
            
            return False
        elif response.status_code == 401:
            print("Unauthorised or Forbidden(login required)")
            print(issue)
            return False
        elif response.status_code == 503:
            print("Services Unavailable")
            print(issue)
            return False
        elif response.status_code == 429:
            print("Too many requests")
            print(issue)
            return False
    except requests.exceptions.Timeout:
        print("Request timed out. Server took too long to respond.")
        print(issue)
        return False
    except requests.exceptions.ConnectionError:
        print(issue)
        return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")
        print(issue)
        return False

