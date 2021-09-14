# tutorial from: https://betterprogramming.pub/the-only-step-by-step-guide-youll-need-to-build-a-web-scraper-with-python-e79066bd895a

# will allow us to send HTTP requests to get HTML files
import requests
# will help us parse the HTML files
from bs4 import BeautifulSoup
# will help us assemble the data into a DataFrame to clean and analyze it
import pandas as pd

# since scrapping source, languages of movies can change, so ensure it is English by:
headers = {"Accept-Language": "en-US, en;q=0.5"}

URL = 'https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv'

results = requests.get(URL, headers = headers)
soup = BeautifulSoup(results.text, 'html.parser')
#print(soup.prettify())

# initializing lists
titles = []
years = []
length = []
genre = []
ratings = []
metascores = []
us_gross = []

movie_elems = soup.find_all('div', class_ = 'lister-item')

# pulling data from each section of website
for i, movie_elem in enumerate(movie_elems):
	# old way of doing it: title_elem = movie_elem.find('h3', class_ = 'lister-item-header').text.strip() 
	# now we can simplify by putting the nested titles after div ".h3 .a"
	# if else statement can be made on one line:
	title_elem = movie_elem.h3.a.text if movie_elem.h3.a else 'No title found'
	# if more complicated, do not put on one line:
	# if movie_elem.h3.a:
	# 	title_elem = movie_elem.h3.a.text
	# else:
	# 	title_elem = 'No title found'

	# adding to lists
	titles.append(title_elem)
	# print(i+1, title_elem)
	
	# old: year_elem = movie_elem.find('span', class_ = 'lister-item-year').text.strip() 
	year_elem = movie_elem.h3.find('span', class_ = 'lister-item-year').text if movie_elem.h3.find('span', class_ = 'lister-item-year') else 'No year found'
	years.append(year_elem)
	# print(year_elem)

	# .p because it is found within the header .p
	length_elem = movie_elem.p.find('span', class_ = 'runtime').text if movie_elem.p.find('span', class_ = 'runtime') else 'No movie length found'
	length.append(length_elem)
	# print(length_elem)
	
	genre_elem = movie_elem.p.find('span', class_ = 'genre').text.strip()
	genre.append(genre_elem)
	# print(genre_elem)
	
	# rating is typed differently in the code. There is no text, it is only data-value = ""
	rating_elem = float(movie_elem.strong.text)
	ratings.append(rating_elem)
	# print(rating_elem)
	
	metascore_elem = int(movie_elem.find('span', class_ = 'metascore').text) if movie_elem.find('span', class_ = 'metascore') else "No metascore found"
	metascores.append(metascore_elem)
	# print(metascore_elem)

	# multiple nv categories under span, so pull all and then can clarify which position you want
	nv = movie_elem.find_all('span', attrs = {'name' : 'nv'})
	# not all have the gross worth
	if len(nv) > 1:
		us_gross_elem = nv[1].text
		# print(us_gross_elem, '\n')
	else:
		us_gross_elem = "-"
		# print('No US gross', '\n')
	us_gross.append(us_gross_elem)


# building DataFrame using pandas (this will make a table with titles listed left)
movies = pd.DataFrame({
	'movie' : titles,
	'year' : years,
	'length (min)' : length,
	'genre' : genre,
	'IMDb ratings' : ratings,
	'Metascore' : metascores,
	'US gross (millions)' : us_gross,
	})

#print(movies)

# in order to clean up data you must know what each data type has been stored as:
# print(movies.dtypes)

# cleaning up data:
# \d+ says to start extracting at the 1st digit, "+" means that it must have at least 1 digit
# \d* "*" means you can start at 0 integers
movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
movies['length (min)'] = movies['length (min)'].str.extract('(\d+)').astype(int)

# online tutorial way of doing it:
# movies['US gross (millions)'] = movies['US gross (millions)'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['US gross (millions)'] = movies['US gross (millions)'].str.replace('M', '').str.replace('$', '')
movies['US gross (millions)'] = pd.to_numeric(movies['US gross (millions)'], errors='coerce')


# print(movies.dtypes)

# Specifically saving in correct folder, using absolute file path
movies.to_csv('/Users/anjawu/Code/imdb-web-scraping/IMDbmovies.csv')