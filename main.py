from bs4 import BeautifulSoup
import requests
import csv

search_input = input("Enter product name you want to query: ")

search_key = ""
for i in search_input:
    if i == " ":
        search_key += "+"
    else:
        search_key += i

URL = f"https://amazon.in/s?k={search_key}"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
HEADERS = ({"User-Agent": USER_AGENT, "Accept-Language": "en-US, en;q=0.5"})

http_request = requests.get(URL, headers=HEADERS)

webpage = BeautifulSoup(http_request.content, "html.parser")

products = webpage.find_all("a", attrs={"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})

product_links = []

for product in products:
    link = product.get("href")
    product_links.append("https://amazon.in/" + link)


products_detail = []

print(f"There are total {len(products)} products")
counter = 1

for link in product_links:
    print(f"Scraping Product Page {counter}")
    product_details = {"name": "", "price": "", "rating": ""}

    http_request_product = requests.get(link, headers=HEADERS)
    product_webpage = BeautifulSoup(http_request_product.content, "html.parser")

    try:

        product_details["name"] = product_webpage.find("span", attrs={"id": "productTitle"}).text.strip()
    except:
        product_details["name"] = "Product name not available"

    try:
        product_details["price"] = product_webpage.find("span", attrs={"class": "a-price-whole"}).text[:-1]
    except:
        product_details["price"] = "Product price not available"

    try:
        product_details["rating"] = product_webpage.find("span", attrs={"id": "acrPopover"}).find("span", attrs={"class": "a-icon-alt"}).text
    except:
        product_details["rating"] = "Rating not available"

    products_detail.append(product_details)

    counter += 1

csv_file = open(f"{search_input}.csv", "w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Product Name", "Product Price", "Product Rating"])

for product_detail in products_detail:
    csv_writer.writerow([product_detail.get('name'), product_detail.get('price'), product_detail.get('rating')])

print(f"Data successfully written into {search_input}.csv file.")
csv_file.close()






