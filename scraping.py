#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt 

#initialize browser, create dictionary, end webdriver and return scraped data
def scrape_all():
    #initiate headless driver for dev
    browser = Browser(driver_name='chrome', executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    #run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemisphere(browser),
        "last_modified": dt.datetime.now()
        
    }
    browser.quit()
    return data

#set executable path
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}


def mars_news(browser):
    #visit mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    #optional browser delay
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #set up html parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    slide_elem = news_soup.select_one('ul.item_list li.slide')

    #try/except for error handling
    try:
        slide_elem.find("div", class_='content_title')
        #use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_='content_title').get_text()
        #use parent element to find paragraph text
        news_p = slide_elem.find("div", class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
   
    return news_title, news_p


# ## JPL Space featured image
def featured_image(browser):

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

    #try/except for error handling
    try:
        #find relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None
    

    #use base url to create absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url



def mars_facts():
    try:
        #read html table into dataframe
        df = pd.read_html('https://space-facts.com/mars/')[0]
    except BaseException:
        return None

    #assign columns and set index
    df.columns = ['description', 'Mars']
    df.set_index('description', inplace=True)

    #convert dataframe to html format
    return df.to_html(classes="table table-striped")


if __name__ == "__main__":
    #if running as script, print scraped data
    print(scrape_all())

def mars_hemisphere(browser):

    #visit url
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    #let browser load
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    
    targetList = []
    for i in range(4):
        browser.find_by_css("a.product-item h3")[i].click()

        #parse the resulting html
        html = browser.html
        hemisphereSoup = BeautifulSoup(html, 'html.parser')
        

    #try/except for error handling
        try:
            hemisphereTitle = hemisphereSoup.find('h2').text
            #find relative image url
            img_url = hemisphereSoup.find('a', text="Sample").get("href")
        except AttributeError:
            return None
   
        hemisphereDict = {'title': hemisphereTitle, 'img_url': img_url}

        targetList.append(hemisphereDict)
        browser.back()

    return targetList






