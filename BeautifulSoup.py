from bs4 import BeautifulSoup
import requests

url = 'https://thegoodshoppingguide.com/subject/ethical-skincare/?_gl=1*1g6vg9w*_up*MQ..*_ga*MTUwODAxMTUzMC4xNzQ0NTIyNjQy*_ga_PYEMHYT21H*MTc0NDUyMjY0Mi4xLjEuMTc0NDUyMjkxMy4wLjAuMA..'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

results = soup.find(id="rating__rows")
data= results.find_all("div", class_="rating__row") 

for info in data: 
    brand_name = info.find("h3", class_="text-xs")
    ethics = info.find_all("h6", class_="text-base") #replaced find with find_all so it returns all matches as a list
    rating = info.find("div", class_="rating__index")

    if brand_name and ethics and rating:
        print(brand_name.text.strip())
        #added necessary loop
        for diff in ethics:
            print(ethics.text.strip())
        print(rating.text.strip())

