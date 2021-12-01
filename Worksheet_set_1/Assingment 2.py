#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 1. program to display all the header tags from wikipedia.org.
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen('https://en.wikipedia.org/wiki/Main_Page')
bs = BeautifulSoup(html, "html.parser")
titles = bs.find_all(['h1', 'h2','h3','h4','h5','h6'])
print('List all the header tags :', *titles, sep='\n\n')


# In[ ]:


# 2. program to display IMDB’s Top rated 100 movies’ data (i.e. name, rating, year of release)
and make data frame.
from bs4 import BeautifulSoup
import requests
import re


# Downloading imdb top 250 movie's data
url = 'http://www.imdb.com/chart/top'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

movies = soup.select('td.titleColumn')
links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]

ratings = [b.attrs.get('data-value')
		for b in soup.select('td.posterColumn span[name=ir]')]

votes = [b.attrs.get('data-value')
		for b in soup.select('td.ratingColumn strong')]

list = []

# create a empty list for storing
# movie information
list = []

# Iterating over movies to extract
# each movie's details
for index in range(0, len(movies)):
	
	# Separating movie into: 'place',
	# 'title', 'year'
	movie_string = movies[index].get_text()
	movie = (' '.join(movie_string.split()).replace('.', ''))
	movie_title = movie[len(str(index))+1:-7]
	year = re.search('\((.*?)\)', movie_string).group(1)
	place = movie[:len(str(index))-(len(movie))]
	data = {"movie_title": movie_title,
			"year": year,
			"place": place,
			"star_cast": crew[index],
			"rating": ratings[index],
			"vote": votes[index],
			"link": links[index]}
	list.append(data)

# printing movie details with its rating.
for movie in list:
	print(movie['place'], '-', movie['movie_title'], '('+movie['year'] +
		') -', 'Starring:', movie['star_cast'], movie['rating'])


# In[ ]:


# 4. Write a python program to scrape cricket rankings from icc-cricket.com. You have to scrape:
a) Top 10 ODI teams in men’s cricket along with the records for matches, points and rating.
b) Top 10 ODI Batsmen in men along with the records of their team and rating.
c) Top 10 ODI bowlers along with the records of their team and rating. 
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd




final_result_file_name = "All Ranking List.csv"
final_column_names = ["Ranking Type", "Position", "Player Name", "Team Name", "Rating", "Career Best Rating", "Crawl URL"]
pd.DataFrame(columns=final_column_names).to_csv(final_result_file_name, sep="\t", index=False, encoding="utf-8")

for url in urls:
    request_object = requests.get(url, headers=headers)
    html_content = request_object.text
    print(request_object.status_code, "->", url)
    soup_object = BeautifulSoup(html_content, "lxml")
    for element in soup_object.select('[class="ranking-pos up"], [class="ranking-pos down"]'):
        element.replace_with(BeautifulSoup("<" + element.name + "></" + element.name + ">", "html.parser"))

    ranking_type = soup_object.select_one(".rankings-block__title-container > h4").text

    result_file_name = ranking_type + ".csv"
    column_names = ["Position", "Player Name", "Team Name", "Rating", "Career Best Rating", "Crawl URL"]
    pd.DataFrame(columns=column_names).to_csv(result_file_name, sep="\t", index=False, encoding="utf-8")

    for element in soup_object.select('table[class="table rankings-table"] tr'):
        if(element.find("th")):
            continue
        data_dict = dict()
        data_dict["Crawl URL"] = url
        data_dict["Ranking Type"] = ranking_type
        if(element.select_one('[class*="position"]')):
            data_dict["Position"] = element.select_one('[class*="position"]').text
        for player_name in (element.select('a[href*="/player-rankings"]')):
            if(player_name.text.strip()):
                data_dict["Player Name"] = player_name.text
        if(element.select_one('[class^="flag-15"]')):
            data_dict["Team Name"] = element.select_one('[class^="flag-15"]')["class"][-1]
        if(element.select_one('[class$="rating"]')):
            data_dict["Rating"] = element.select_one('[class$="rating"]').text
        if(element.select_one('td.u-hide-phablet')):
            data_dict["Career Best Rating"] = element.select_one('td.u-hide-phablet').text
        for key in data_dict.keys():
            data_dict[key] = re.sub(r"\s+", " ", data_dict[key])
            data_dict[key] = data_dict[key].strip()
        pd.DataFrame([data_dict], columns=column_names).to_csv(result_file_name, sep="\t", index=False, header=False, encoding="utf-8", mode="a")
        pd.DataFrame([data_dict], columns=final_column_names).to_csv(final_result_file_name, sep="\t", index=False, header=False, encoding="utf-8", mode="a")


