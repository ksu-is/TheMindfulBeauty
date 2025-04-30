import requests
from bs4 import BeautifulSoup
import chompjs
import pandas as pd
import html

def scrape_category(url, filename):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    ratings_objects = []  #store criterias and their scores
    comparison_objects = []  #store general brand info (name, link, GSG score, etc..)

    #Extract and parse all script tags
    scripts = soup.find_all('script')

    for script in scripts: 
        if not script.string: #skip scripts with no text content
            continue 

        #Parse all 'window.ratings[' JS objects
        if 'window.ratings[' in script.string:
            js = script.string.split('window.ratings[')
            for text in js[1:]:
                try:
                    clean = text.split('= (')[1].split(');')[0]
                    parsed = chompjs.parse_js_object(clean)
                    ratings_objects.append(parsed)
                except Exception: 
                    continue

        #Parse all 'window.comparison[' JS objects
        if 'window.comparison[' in script.string:
            js = script.string.split('window.comparison[')
            for text in js[1:]:
                try:
                    clean = text.split('= (')[1].split(');')[0] #isolate the JS object
                    parsed = chompjs.parse_js_object(clean) #convert JS object to Python dict
                    comparison_objects.append(parsed) #save to list
                except Exception:   
                    continue

    #Create map of brand names to their parent companies from HTML section
    parent_company_map = {}
    results = soup.select("#rating__rows .rating__row")
    for data in results:
        brand_tag = data.select_one("h4")
        parent_tag = data.select_one("p.text-base")
        
        if brand_tag and parent_tag:
            brand_name = brand_tag.text.strip().replace(" Ethical Rating", "").lower()
            parent_name = parent_tag.text.strip().replace("Parent company: ", "")
            parent_company_map[brand_name] = parent_name

    #Merge JS data with HTML info
    brands_data = []
    for i, brand in enumerate(comparison_objects):
        name = html.unescape(brand.get("company_name", "")).strip() #decode HTML characters
        link = brand.get("link", "")
        gsg_score = brand.get("ethical_company_index", "")
        parent_company = parent_company_map.get(name.lower())
        
        #Create a dictionary
        csv_data = {    
            "Brand": name,
            "GSG Score": gsg_score,
            "Link": link,
            "Parent Company": parent_company
        }

        total_raw_score = 0
        #Match to the same index in ratings
        if i < len(ratings_objects):   #ensure there is a matching ratings entry
            rating_dict = ratings_objects[i].get("ratings", {})
            if isinstance(rating_dict, dict):  #double check it is valid!
                for nests in rating_dict.values(): 
                    for nest in nests.values(): #loop through nested dictionary values
                        title = nest.get("title", "").strip() #extract necessary info!
                        score = nest.get("score", "").strip()
                        if title and score:
                            csv_data[title] = score
                            try:
                                total_raw_score += float(score) #convert str to float(decimal)
                            except ValueError:
                                pass  #in case the score is not a valid number

        #Store the total raw score
        csv_data["Raw Score Total"] = round(total_raw_score, 0)
        brands_data.append(csv_data)

        # Save to CSV
        df = pd.DataFrame(brands_data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"{filename} created!")
        return df

# Call for skincare data!
skincare_df = scrape_category(
    url = "https://thegoodshoppingguide.com/subject/ethical-skincare/",
    filename="skincare.csv"
)

# Call for fashion data!
fashion_df = scrape_category(
    url = "https://thegoodshoppingguide.com/subject/ethical-fashion-retailers/",
    filename = "fashion.csv"
)