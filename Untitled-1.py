#Import SDK and create API object
import openfoodfacts
api = openfoodfacts.API(user_agent="TheMindfulFoodie")

api.product.text_search("mineral water")