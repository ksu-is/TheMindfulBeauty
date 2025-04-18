from bs4 import BeautifulSoup
import requests
import pandas as pd

brands_data = []

#since only one URL neccesary took away 'for criteria:' portion
url = 'https://thegoodshoppingguide.com/subject/ethical-skincare/?_gl=1*1g6vg9w*_up*MQ..*_ga*MTUwODAxMTUzMC4xNzQ0NTIyNjQy*_ga_PYEMHYT21H*MTc0NDUyMjY0Mi4xLjEuMTc0NDUyMjkxMy4wLjAuMA..'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

results = soup.find(id="rating__rows")
data= results.find_all("div", class_="rating__row") 

for info in data:
    brand_info = info.find("h3", class_="text-xs")
    ethics_info = info.find_all("h6", class_="text-base") #replaced find with find_all so it returns all matches as a list
    rating_info = info.find_all("span", class_="sr-only")
    score_info = info.find("div", class_="rating__index")

    if brand_info and ethics_info and rating_info:
        ethics = []
        for i in range(len(ethics_info)):
            ethic = ethics_info[i].text.strip() 
            rating = rating_info[i].text.strip()
            ethics.append((ethic, rating)) #forgot to append 'ethic,rating' to 'ethics', added again 
            
        brands_data.append({
            'name': brand_info.text.strip(),
            'score': score_info.text.strip(),
            'ethics': ethics, #plan to filter out 'Use Setting' that is still appearing, wanted to test CSV first
        })

page = pd.DataFrame(brands_data, columns=['name', 'ethics', 'score']) #mispelled columns, fixed
csv = page.to_csv('skincare.csv')
print(csv)