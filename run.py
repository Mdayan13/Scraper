from Cli.main import advanced_menu, maincli, get_url

 
import os
def display_header():
    os.system("clear")  # Clear screen
    os.system("figlet -f slant ANON ")
    print("\n============")
    print("\nGitHub: https://github.com/Mdayan13/")
    print("Telegram: https://t.me/anongeek12")
    print("\n============")
def main():
    if os.path.exists("Data"):
        display_header()
    else:
        print("Installing  requirements...")
        os.system("pip install -r requirement s.txt")
        print("Installation Complete ✅ ")
        os.system("clear")
        os.mkdir("Data")
        display_header()

    
    

if __name__ == "__main__":
    main()
    os.system("figlet -f slant scraper \n\n")
    
    url = get_url()
    if maincli(url):
        advanced_menu()
    
    