# In[ ]:


# 6. python program to scrape details of all the posts from coreyms.com
def corey_soup_made(no_page=1):
    from bs4 import BeautifulSoup
    import csv
    import json
    import requests
    import pandas as pd
    
    #get the website using request
    for pageno in range(1,no_page+1):
        corey_response = requests.get(f'https://coreyms.com/page/{pageno}')
        corey_response.raise_for_status()
    
        # start making soup using Beautiful soup
        corey_soup = BeautifulSoup(corey_response.text,'lxml')

        # scrap the content out
        csv_file = open('cms_scrape.csv','w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Title','Desc','Youtube Link','Date'])
        tutorials = corey_soup.select('article')
        print(f'Tutorials in Page {pageno}')
        print('*'*50)
        for tutorial in tutorials:
            title = tutorial.find('h2',class_='entry-title').get_text()
            desc = tutorial.find('div',class_='entry-content').get_text().replace('\n','')
            if tutorial.iframe:
                ytlink = f"https://www.youtube.com/watch?={tutorial.iframe['src'].split('/')[-1].split('?')[0]}"
            else:
                ytlink = 'Notification'
            date_posted = tutorial.find('time',class_='entry-time').get_text()
        #         comments = tutorial.find('span',class_='entry-comments-link').get_text()
            
            print(f'Title Of The Tutorial: {title}')
            print(f'Tutorial Description: {desc}')
            print(f'Youtube Link: {ytlink}')
            print(f'Date Posted: {date_posted}')
        #         print(f'Number of Comments: {comments}')
            csv_writer.writerow([title,desc,ytlink,date_posted])
            print('')
            print('')
        csv_file.close()
        print('*'*50)
        print('')
        


# In[ ]:


# 3. program to display IMDB’s Top rated 100 Indian movies’ data
'''
Author: Reljod T. Oreta PUP-Manila
BSECE 5th year
'''
import lxml
import re
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
from requests import get

url1 = "https://www.imdb.com/list/ls056092300/"

class IMDB(object):
	"""docstring for IMDB"""
	def __init__(self, url):
		super(IMDB, self).__init__()
		page = get(url)

		self.soup = BeautifulSoup(page.content, 'lxml')

	def articleTitle(self):
		return self.soup.find("h1", class_="header").text.replace("\n","")

	def bodyContent(self):
		content = self.soup.find(id="main")
		return content.find_all("div", class_="lister-item mode-advanced")

	def movieData(self):
		movieFrame = self.bodyContent()
		movieTitle = []
		movieDate = []
		movieRunTime = []
		movieGenre = []
		movieRating = []
		movieScore = []
		movieDescription = []
		movieDirector = []
		movieStars = []
		movieVotes = []
		movieGross = []
		for movie in movieFrame:
			movieFirstLine = movie.find("h3", class_="lister-item-header")
			movieTitle.append(movieFirstLine.find("a").text)
			movieDate.append(re.sub(r"[()]","", movieFirstLine.find_all("span")[-1].text))
			try:
				movieRunTime.append(movie.find("span", class_="runtime").text[:-4])
			except:
				movieRunTime.append(np.nan)
			movieGenre.append(movie.find("span", class_="genre").text.rstrip().replace("\n","").split(","))
			try:
				movieRating.append(movie.find("strong").text)
			except:
				movieRating.append(np.nan)
			try:
				movieScore.append(movie.find("span", class_="metascore unfavorable").text.rstrip())
			except:
				movieScore.append(np.nan)
			movieDescription.append(movie.find_all("p", class_="text-muted")[-1].text.lstrip())
			movieCast = movie.find("p", class_="")

			try:
				casts = movieCast.text.replace("\n","").split('|')
				casts = [x.strip() for x in casts]
				casts = [casts[i].replace(j, "") for i,j in enumerate(["Director:", "Stars:"])]
				movieDirector.append(casts[0])
				movieStars.append([x.strip() for x in casts[1].split(",")])
			except:
                casts = movieCast.text.replace("\n","").strip()
                movieDirector.append(np.nan)
				movieStars.append([x.strip() for x in casts.split(",")])

			movieNumbers = movie.find_all("span", attrs={"name": "nv"})

			if len(movieNumbers) == 2:
				movieVotes.append(movieNumbers[0].text)
				movieGross.append(movieNumbers[1].text)
			elif len(movieNumbers) == 1:
				movieVotes.append(movieNumbers[0].text)
				movieGross.append(np.nan)
			else:
				movieVotes.append(np.nan)
				movieGross.append(np.nan)

		movieData = [movieTitle, movieDate, movieRunTime, movieGenre, movieRating, movieScore, movieDescription,
							movieDirector, movieStars, movieVotes, movieGross]
		return movieData


