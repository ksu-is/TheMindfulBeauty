from bs4 import BeautifulSoup
import requests

url = 'https://thegoodshoppingguide.com/subject/ethical-skincare/?_gl=1*1g6vg9w*_up*MQ..*_ga*MTUwODAxMTUzMC4xNzQ0NTIyNjQy*_ga_PYEMHYT21H*MTc0NDUyMjY0Mi4xLjEuMTc0NDUyMjkxMy4wLjAuMA..'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

results = soup.find(id="rating__rows")
rows = results.find_all("div", class_="rating__row") 

for info in rows: 
    brand_name = info.find("h3", class_="text-xs")
    ethics = info.find("h6", class_="text-base")
    rating = info.find("div", class_="rating__index")

    if brand_name and ethics and rating:
        print(brand_name.text.strip())
        print(ethics.text.strip())
        print(rating.text.strip())