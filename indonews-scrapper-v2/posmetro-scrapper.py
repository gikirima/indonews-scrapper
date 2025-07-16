# -*- coding: utf-8 -*-
"""
indonews-scrapper-v2-posmetro-medan-only.ipynb

This script is a modified version specifically for scraping news articles
from Posmetro Medan by iterating through its monthly archives.
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install feedparser requests beautifulsoup4 pandas tqdm

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from tqdm import tqdm
import time
import random

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Konfigurasi Selector untuk posmetro-medan.com ---
SELECTORS = {
    'posmetro-medan.com': {
        'judul': 'p.title',
        'author': 'span.fn.author',
        'date': 'abbr.published',
        'isi': 'div.post-body.entry-content' 
    }
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_posmetro_article_links(start_year=2017, start_month=1, end_year=2025, end_month=7):
    """
    Iterates through the monthly archives of posmetro-medan.com to collect all article links.
    """
    base_url = "https://www.posmetro-medan.com"
    article_links = set() # Use a set to automatically handle duplicates

    # Generate all year/month combinations for the archive URLs
    archive_urls = []
    for year in range(start_year, end_year + 1):
        month_start = start_month if year == start_year else 1
        month_end = end_month if year == end_year else 12

        for month in range(month_start, month_end + 1):
            archive_urls.append(f"{base_url}/{year}/{month:02d}")

    logging.info(f"Generated {len(archive_urls)} monthly archive pages to scan.")
    print(f"Scanning {len(archive_urls)} monthly archive pages for article links...")

    # Iterate through each monthly archive page and extract article links
    for url in tqdm(archive_urls, desc="Scanning Archives"):
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            link_elements = soup.select('h2.post-title.entry-title a')
            
            for link in link_elements:
                if link.has_attr('href'):
                    article_links.add(link['href'])
        except requests.RequestException as e:
            logging.warning(f"Could not retrieve or process archive page {url}: {e}")
            continue

    logging.info(f"Found {len(article_links)} unique article links.")
    return list(article_links)

def scrape_article(url, max_retries=2):
    """
    Scrapes the content of a single article from posmetro-medan.com.
    (Now with added delay to be polite to the server)
    """
    site_selectors = SELECTORS['posmetro-medan.com']

    # --- ADDED: A small, random delay before each request ---
    time.sleep(random.uniform(0.5, 2.0)) # Wait between 0.5 and 2 seconds

    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            judul = soup.select_one(site_selectors['judul'])
            author = soup.select_one(site_selectors['author'])
            tanggal = soup.select_one(site_selectors['date'])
            content_container = soup.select_one(site_selectors['isi'])
            
            isi = ''
            if content_container:
                isi = content_container.get_text(separator='\n', strip=True)

            if judul and isi:
                return {
                    'sumber': 'posmetro-medan.com',
                    'url': url,
                    'judul': judul.get_text(strip=True),
                    'author': author.get_text(strip=True) if author else None,
                    'tanggal_publikasi': tanggal.get_text(strip=True) if tanggal else None,
                    'isi_berita': isi,
                }
            else:
                logging.warning(f"Could not find title or content for {url}")
                return None
        except requests.RequestException as e:
            # For 503 errors, wait longer before retrying
            wait_time = (attempt + 1) * 3 # Wait 3s, then 6s, then 9s
            logging.warning(f"Request error (attempt {attempt+1}) for {url}: {e}. Waiting {wait_time}s.")
            if attempt < max_retries:
                time.sleep(wait_time) 
            else:
                return None
        except Exception as e:
            logging.error(f"An unexpected error occurred while scraping {url}: {e}")
            return None

def main():
    """
    Main function to run the entire scraping process.
    """
    # Get all article links by iterating through archives up to the current date
    all_article_links = get_posmetro_article_links(start_year=2017, start_month=1, end_year=2025, end_month=7)

    if not all_article_links:
        logging.info("No links to scrape. Halting process.")
        return

    scraped_data = []
    # Use ThreadPoolExecutor for parallel scraping
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_url = {executor.submit(scrape_article, url): url for url in all_article_links}

        for future in tqdm(as_completed(future_to_url), total=len(all_article_links), desc="Scraping Articles"):
            result = future.result()
            if result:
                scraped_data.append(result)

    if not scraped_data:
        logging.info("No data was successfully scraped.")
        return

    # Create a DataFrame from the scraped data
    logging.info(f"Creating DataFrame from {len(scraped_data)} articles...")
    df = pd.DataFrame(scraped_data)

    # Clean the DataFrame
    df.dropna(subset=['isi_berita', 'judul'], inplace=True)
    df = df[df['isi_berita'] != '']
    df.reset_index(drop=True, inplace=True)

    # Export DataFrame to a CSV file
    today_date = datetime.now().strftime('%Y-%m-%d')
    output_filename = f"scrapping_posmetro-medan_{today_date}.csv"

    try:
        df.to_csv(output_filename, index=False, encoding='utf-8-sig')
        logging.info(f"Scraping process complete. Data saved to file: {output_filename}")
        print(f"\n✅ Scraping Complete! {len(df)} articles successfully saved to '{output_filename}'.")
    except Exception as e:
        logging.error(f"Failed to save DataFrame to CSV: {e}")

if __name__ == '__main__':
    main()