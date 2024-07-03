import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def scrape_quotes():
    quotes = []
    authors = []
    author_urls = set()
    page_url = "/page/1"

    while page_url:
        soup = get_soup(BASE_URL + page_url)
        quote_divs = soup.find_all("div", class_="quote")

        for quote_div in quote_divs:
            text = quote_div.find("span", class_="text").get_text()
            author = quote_div.find("small", class_="author").get_text()
            tags = [tag.get_text() for tag in quote_div.find_all("a", class_="tag")]

            quotes.append({"tags": tags, "author": author, "quote": text})

            author_url = quote_div.find("a")["href"]
            if author_url not in author_urls:
                author_urls.add(author_url)
                author_soup = get_soup(BASE_URL + author_url)
                author_fullname = (
                    author_soup.find("h3", class_="author-title").get_text().strip()
                )
                author_born_date = (
                    author_soup.find("span", class_="author-born-date")
                    .get_text()
                    .strip()
                )
                author_born_location = (
                    author_soup.find("span", class_="author-born-location")
                    .get_text()
                    .strip()
                )
                author_description = (
                    author_soup.find("div", class_="author-description")
                    .get_text()
                    .strip()
                )

                authors.append(
                    {
                        "fullname": author_fullname,
                        "born_date": author_born_date,
                        "born_location": author_born_location,
                        "description": author_description,
                    }
                )

        next_button = soup.find("li", class_="next")
        page_url = next_button.find("a")["href"] if next_button else None

    return quotes, authors


def save_to_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    quotes, authors = scrape_quotes()
    save_to_json("quotes.json", quotes)
    save_to_json("authors.json", authors)


if __name__ == "__main__":
    main()
