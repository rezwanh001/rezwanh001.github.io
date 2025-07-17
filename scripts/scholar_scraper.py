# scripts/scholar_scraper.py
import requests
from bs4 import BeautifulSoup
import yaml
import os

USER_ID = 'HaI-oFUAAAAJ' # Your Google Scholar User ID
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', '_data', 'scholar.yml')

def scrape_scholar():
    url = f'https://scholar.google.com/citations?hl=en&user={USER_ID}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        stats_table = soup.find('table', {'id': 'gsc_rsb_st'})
        if not stats_table:
            raise ValueError("Stats table not found.")

        rows = stats_table.find_all('tr')
        stats = {
            'citations': {'all': rows[0].find_all('td')[1].text, 'since_2020': rows[0].find_all('td')[2].text},
            'h_index': {'all': rows[1].find_all('td')[1].text, 'since_2020': rows[1].find_all('td')[2].text},
            'i10_index': {'all': rows[2].find_all('td')[1].text, 'since_2020': rows[2].find_all('td')[2].text}
        }
        
        with open(DATA_FILE, 'w') as f:
            yaml.dump(stats, f, default_flow_style=False)
        print(f"Successfully updated Google Scholar stats in {DATA_FILE}")

    except Exception as e:
        print(f"Error scraping Google Scholar: {e}")

if __name__ == '__main__':
    scrape_scholar()