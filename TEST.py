from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

brands_data = []

url = 'https://thegoodshoppingguide.com/subject/ethical-skincare/?_gl=1*1g6vg9w*_up*MQ..*_ga*MTUwODAxMTUzMC4xNzQ0NTIyNjQy*_ga_PYEMHYT21H*MTc0NDUyMjY0Mi4xLjEuMTc0NDUyMjkxMy4wLjAuMA..'
r = requests.get(url)

soup = BeautifulSoup(r.content, 'html.parser')
script = soup.find_all('script')[2]

results = soup.find(type="text/javascript")
table = results.find_all("div", class_="rating__row") 

for info in table:
    brand_info = info.find("h3", class_="text-xs")
    ethics_info = info.find_all("h6", class_="text-base") #replaced find with find_all so it returns all matches as a list
    rating_info = info.find_all("span", class_="sr-only")
    score_info = info.find("div", class_="rating__index")

    if brand_info and ethics_info and rating_info:
        csv_data = {
            'name': brand_info.text.strip(),
            'score': score_info.text.strip()
        }
        
        valid_ratings = ["Good", "Poor", "Acceptable"]
        for i in range(len(ethics_info)):
            ethic = ethics_info[i].text.strip() 
            rating = rating_info[i].text.strip()

            if rating in valid_ratings:
                csv_data[ethic] = rating #makes each ethic its own column with its correpsonding rating 
            
        brands_data.append(csv_data)

page = pd.DataFrame(brands_data)
page.to_csv('skincare.csv', index=False, encoding='utf-8-sig') #added 'utf-8-sig' parameter to fix misreading of csv file 
print('skincare.csv created!')
