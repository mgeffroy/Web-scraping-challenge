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
    t_url = 'https://galaxyfacts-mars.com/'
    
    #Read the tables 
    tables = pd.read_html(t_url)

    #Get the table with the Mars, Earth Comparison 
    me_df = tables[0]
    me_df.columns = ['Mars-Earth Comparison', 'Mars', 'Earth']
    
    #Clean table and pass it to html 
    mars_earth_table = me_df.iloc[1:5, :]
    html_table = mars_earth_table.to_html()
    html_table.replace('\n', '')
    


    # Get the max avg temp
    max_temp = avg_temps.find_all('strong')[1].text

    # BONUS: Find the src for the sloth image
    relative_image_path = soup.find_all('img')[2]["src"]
    sloth_img = url + relative_image_path



    ##### Store data in a dictionary
    costa_data = {
        "sloth_img": sloth_img,
        "min_temp": min_temp,
        "max_temp": max_temp
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return costa_data
