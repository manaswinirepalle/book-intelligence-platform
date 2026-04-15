from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@dataclass
class ScrapedBook:
    title: str
    author: str
    description: str
    rating: float
    reviews_count: int
    book_url: str


def _rating_to_float(rating_class: str) -> float:
    return {"One": 1.0, "Two": 2.0, "Three": 3.0, "Four": 4.0, "Five": 5.0}.get(
        rating_class,
        0.0,
    )


def scrape_books(base_url: str, pages: int = 1):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    records = []

    try:
        for page_idx in range(1, pages + 1):
            page_url = base_url.replace("page-1.html", f"page-{page_idx}.html")
            driver.get(page_url)
            cards = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

            for card in cards:
                title_el = card.find_element(By.CSS_SELECTOR, "h3 a")
                title = title_el.get_attribute("title").strip()
                href = title_el.get_attribute("href")
                rating_class = (
                    card.find_element(By.CSS_SELECTOR, "p.star-rating")
                    .get_attribute("class")
                    .split()[-1]
                )

                driver.get(href)
                try:
                    description = driver.find_element(
                        By.CSS_SELECTOR,
                        "#product_description + p",
                    ).text.strip()
                except Exception:
                    description = "No description available."

                records.append(
                    ScrapedBook(
                        title=title,
                        author="Unknown",
                        description=description,
                        rating=_rating_to_float(rating_class),
                        reviews_count=0,
                        book_url=href,
                    )
                )
                driver.back()
    finally:
        driver.quit()

    return records