# In[ ]:


# 8 a python program to scrape mentioned details from dineout.co.in
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def dineout_list(request):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        response = requests.get("https://www.dineout.co.in/bangalore-restaurants",headers=headers)


        content = response.content
        soup = BeautifulSoup(content,"html.parser")

        top_rest = soup.find_all("div",attrs={"class": "listing-cards-wrapper"})
        list_tr = top_rest[0].find_all("div",attrs={"class": "cardBg"})

        # List of restaurants
        list_rest =[]
        for tr in list_tr:
            try:
                name = (tr.find("a",attrs={"data-type": "Name"})).text.replace('\n', ' ').strip()
                location = (tr.find("a",attrs={"data-type": "Locality"})).text.replace('\n', ' ').strip() + ", " + (tr.find("a",attrs={"data-type": "Area"})).text.replace('\n', ' ').strip()
                url = (tr.find("a",attrs={"data-w-onclick":"restarant_url_click_ga|w1-restarant"}))['href']
                rating = (tr.find("a",attrs={"data-w-onclick":"reviewLinkClickHandler|w1-restarant"})).text.replace('\n', ' ').strip()
                

                # For reviews
                try:
                    review_url = "https://www.dineout.co.in"+url+"/review"
                    response2 = requests.get(review_url,headers=headers)
                    content2 = response2.content
                    soup2 = BeautifulSoup(content2,"html.parser")
                    all_reviews = soup2.find_all("div",attrs={"class": "reviews marginT0"})


                    # Extracting total number of reviews
                    num = all_reviews[0].span.text.replace('\n', ' ')
                    num = num.replace('(', '')
                    num = num.replace(')', '')
                    newnum = int(num)//10+1;
                    # print(newnum)

                    # Scraping all reviews from single page
                    review_url_new = "https://www.dineout.co.in"+url+"/review?revpage="+str(newnum)
                    response3 = requests.get(review_url_new,headers=headers)
                    content3 = response3.content
                    soup3 = BeautifulSoup(content3,"html.parser")
                    all_reviews3 = soup3.find_all("div",attrs={"class": "reviews marginT0"})

                    list_ar = all_reviews3[0].find_all("div",attrs={"class": "user-info"})
                    list_review = []
                    dataframe2 = ""
                    for tr2 in list_ar:
                        try:
                            r_name = (tr2.find("div",attrs={"class": "name"})).text.replace('\n', ' ').strip()
                            r_date = (tr2.find("span",attrs={"class": "date"})).text.replace('\n', ' ').strip()
                            r_text = (tr2.find("span",attrs={"class": "more"})).text.replace('\n', ' ').strip()
                            # dataframe2 = [r_name,r_date,r_text]
                            dataframe2 += "<strong>"+r_name+"</strong><br>"+r_date+"<br><p>"+r_text+"</p><hr>"
                        except:
                            print()
                    list_review.append(dataframe2)
                    dataframe1 = [name,location,url,rating,list_review,num]
                except:
                    dataframe1 = [name,location,url,rating, "No reviews found!"]
                print(dataframe1)
                list_rest.append(dataframe1)
            except:
                print()
    except:
        print("Problem in scraping data")

    return render(request, 'dineout/dineout_list.html', {'list_rest':list_rest})


# In[ ]:


# 7. python program to scrape house details from mentioned URL. It should include house title, location area, EMI and price from nobroker.in.
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import time
import random
import progressbar


headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

# dataframe
titles = []
addresses = []
rents = []
sizes = []
deposits = []
furnishings = []
property_ages = []
available_fors = []
immediate_possessions = []

