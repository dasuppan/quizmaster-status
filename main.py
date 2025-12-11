import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup

# Configuration
BASE_URL = 'https://www.servustv.com/tv-programm/PN0B1EC15B2FE10/'
SEARCH_STRING = 'Quizmaster'
OUTPUT_FILE = 'results.csv'
OUTPUT_FILE = 'results.csv'
HTML_FILE = 'index.html'

def check_site():
    try:
        date_param = datetime.now().strftime("%d.%m.")
        target_url = f"{BASE_URL}?d={date_param}"
        print(f"Checking URL: {target_url}")

        response = requests.get(target_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        for script_or_style in soup(["script", "style", "head", "meta", "noscript"]):
            script_or_style.decompose()

        # Extract only the text from the remaining HTML
        # separator=' ' prevents words from merging (e.g., "Hello</div><div>World")
        clean_text = soup.get_text(separator=' ')

        # 3. Check for the string in the CLEAN text
        # (Optional: .lower() makes it case-insensitive)
        found_string = SEARCH_STRING.lower() in clean_text.lower()

        # 4. Store the result
        with open(OUTPUT_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), target_url, found_string])

        update_html(found_string, target_url)

        print(f"Scrape successful. String found: {found_string}")

    except Exception as e:
        print(f"Error occurred: {e}")


def update_html(is_found, url):
    # Determine color and text based on result
    if is_found:
        color = "#2ecc71"
        status_text = f"Ja, heute läuft Quizmaster"
    else:
        color = "#e74c3c"
        status_text = f"Nein, heute läuft kein Quizmaster"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Simple HTML template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Scrape Status</title>
        <meta http-equiv="refresh" content="300"> <style>
            body {{ font-family: sans-serif; text-align: center; padding: 50px; }}
            .status {{ font-size: 48px; font-weight: bold; color: {color}; }}
            .time {{ color: #888; margin-top: 20px; }}
            .link {{ margin-top: 40px; display: block; }}
        </style>
    </head>
    <body>
        <h1>Current Status:</h1>
        <div class="status">{status_text}</div>
        <div class="time">Zuletzt überprüft: {timestamp}</div>
        <a class="link" href="{url}">Zum heutigen Programm</a>
    </body>
    </html>
    """

    # Write the HTML file
    with open(HTML_FILE, 'w') as f:
        f.write(html_content)


if __name__ == "__main__":
    check_site()