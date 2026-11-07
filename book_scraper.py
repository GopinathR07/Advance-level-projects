
import requests
from bs4 import BeautifulSoup
import csv


URL = "https://books.toscrape.com/"


def fetch_webpage(url):
    """Download webpage HTML."""

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; LearningScraper/1.0)"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        return response.text

    except requests.exceptions.RequestException as error:
        print("Website connection failed:", error)
        return None


def extract_books(html):
    """Extract book information from HTML."""

    soup = BeautifulSoup(html, "html.parser")

    book_containers = soup.find_all(
        "article",
        class_="product_pod"
    )

    books = []

    for book in book_containers:

        title_element = book.find("h3").find("a")
        title = title_element.get("title", "Unknown")

        price_element = book.find(
            "p",
            class_="price_color"
        )
        price = price_element.get_text(strip=True)

        rating_element = book.find(
            "p",
            class_="star-rating"
        )
        rating = rating_element.get("class")[1]

        availability_element = book.find(
            "p",
            class_="instock"
        )
        availability = availability_element.get_text(
            strip=True
        )

        book_data = {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Availability": availability
        }

        books.append(book_data)

    return books


def save_to_csv(books, filename="books.csv"):
    """Save book information into a CSV file."""

    if not books:
        print("No book records to save.")
        return

    fieldnames = [
        "Title",
        "Price",
        "Rating",
        "Availability"
    ]

    with open(
        filename,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(books)

    print(f"Successfully saved {len(books)} books to {filename}")


def main():

    print("===== BOOK WEB SCRAPER =====")

    html = fetch_webpage(URL)

    if html is None:
        return

    books = extract_books(html)

    print(f"\nTotal books extracted: {len(books)}")

    for index, book in enumerate(books, start=1):
        print(f"\nBook {index}")
        print("Title:", book["Title"])
        print("Price:", book["Price"])
        print("Rating:", book["Rating"])
        print("Availability:", book["Availability"])

    save_to_csv(books)

    print("\nScraping completed!")


if __name__ == "__main__":
    main()
