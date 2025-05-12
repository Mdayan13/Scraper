

from bs4 import BeautifulSoup
import questionary
def parse_data(url, bin):
    try:
        with open(f"Data/{bin}/html/index.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            data = {
                'urls': [],
                'images': [],
                'videos': [],
                'titles': [],
                'statements': [],
                'base_url': url
            }
            
            url_extract(soup, data)
            print(f"\nURLs extracted: {len(data['urls'])}")
            image_extract(soup, data)
            print(f"\nimages extraced: {len(data['images'])}")
            video_extract(soup, data)
            print(f"\nvideos extracted: {len(data['videos'])}")
            title_extract(soup, data)
            print(f"\ntitles Extracted: {len(data['titles'])}")
            statement_extract(soup, data)
            print(f"\nDtatements Extracted: {len(data['statements'])}")
            audio_music_extract(soup, data)
            print(f"\nAudio Extracted: {len(data['audio'])}")
            return data
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

def url_extract(soup, data):
    from urllib.parse import urljoin, urlparse
    base_url = data.get('base_url', '')
    
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            # Skip javascript: and mailto: links
            if href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                continue
                
            # Make relative URLs absolute
            if base_url:
                href = urljoin(base_url, href)
            
            # Parse the URL
            parsed = urlparse(href)
            
            # Only accept http/https URLs with valid domains
            if (parsed.scheme in ['http', 'https'] and 
                parsed.netloc and 
                '.' in parsed.netloc and
                not any(x in href.lower() for x in [
                    'javascript:', 'data:', 
                    'file:', 'ftp:', 'mailto:'])):
                # Remove duplicate fragments and normalize
                normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                if parsed.query:
                    normalized_url += f"?{parsed.query}"
                    
                # Add if not already present
                if normalized_url not in data['urls']:
                    data['urls'].append(normalized_url)

def image_extract(soup, data):
    # Extract from img tags
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            data['images'].append(src)
        for a in data['urls']:
            if a.endswith(('.jpg','.png','.jpeg','.gif','.svg')):
                data['images'].append(a)
    
    # Extract from CSS background images
    for tag in soup.find_all(style=True):
        if 'background-image' in tag['style']:
            data['images'].append(tag['style'])

def video_extract(soup, data):
    # Extract from video tags
    for video in soup.find_all('video'):
        src = video.get('src')
        if src:
            data['videos'].append(src)
        for v in data['urls']:
            if v.endswith(('.mp4','.webm','.mkv','.avi','.flv','.mov')):
                data['videos'].append(v)
    # Extract from source tags within video
    for source in soup.find_all('source'):
        src = source.get('src')
        if src and any(ext in src.lower() for ext in ['.mp4', '.webm', '.ogg']):
            data['videos'].append(src)
            
    # Extract from iframes (common for embedded videos)
    for iframe in soup.find_all('iframe'):
        src = iframe.get('src')
        if src:
            data['videos'].append(src)

def title_extract(soup, data):
    # Get main title
    if soup.title:
        data['titles'].append(soup.title.string)
    
    # Get all headings
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if heading.string:
            data['titles'].append(heading.string.strip())

def statement_extract(soup, data):    
    # Extract paragraphs
    for p in soup.find_all('p'):
        if p.string:
            data['statements'].append(p.string.strip())
    
    # Extract article content
    for article in soup.find_all('article'):
        if article.string:
            data['statements'].append(article.string.strip())
    
    # Extract div with content
    for div in soup.find_all('div', class_=['content', 'article', 'text']):
        if div.string:
            data['statements'].append(div.string.strip())

def audio_music_extract(soup, data):
    # Add audio field if not exists
    if 'audio' not in data:
        data['audio'] = []
        
    # Extract from audio tags
    for audio in soup.find_all('audio'):
        src = audio.get('src')
        if src:
            data['audio'].append(src)
            
    # Extract from source tags within audio
    for source in soup.find_all('source'):
        src = source.get('src')
        if src and any(ext in src.lower() for ext in ['.mp3', '.wav', '.ogg', '.m4a', '.aac']):
            data['audio'].append(src)
            
    # Check hrefs for audio files
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and any(ext in href.lower() for ext in ['.mp3', '.wav', '.ogg', '.m4a', '.aac']):
            data['audio'].append(href)

