import requests
from bs4 import BeautifulSoup
import json

def scrape_batch_issue(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the "News" section header (h1)
    news_header = soup.find(lambda tag: tag.name == 'h1' and 'news' in tag.get_text(strip=True).lower())
    if not news_header:
        print(f"News section not found in {url}")
        return []

    articles = []
    current = news_header.find_next_sibling()

    while current:
        # Article starts at each <h1> after "News"
        if current.name == 'h1':
            title = current.get_text(strip=True)

            # Find image directly above the <h1>
            image_url = None
            prev = current.find_previous_sibling()
            while prev:
                img = prev.find('img')
                if img:
                    image_url = img['src']
                    break
                prev = prev.find_previous_sibling()

            # Collect paragraphs and bullet points until the next <h1>
            text_parts = []
            next_elem = current.find_next_sibling()
            while next_elem and not (next_elem.name == 'h1'):
                if next_elem.name == 'p':
                    text_parts.append(next_elem.get_text(strip=True))
                elif next_elem.name in ['ul', 'ol']:
                    for li in next_elem.find_all('li'):
                        text_parts.append(f"- {li.get_text(strip=True)}")
                next_elem = next_elem.find_next_sibling()

            articles.append({
                'title': title,
                'text': "\n".join(text_parts),
                'image_url': image_url,
                'link': url  # Use the issue URL for now
            })

            current = next_elem  # Move to next <h1>
        else:
            current = current.find_next_sibling()

    return articles

all_articles = []
for issue_num in range(301, 306):
    issue_url = f"https://www.deeplearning.ai/the-batch/issue-{issue_num}/"
    print(f"Scraping issue {issue_num}...")
    articles = scrape_batch_issue(issue_url)
    all_articles.extend(articles)

output_filename = "deeplearning_batch_301_to_305.json"
with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=2)

print(f"\n{len(all_articles)} articles saved to {output_filename}")