# progressbar for displaying % completion
bar = progressbar.ProgressBar(maxval=1000)
bar.start()

# scraping through 1000 pages of nobroker website of places in Chennai
for page in range(1000):
    bar.update(page+1)
    page += 1;
    link = "https://www.nobroker.in/property/rent/chennai/Chennai/?searchParam=W3sibGF0IjoxMy4wNDM3NjEyODI5MTkyLCJsb24iOjgwLjIwMDA2ODUxNjk2OTMsInNob3dNYXAiOmZhbHNlLCJwbGFjZUlkIjoiQ2hJSllUTjlULXBsVWpvUk05UmphQXVuWVc0IiwicGxhY2VOYW1lIjoiQ2hlbm5haSIsImNpdHkiOiJjaGVubmFpIn1d&sharedAccomodation=0&orderBy=nbRank,desc&radius=2&traffic=true&travelTime=30&propertyType=rent&pageNo="+str(page)

    response = get(link,headers=headers)

    # for testing if scraping of website is allowed...
    # print(response)
    # print(response.text[:1000])


    # Parsing through html page
    html_soup = BeautifulSoup(response.text,'html.parser')
    house_containers = html_soup.find_all('div', class_="card")
    if(house_containers != []):
        for container in house_containers:
            
            try:
                rent = container.find_all('h3')[2].find('span').text.replace(',','')
                rent = int(''.join(itertools.takewhile(str.isdigit,rent)))
                rents.append(int(rent))
            except:
                rents.append('-')
            try:
                size = int(container.find_all('h3')[0].find_all('span')[0].text.replace(',',''))
                sizes.append(int(size))
            except:
                sizes.append('-')
            try:
                deposit = int(container.find_all('h3')[1].find_all('span')[0].text.replace(',',''))
                deposits.append(int(deposit))
            except:
                deposits.append('-')
            title = (container.find('div','card-header-title').find('h2').text.replace('\n',''))
            address = (container.find('div','card-header-title').find('h5').text.replace('\n',''))
            titles.append(title)
            addresses.append(address)

            furnishing = (container.find('div','detail-summary').find_all('h5')[0].text.replace('\n',''))
            furnishings.append(furnishing)
    
            property_age = (container.find('div','detail-summary').find_all('h5')[1].text.replace('\n',''))
            property_ages.append(property_age)
    
            available_for = (container.find('div','detail-summary').find_all('h5')[2].text.replace('\n',''))
            available_fors.append(available_for)
    
            immediate_possession = (container.find('div','detail-summary').find_all('h5')[3].text.replace('\n',''))
            immediate_possessions.append(immediate_possession)
    else:
        break;

    time.sleep(random.randint(1,2))
bar.finish()
print("Successfully scraped {} pages containing {} properties.".format(page,len(titles)))


# creating dataframe to save data in .csv format
cols = ['Title', 'Address', 'Rent(Rs)', 'Deposit(Rs)', 'Size(Acres)', 'Furnishing', 'Property age', 'Available for', 'Immediate possession']

chennai = pd.DataFrame({'Title': titles,
                        'Address': addresses,
                        'Rent(Rs)': rents,
                        'Deposit(Rs)': deposits,
                        'Size(Acres)': sizes,
                        'Furnishing': furnishings,
                        'Property age': property_ages,
                        'Available for': available_fors,
                        'Immediate possession': immediate_possessions})[cols]
chennai.to_csv('chennai_rent.csv')


# In[ ]:


# 9. a python program to scrape weather details for last 24 hours from Tutiempo.net 
import requests
from pprint import pprint
def weather_data(query):
	res=requests.get('https://en.tutiempo.net/india.html');
	return res.json();
def print_weather(result,city):
	print("{}'s temperature: {}°C ".format(city,result['main']['temp']))
	print("Wind speed: {} m/s".format(result['wind']['speed']))
	print("Description: {}".format(result['weather'][0]['description']))
	print("Weather: {}".format(result['weather'][0]['main']))
def main():
	city=input('Enter the city:')
	print()
	try:
	  query='q='+city;
	  w_data=weather_data(query);
	  print_weather(w_data, city)
	  print()
	except:
	  print('City name not found...')
if __name__=='__main__':
	main()


# In[ ]:




