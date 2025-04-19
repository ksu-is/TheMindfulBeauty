from bs4 import BeautifulSoup
import requests
import pandas as pd

brands_data = []

url = 'https://thegoodshoppingguide.com/subject/ethical-skincare/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

results = soup.select("#rating__rows .rating__row") #broadened my reach to get all info needed
for data in results: #switched to using a CSS selector to scrape mroe accurately
    brand_tag = data.select_one("h4")
    parent_company_tag = data.select_one("p.text-base")
    GSG_score_tag = data.select_one("div.rating__index")

    brand = brand_tag.text.strip().replace(" Ethical Rating", "") #got rid of unecessary text
    parent_company = parent_company_tag.text.strip().replace("Parent company: ", "") #got rid of unecessary text
    GSG_score = GSG_score_tag.text.strip()

    csv_data = {
            'Brand': brand,
            'Parent Company': parent_company,
            'GSG Score': GSG_score
        }

    for pair in data.select("li"):  #changed to li elements to more accurately scrape
        criteria = pair.select_one("h6")
        rating = pair.select_one("span.sr-only")
        if criteria and rating:
            csv_data[criteria.text.strip()] = rating.text.strip() #makes each ethic its own column with its correpsonding rating 

    brands_data.append(csv_data)

scraped = pd.DataFrame(brands_data)
scraped.to_csv('skincare.csv', index=False, encoding='utf-8-sig') #added 'utf-8-sig' parameter to fix misreading of csv file 
print('skincare.csv created!')
print(scraped)