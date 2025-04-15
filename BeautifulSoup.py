from bs4 import BeautifulSoup
import requests

url = 'https://thegoodshoppingguide.com/subject/ethical-skincare/?_gl=1*1g6vg9w*_up*MQ..*_ga*MTUwODAxMTUzMC4xNzQ0NTIyNjQy*_ga_PYEMHYT21H*MTc0NDUyMjY0Mi4xLjEuMTc0NDUyMjkxMy4wLjAuMA..'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

results = soup.find(id="rating__rows")
data= results.find_all("div", class_="rating__row") 

brands_data = []
for info in data: 
    brand_info = info.find("h3", class_="text-xs")
    ethics_info = info.find_all("h6", class_="text-base") #replaced find with find_all so it returns all matches as a list
    rating_info = info.find_all("span", class_="sr-only")
    score_info = info.find("div", class_="rating__index")

    if brand_info and ethics_info and rating_info:
        ethics = [(ethic.text.strip(), rating.text.strip()) for ethic, rating in zip(ethics_info, rating_info)] #used zip for parallel iteration
        brands_data.append({
            'name': brand_info.text.strip(),
            'ethics': ethics, #simplified
            'score': score_info.text.strip()
        })


user_input = input("Welcome! Enter a brand name: ").strip().lower() #allows user to search for specific brands 

brand_names = [brand['name'] for brand in brands_data]

if user_input == ('Brands').lower():
        print("\nAvailable Brands:\n")
        print(" | ".join(brand_names))
else:
    available = False
    for brand in brands_data:
        if brand['name'].lower() == user_input:
            print("\nBrand: " + brand['name'])
            print("Ethical Criteria:")
            for ethic, rating in brand['ethics']:
                print(" - " + ethic + " - " + rating)
            print("Overall Score: " + brand['score'])
            available = True
            break        

    if not available:
        print("Brand not found. Please check the spelling or try another brand!")

