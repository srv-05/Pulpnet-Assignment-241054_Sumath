import requests
from bs4 import BeautifulSoup

def scrape():
    base_urls = [
        'https://voxiitk.com/category/all-about-iitk/page/',
        'https://voxiitk.com/category/editorials/page/',
        'https://voxiitk.com/category/flagship-series/page/',
        'https://voxiitk.com/category/reports-and-investigations/page/',
        'https://voxiitk.com/category/surveys/page/',
        'https://voxiitk.com/category/beyond-iitk/page/' 
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    article_links = []

    for base_url in base_urls:
        page = 1
        while True:
            url = f'{base_url}{page}'
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            links = [a for a in soup.find_all('a', rel='bookmark') if a.string and a.string.strip()]
            article_links.extend(links)
            page += 1

    with open("clean_data.txt", "w", encoding="utf-8") as f:
        for i in article_links:
            article_url = i.get('href')
            try:
                article_response = requests.get(article_url, headers=headers)
                article_soup = BeautifulSoup(article_response.text, 'html.parser')

                title_tag = article_soup.find('h1', class_='entry-title entry-title-large')
                title = title_tag.get_text(strip=True) if title_tag else 'No Title'

                tag_container = article_soup.find('div', class_='entry-meta entry-categories cat-links categories-has-text-color')
                if tag_container:
                    tag_elements = tag_container.find_all('a', rel='category tag')
                    tags = ', '.join(tag.get_text(strip=True) for tag in tag_elements)
                else:
                    tags = 'No Tags'

                content_blocks = article_soup.find_all('div', class_='elementor-widget-container')
                paragraphs = []

                for block in content_blocks:
                    paragraphs.extend(block.find_all('p'))

                if paragraphs:
                    content = '\n'.join(p.get_text(strip=True) for p in paragraphs)
                else:
                    fallback_paragraphs = article_soup.find_all('p')
                    if fallback_paragraphs:
                        content = '\n'.join(p.get_text(strip=True) for p in fallback_paragraphs)
                    else:
                        content = 'No article content found.'

                f.write(content)
                f.write("\n")
            except Exception as e:
                f.write(f"Failed to process {article_url}: {e}\n\n")

if __name__ == '__main__':
    scrape()