def download(data, bin):
    import requests
    import os

    choice = questionary.select(
        "Which Data-Type you wanna work on",
        choices=[
            "1. URLs🔗",
            "2. Images🖼️",
            "3. Videos🎦",
            "4. Titles📝",
            "5. Statements📜",
            "6. Audio🎧",
            "7. All🌐"
        ]
    ).ask()

    def download_file(url, folder):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                filename = url.split('/')[-1]
                filepath = os.path.join(f"Data/{bin}/{folder}", filename)
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"\nDownloaded: {filename}")
        except Exception as e:
            print(f"\nError downloading {url}: {str(e)}")
        print(f"\n\n\n==========\n\nDownload📂 => Data/{folder}")
    def save_text(content, filename, folder):
        filepath = os.path.join(f"Data/{bin}/{folder}", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content + '\n')

    # Create necessary folders
    os.makedirs(f"Data/{bin}/images", exist_ok=True)
    os.makedirs(f"Data/{bin}/videos", exist_ok=True)
    os.makedirs(f"Data/{bin}/audio", exist_ok=True)
    os.makedirs(f"Data/{bin}/text", exist_ok=True)

    if choice == "1. URLs🔗":
        
        # First save URLs to file
        with open(f"Data/{bin}/text/urls.txt", 'w') as f:
            for url in data['urls']:
              
                f.write(url + '\n')
        print("\nURLs saved to urls.txt")
        
        # Then attempt to download the URLs
        download_dir = f"Data/{bin}/downloads"
        os.makedirs(download_dir, exist_ok=True)
        
        for url in data['urls']:
            try:
                response = requests.get(url, stream=True, timeout=5)
                if response.status_code == 200:
                    filename = url.split('/')[-1]
                    if not filename:
                        filename = 'download_' + str(hash(url))
                    filepath = os.path.join(download_dir, filename)
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    print(f"\nDownloading: {filename}")
                else:
                    print(f"\nFailed to download: {url}")
            except Exception as e:
                print(f"\nError downloading {url}: {str(e)}")
    elif choice == "2. Images🖼️":
        for url in data['images']:
            if url.startswith(('http://', 'https://')):
                download_file(url, "images")

    elif choice == "3. Videos🎦":
        for url in data['videos']:
            if url.startswith(('http://', 'https://')):
                download_file(url, "videos")

    elif choice == "4. Titles📝":
        for i, title in enumerate(data['titles']):
            save_text(title, f"title_{i}.txt", "text")
        print("\nTitles saved to text files")

    elif choice == "5. Statements📜":
        for i, statement in enumerate(data['statements']):
            save_text(statement, f"statement_{i}.txt", "text")
        print("\nStatements saved to text files")

    elif choice == "6. Audio🎧":
        for url in data['audio']:
            if url.startswith(('http://', 'https://')):
                download_file(url, "audio")

    elif choice == "7. All🌐":
        # Download everything
        for url in data['images']:
            if url.startswith(('http://', 'https://')):
                download_file(url, "images")
        for url in data['videos']:
            if url.startswith(('http://', 'https://')):
                download_file(url, "videos")
        for url in data['audio']:
            if url.startswith(('http://', 'https://')):
                download_file(url, "audio")
        # Save text content
        with open(f"Data/{bin}/text/urls.txt", 'w') as f:
            for url in data['urls']:
                f.write(url + '\n')
        for i, title in enumerate(data['titles']):
            save_text(title, f"title_{i}.txt", "text")
        for i, statement in enumerate(data['statements']):
            save_text(statement, f"statement_{i}.txt", "text")
        print("\nAll content downloaded and saved")
    
    