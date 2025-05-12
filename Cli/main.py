
from Scrapper import fetcher, Parser, Utils
import questionary
import os
def advanced_menu(url,fold):
    choice = questionary.select(
        "Select an option:",
        choices=[
            "1.  Data parsing || Analyse",
            "2.  see on local host",
            "3.  Exit"
        ]
    ).ask()

    if choice == "1.  Data parsing || Analyse":
        print(f"Selected: {choice}")
        data = Parser.parse_data(url,fold)
        if data:
            Parser.download(data, fold)
    elif choice == "2.  see on local host":
        print(f"Selected: {choice}")
        print("address:-  127.0.0.1:8000")
        os.system("python -m http.server 8000 --directory Data")
    elif choice == "3.  Exit":
        print(f"selected: {choice}")
        exit()
        
def create_sep_folder(url):
    folder_name = url.split("//")[-1].split("/")[0]
    if not os.path.exists(f"Data/{folder_name}/"):
        os.mkdir(f"Data/{folder_name}/")
    return folder_name

def get_url()-> str:
    return input("Enter the URL: ")
def maincli(url:str):
    fold = create_sep_folder(url)
    print("Checking URL validity...")
    if not Utils.is_valid_url(url):
        return False
    
    print("Checking URL info...")
    url_info_result = Utils.url_info(url)
    if not url_info_result:
        print("URL info check failed. Skipping fetch operation.")
        return False
        
    print("Fetching Data...")
    if fetcher.fetch_data(url,fold):
        print("DATA fetched ✅ and stored in Data/raw files")
    advanced_menu(url,fold)
    