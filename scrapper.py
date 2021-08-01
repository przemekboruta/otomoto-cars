from bs4 import BeautifulSoup
from requests import get
import sqlite3 
from sys import argv


#URL = 'https://www.otomoto.pl/osobowe/ford/mustang/?search%5Border%5D=created_at%3Adesc'
URL = 'https://www.otomoto.pl/osobowe/?search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D='
DB_NAME = 'otomoto_data.db'
try:
	MAX_PAGE = int(input("Input max no pages to be processed: "))
except:
	MAX_PAGE = 1000
	print("Value not an integer - processing max 1000 pages.")


def add_page_data(pagenum):

	try:
		page = get(f"{URL}&page={pagenum}")
		bs = BeautifulSoup(page.content, 'html.parser')
		for offer in bs.find_all('div', class_ = 'offer-item__wrapper'):
			try:
				footer = offer.find('a', class_= 'offer-title__link').get_text().strip().split(',')[0]
				brand = footer.split()[0]
				try:
					desc = offer.find('h3', class_='offer-item__subtitle ds-title-complement hidden-xs').get_text().strip().split(',')[0]
				except:
					desc = ""
				price = int(offer.find('span', class_='offer-price__number ds-price-number').get_text().splitlines()[1].replace(' ', ''))
				year = int(offer.find_all('li', class_ = 'ds-param')[0].get_text().strip())
				dist = int(offer.find_all('li', class_ = 'ds-param')[1].get_text().strip(' km\n ').replace(' ', ''))
				vol = int(offer.find_all('li', class_ = 'ds-param')[2].get_text().strip(' cm3\n ').replace(' ', ''))
				fuel = offer.find_all('li', class_ = 'ds-param')[3].get_text().strip()
				location = offer.find('span', class_ = 'ds-location-city').get_text().strip().split(',')[0]
				region = offer.find('span', class_ = 'ds-location-region').get_text().strip().split(',')[0].strip('()')
				#print(brand)

				cursor.execute('INSERT INTO offers VALUES (?,?,?,?,?,?,?,?,?,?)', (footer, brand, desc, price, year, dist, vol, fuel, location, region))
				db.commit()
				print("Added: ", footer[:20])
			except:
				print("Can't read record, probably an ad.")
			
	except:
		print("Something went wrong :( : ", sys.exc_info())

#Connect to DB and, optionally, create table	
db = sqlite3.connect(DB_NAME)
cursor = db.cursor()

if len(argv) > 1 and '-create' in argv:
	cursor.execute('''CREATE TABLE offers (footer TEXT, brand TEXT, descr TEXT, price REAL, year REAL, dist REAL, vol REAL, fuel TEXT, location TEXT, region TEXT)''')

if len(argv) > 1 and '-url' in argv:
	URL = input('Paste an otomoto URL from search (cars can be filtered): ')

for page in range(1,MAX_PAGE+1):
	try:
		add_page_data(page)
		print(f"Processing of page # {page} finished.")
	except:
		print(sys.exc_info())
		print("No more pages.")
		break

db.close()