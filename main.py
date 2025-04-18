# main.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def check_links(url):
    """
    Fetches a web page and checks all anchor tag links for broken URLs.
    """
    try:
        # Get the HTML content of the page
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <a> tags with href attribute
        links = soup.find_all('a')
        print(f"\n🔎 Found {len(links)} links on {url}\n")

        for link in links:
            href = link.get('href')

            if href:
                # Join relative URLs with base URL
                full_url = urljoin(url, href)

                try:
                    # Check the link status (HEAD is faster than GET)
                    r = requests.head(full_url, allow_redirects=True, timeout=5)

                    if r.status_code >= 400:
                        print(f"❌ Broken: {full_url} (Status: {r.status_code})")
                    else:
                        print(f"✅ OK: {full_url}")

                except requests.RequestException as e:
                    print(f"⚠️ Error: Could not access {full_url} - {e}")

    except Exception as e:
        print("❗ Failed to fetch the webpage:", e)

if __name__ == "__main__":
    print("🔗 Broken Link Checker Tool\n")
    website = input("Enter website URL (e.g., https://example.com): ")
    check_links(website)
