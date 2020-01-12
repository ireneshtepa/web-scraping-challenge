from bs4 import BeautifulSoup
from splinter import Browser
browser = Browser('chrome')
import requests
import pandas as pd

def scrape():
    Mars_Data={}
    

# Mars news
def mars_news():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_="slide")
    titles=[]
    paragraphs=[]
    
    for r in results:
        title=r.find('div', class_='content_title').text
        titles.append(title)
        paragraph=r.find('div', class_='rollover_description_inner').text
        paragraphs.append(paragraph)

    articel_title=titles[0]
    article_content=paragraphs[0]

    mars_news=[articel_title, article_content]


# URL of page to be scraped
url_img = 'https://jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url_img)

#finding a link by partial text "FULL IMAGE"
browser.click_link_by_partial_text('FULL IMAGE')

##finding a link by partial text "more info"
browser.click_link_by_partial_text('more info')


# Create BeautifulSoup object; parse with 'html.parser'; examining results
soup_img=BeautifulSoup(browser.html, 'html.parser')
print(soup_img.prettify())

#scraping for image url
img_src=soup_img.find('figure', class_="lede").a['href']
img_url=f'https://www.jpl.nasa.gov{img_src}'
print(img_url)


# URL of page to be scraped
url_tweet="https://twitter.com/marswxreport?lang=en"
browser.visit(url_tweet)

# Retrieve page with the requests module; create BeautifulSoup object; parse; examine results
soup_tweet=BeautifulSoup(browser.html, 'html.parser')


print(soup_tweet.prettify())

#scraping for latest tweet text
mars_tweeter=soup_tweet.find_all('div', class_='js-tweet-text-container')
latest_tweet=mars_tweeter[0]
mars_weather=latest_tweet.p.text
print(mars_weather)


# URL of page to be scraped
url_facts="https://space-facts.com/mars/"


#checking for tables on the website
tables=pd.read_html(url_facts)
tables

#creating DataFrame from 1st table; naming columns
df = tables[0]
df.columns = ["Description", "Values"]
df.head()

#assigning index column
df.set_index('Description', inplace=True)
df.head()

#converting to html
html_table = df.to_html()
html_table


# URL of page to be scraped
url_hemi="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

# Retrieve page with the requests module; create BeautifulSoup object; parse; examine results
browser.visit(url_hemi)
soup_hemi=BeautifulSoup(browser.html, "html.parser")
print(soup_hemi.prettify())

#creating list of urls for each hemishpere's individual web-page
astro_url="https://astrogeology.usgs.gov/"
hemi_urls=[]
hemispheres=soup_hemi.find_all('div', class_='item')
for h in range (len(hemispheres)):
    hemi=astro_url+hemispheres[h].a['href']
    hemi_urls.append(hemi)
print(hemi_urls)


#looping through each hemishpere's individual web-page 
#to get original image url and hemishpere name and save this data into dictionary
hemisphere_image_urls=[]
for h in range (len(hemi_urls)):
    hemisphere_data={}
    browser.visit(hemi_urls[h])
    soup_hemi_urls=BeautifulSoup(browser.html, "html.parser")
    content=soup_hemi_urls.find('div', class_="content")
    hemisphere_data["title"]=content.h2.text.replace("Enhanced", "")
    hemisphere_data["img_url"]=content.a['href']
    hemisphere_image_urls.append(hemisphere_data)
    
hemisphere_image_urls