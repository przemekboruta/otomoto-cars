# OTOMOTO Cars - webscrapper

The webscraping tool allows you to quickly obtain a large SQLite database of cars sold on the OTOMOTO website.

Collected items:
- footer: offer's footer 
- brand: brand name based on footer's first substring
- descr: description of an offer
- price: *integer*, demanded price in PLN
- year: *integer*, year of production
- dist: *integer*, mileage in kilometers
- vol: *integer*, engine size in litres
- fuel: type of fuel in Polish
- location: seller's location name
- region: region name

Commands:
 - -create : Creates a new database, required for the first use of the script.
 - -url : Allows the user to input an URL from OTOMOTO search engine. The user can filter the cars to be included in the database in advance, and then paste the link from the browser.

###### Example: *python scrapper.py -create -url*
