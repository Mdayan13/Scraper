
from Scrapper import fetcher, Parser, Utils
import questionary
import os
def advanced_menu(url,fold):
    print("\n\n==========================================\n")
    choice = questionary.select(
        "Select an option:",
        choices=[
            "1.  Data parsing || Analyse",
            "2.  see on local host",
            "3.  Exit"
        ]
    ).ask()

    if choice == "1.  Data parsing || Analyse":
        print(f"\nSelected: {choice}")
        data = Parser.parse_data(url,fold)
        if data:
            Parser.download(data, fold)
    elif choice == "2.  see on local host":
        print(f"\nSelected: {choice}")
        print(" \n💻Address:-  127.0.0.1:8000")
        os.system("python -m http.server 8000 --directory Data")
    elif choice == "3.  Exit":
        print(f"\nselected: {choice}")
        exit()
        
def create_sep_folder(url):
    folder_name = url.split("//")[-1].split("/")[0]
    if not os.path.exists(f"Data/{folder_name}/"):
        os.mkdir(f"Data/{folder_name}/")
    return folder_name

def get_url()-> str:
    return input("Enter the URL➡️:  ")
def maincli(url:str):
    fold = create_sep_folder(url)
    print("\nChecking URL validity...")
    if not Utils.is_valid_url(url):
        return False
    
    print("\nChecking URL info...")
    url_info_result = Utils.url_info(url)
    if not url_info_result:
        return False
        
    print("Fetching Data...")
    if fetcher.fetch_data(url,fold):
        print("\nDATA fetched ✅ ")
        print("\nimporting raw data... ")
    advanced_menu(url,fold)
    