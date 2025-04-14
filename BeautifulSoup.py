from bs4 import BeautifulSoup
import requests

url = 'https://thegoodshoppingguide.com/subject/ethical-skincare/?_gl=1*1g6vg9w*_up*MQ..*_ga*MTUwODAxMTUzMC4xNzQ0NTIyNjQy*_ga_PYEMHYT21H*MTc0NDUyMjY0Mi4xLjEuMTc0NDUyMjkxMy4wLjAuMA..'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

results = soup.find(id="rating__rows")
data= results.find_all("div", class_="rating__row") 

brands_data = []

for info in data: 
    brand_name = info.find("h3", class_="text-xs")
    ethics = info.find_all("h6", class_="text-base") #replaced find with find_all so it returns all matches as a list
    rating = info.find("div", class_="rating__index")

    print(ethics)

    if brand_name and ethics and rating: #ensures they are not empty
        brands_data.append({     #dictionary created
            'name': brand_name.text.strip(),
            'ethics': [criteria.text.strip() for criteria in ethics], #ensures all criteria for each company is collected 
            'rating': rating.text.strip()
        })


user_input = input("Welcome! Enter a brand name: ").strip().lower() #allows user to search for specific brands 

available = False
for brand in brands_data:
    if brand['name'].lower() == user_input:
        print("\nBrand: " + brand['name'])
        print("Ethical Criteria:")
        for e in brand['ethics']:
            print(" - " + e)
        print("Overall Rating: " + brand['rating'])
        found = True
        break

if not available:
    print("Brand not found. Please check the spelling or try another brand!")

