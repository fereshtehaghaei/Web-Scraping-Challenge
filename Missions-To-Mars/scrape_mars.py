#!/usr/bin/env python
# coding: utf-8

# # Scraping and Analysis Tasks

# * Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/)
# * Collect the latest News Title and Paragraph Text
# * Assign the text to variables that you can reference later.

# ### Data Sources: 
# 
#    #### All the data were scraped from the following websites:
# 
# * [NASA Mars News Site](https://mars.nasa.gov/news/) -Scraped the latest News Title and Paragraph Text
# * [JPL Featured Space Image](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars) - Scraped the image url for the current Featured Mars Image
# * [Mars Facts webpage](https://space-facts.com/mars/) -Scraped the table containing facts about the planet including Diameter, Mass, etc
# * [USGS Astrogeology site](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) - Scraped high resolution images for each of Mar's hemispheres
# 

# In[6]:


# Import Dependencies & Setup
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, redirect
from bs4 import BeautifulSoup
from splinter import Browser
from pprint import pprint
from selenium import webdriver
import pandas as pd
import requests
import time
import pymongo


# ### For Chrome: Choose the executable path to driver 

# In[321]:

def init_browser(): 
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False) # while you are debuging have it False after done set headless to True


# ### For FireFox

# In[188]:


# from webdriver_manager.firefox import GeckoDriverManager
# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())


# # NASA Mars News
# 
# * Scrape the NASA Mars News Site and collect the latest:
#     * News Title
#     * Paragraph Text 
# * Assign the text to variables that you can reference later.

# In[189]:


def scrape():
    browser = init_browser()
    
    # Open Browser- Visit Nasa news url through splinter module
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)


    # In[240]:


    # HTML Object
    nasa_html = browser.html

    # Parse HTML Results with BeautifulSoup
    nasa_soup = BeautifulSoup(nasa_html, 'lxml')

    #print(nasa_soup.prettify())


    # In[193]:


    # Scrape HTML & Finding Everything inside ul
    nasa_results = nasa_soup.find('ul', class_='item_list')

    #nasa_results


    # #### Scrape and collect the latest News "TITLE"

    # In[244]:


    # Retrieve the latest element that contains news title
    news_title = nasa_results.find("div", class_ = "content_title").text

    # Display scrapped data for Title
    print("\n-----------------------------------\n")
    print(f"Latest News Title:\n\n{news_title}")
    print("\n-----------------------------------\n")


    # ####  Scrape and collect the "Paragraph Text"

    # In[245]:


    # Retrieve the latest element that contains news paragraph
    news_parag = nasa_results.find("div", class_ = "article_teaser_body").text

    # Display scrapped data paragraph text
    print("\n--------------------------\n")
    print(f"Paragraph:\n\n{news_parag}")
    print("\n---------------------------\n")


    # # JPL Mars Space Images - Featured Image
    # 
    # * Visit the url for JPL Featured Space Image [Here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)
    # 
    # * Use splinter to navigate the site & find the image url for the current Featured Mars Image 
    # * assign the url string to a variable called `featured_image_url`.
    # 
    # * Make sure to find the image url to the full size `.jpg` image.
    # 
    # * Make sure to save a complete url string for this image.
    # 

    # In[146]:


    # Open Browser - Visit Mars Space Images through splinter module
    jpl_images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_images_url)


    # In[147]:


    # Click 'Full Image' Button on main page
    browser.links.find_by_partial_text('FULL IMAGE').click()


    # In[148]:


    time.sleep(1)

    # Click 'more info' button to get to image page
    browser.links.find_by_partial_text('more info').click()


    # In[149]:


    # HTML Object 
    img_html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(img_html, 'lxml')


    # In[150]:


    #----------------------------------------
    # # My first approach to get image link
    #----------------------------------------
    # results = soup.find_all('figure', class_='lede')
    # results
    # # Search and Save image url 
    # img_url = results[0].a['href']
    # img_url


    # In[151]:


    # Use beautiful soup and store results from image in new page to search for image source
    img_url = soup.select_one('figure.lede a img').get('src')
    img_url


    # In[152]:


    #set a new variable to use Base URL (JPL main page url)
    main_url = 'https://www.jpl.nasa.gov'

    #Concatenate main_url & img_url to create an Absolute URL
    featured_image_url = (main_url + img_url)
    featured_image_url


    # ## Featured Image:

    # <img src ='https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA18249_hires.jpg'>

    # #### Save the Image

    # In[153]:


    #empty jpg file
    f = open('mars_featured_image.jpg', 'wb')


    # In[154]:


    f.close()


    # 
    # # Mars Facts

    # * Visit the Mars Facts webpage [Here](https://space-facts.com/mars/)
    # 
    # * Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # 
    # * Use Pandas to convert the data to a HTML table string.

    # In[155]:


    # Use Pandas to scrape data
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    tables


    # In[166]:


    # checking table's type
    type(tables)


    # In[171]:


    # Take first table for Mars Facts
    df = tables[0]
    df


    # In[172]:


    # Rename columns
    df.columns = ["Description","Value"]
    df


    # In[344]:


    # Convert table to html
    mars_fact_table = df.to_html()

    mars_fact_table.replace('\n', '')

    #print(mars_fact_table)


    # In[174]:


    df.to_html('mars_fact_table.html')


    # # Mars Hemispheres

    # * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
    # 
    # * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # 
    # * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    # 
    # * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    # In[322]:


    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)


    # In[332]:


    hemisphere_image_urls = []

    # Get a list of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")

    #loop through links and keep count of links
    for x in range(len(links)):

        try: 
            # Find element on each loop to avoid a stale element exception
            browser.find_by_css("a.product-item h3")[x].click()

            # Assign the HTML content of the page to a variable & Parse HTML with BeautifulSoup
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            
            # Get Hemisphere Image
            img_url = soup.find("img", class_ = "wide-image")['src']
            
            # Get Hemisphere Title
            title = soup.find("h2", class_ = "title").text

            #Concatenate main_url & img_url to create an Absolute URL
            main_url = 'https://astrogeology.usgs.gov'
            img_url = main_url + img_url

            hemisphere_dict = {"title": title, "img_url": img_url}

            # Append Dictionary objects 'title' & 'img_url' to List
            hemisphere_image_urls.append(hemisphere_dict)
            
            # Click 'Open' button to get to fullsize image
            browser.links.find_by_partial_text('Open').click()
            
            # Navigate Back to original page with all the hemispheres
            browser.back()

        except:
            print("Scraping Complete, Nothing Found")
                
    hemisphere_image_urls 


     # Return all results as one dictionary
    mars_data_dict = {
        "news_title" : news_title,
        "news_paragraph" : news_parag,
        "featured_image_url" : featured_image_url,
        "hemisphere_image" : hemisphere_image_urls
    }

    # In[343]:


    # Close the browser after scraping
    browser.quit()

    # Return results
    return(mars_data_dict)




