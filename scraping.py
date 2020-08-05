#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

# Path to chromedriver
#!which chromedriver

#set executable path
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser(driver_name='chrome', **executable_path)

#visit mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
#optional browser delay
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

#set up html parser
html = browser.html
news_soup = BeautifulSoup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

#use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

#use parent element to find paragraph text
news_p = slide_elem.find("div", class_='article_teaser_body').get_text()
news_p


# ## JPL Space featured image

#visit url
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

#find and click full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

#find more info button and click
browser.is_element_not_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

#parse the resulting html
html = browser.html
img_soup = BeautifulSoup(html, 'html.parser')

#find relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

#use base url to create absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

#read html table into dataframe
df = pd.read_html('https://space-facts.com/mars/')[0]
df.columns = ['description', 'value']
df.set_index('description', inplace=True)
df

df.to_html()

browser.quit()






