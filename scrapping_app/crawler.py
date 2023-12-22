from http.cookies import SimpleCookie
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
import random
import json



def crawl_page(url,scroll_count=30):
    """
    request and crawl the page from the `url` parameter, and scroll down the page in order to load more data.
    the parameter `scroll_count` specifies how many times the page should be scrolled.
    """

    # get facebook cookie from the json file cookie_facebook.json
    
    with open ('cookie_facebook.json', "r", encoding='utf-8') as f:    
        # Reading from file
        FACEBOOK_COOKIE = json.loads(f.read())

    # Set chrome webdriver options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('--binary-location=chromedriver/chromedriver')
    # initialize chrome webdriver
    driver = webdriver.Chrome('chromedriver/chromedriver',options=chrome_options) 

    driver.maximize_window()
    
    driver.get(url)
    # Parse cookies from string format to Python Dict
    cookie = SimpleCookie()
    cookie.load(FACEBOOK_COOKIE)
    for key, morsel in cookie.items():
        driver.add_cookie({"name":key,"value":morsel.value})

    # In order to apply the new cookies settings, we need to request the page again and reload the browser for the cookies settings to take effect.
    driver.get(url)
    driver.refresh()
    for i in range(1,scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll down the page
        time.sleep(random.randint(3,5)) # using random to avoid being blocked
     
    return driver.page_source
