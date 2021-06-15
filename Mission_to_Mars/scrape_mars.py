#Import dependencies 
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import requests
import pandas as pd


def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

##############################################################################
    #Mars News 
   #Prepare everything for Mars News
    # Visit redplanetscience.com
    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")


    #Get the whole list news titles and of teasers 
    title_results = soup.find_all('div', class_='content_title')
    teaser_results = soup.find_all('div', class_='article_teaser_body')
    
    #Only get first news_title and teaser 
    news_title = title_results[0].text.strip()
    news_p= teaser_results[0].text.strip()

    ###############################################

    #Featured Mars image
    #Find the image url for the current Featured Mars Image
    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)

    #Scrape page into soup 
    html = browser.html
    soup = bs(html, 'html.parser')

    #Get featured image
    image_path = soup.find_all('img', class_="headerimage fade-in")[0]["src"]
    featured_image = url + image_path

    ##############################################
    #Mars characteritics table 
    t_url = "https://galaxyfacts-mars.com/"
    
    #Read the tables 
    tables = pd.read_html(t_url)

    #Get the table with the Mars, Earth Comparison 
    me_df = tables[0]
    me_df.columns = ['Mars-Earth Comparison', 'Mars', 'Earth']
    
    #Clean table and pass it to html 
    mars_earth_table = me_df.iloc[1:5, :]
    html_table = mars_earth_table.to_html()
    html_table.replace('\n', '')
    
    ###########################################################
    
    #Mars hemispheres
    # URL of page to be scraped
    url = "https://marshemispheres.com/"
    browser.visit(url)

    #Scrape page into soup 
    html = browser.html
    soup = bs(html, 'html.parser')
    
    #Create our empty list
    hemispheres_image_url = []

    items = soup.find_all('div', class_='item')
    
    #Loop through selected items
    for i in items:
    
        #Find "Hemisphere" title. Remember they are in h3 headers
        title = i.h3.text
    
        #Go inside to gthe hemisphere page to get image URL:
        link_url = i.find('a')['href']
        full_url= url + link_url
        browser.visit(full_url)
        img_url = browser.find_by_text('Sample')['href']
        #Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
        hemispheres_dict = {'Title': title,
                            'Image URL': img_url}
            #Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
        hemispheres_image_url.append(hemispheres_dict)

    ################################
 
    # Close the browser after scraping
    browser.quit()

    scrape_mars ={'news_title': news_title,
                'news_p': news_p,
                'image_url': featured_image,
                'html_table': html_table,
                'hemisphere_images': hemispheres_image_url
                }
    
    print("Ready!")

    return scrape_mars
   
