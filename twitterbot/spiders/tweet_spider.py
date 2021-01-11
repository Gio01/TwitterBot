import scrapy
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from scrapy.utils.response import open_in_browser
from dotenv import load_dotenv
load_dotenv()

user = os.getenv('USERNAME')
passw = os.getenv('PASSWORD')


class TweetSpider(scrapy.Spider):
    name = 'tweets'
    allowed_domains = ['twitter.com']
    # my custom settings

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'CONCURRENT_REQUESTS': 10, 'DOWNLOAD_DELAY': 5.0, 'LOG_LEVEL': 'INFO'
    }

    """
    Before I can even begin to scrape data from twitter I need to actually
    login into my account as if it was me by using selenium! Then I can
    scrape from what would appear on my feed!
    Step1: set up my user and password in an .env file and then get them in
    this file. Make sure to ignore in the .gitignore!
    """
    def start_requests(self):
        urls = ['https://twitter.com/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        # This is the path to the chromedriver exetuable that will open a
        # chrome window and then run the rest of the code! This is located both
        # in my variable Windows path and within this same directory!
        # This will also open the Chrome Window!
        driver = webdriver.Chrome('chromedriver_win32/chromedriver.exe')


        # the driver will wait for 5 seconds for code to render in the browser
        # we use implicitly when we do not know just how much data is going to
        # get rendered onto the site
        driver.implicitly_wait(5)

        # Fetch this link
        driver.get("https://twitter.com/login")

        # We get the login input via the <input> tag name
        # same as -> driver.find_element_by_name('session[...]') I think this
        # is a change in the API from Selium 2 to 3 but the css selector seems
        # to be used by the full function call and not by using By
        email = driver.find_element(By.NAME, 'session[username_or_email]')
        password = driver.find_element(By.NAME, 'session[password]')

        # We are injecting in the username and the password into the inputs on
        # the site. Now when we send them we are essentially submitting the
        # form! The Keys.ENTER submits the form for us!
        email.send_keys(user)
        password.send_keys(passw, Keys.ENTER)

        # I am navigating to my profile page on twitter
        myprofile = driver.find_element_by_css_selector("a[aria-label='Profile']")
        myprofile.click()
        # In the same manner I could click on home and then submit my query
        # into the search bar with selenium. Find the css selector that will
        # give me that
        # a[role]='link'
        # NOTE: find_elementS_by_css_selector! We are getting back a list of
        # items so this cannot be the regular by element func because that func
        # expects a single return value!
        tweet_link = driver.find_elements_by_css_selector("div[data-testid='tweet'] a[role='link']")
        print(tweet_link)
        # the css selector returns a Web element list, an empty list if nothing
        # is found!
        for data in tweet_link:
            print(data)
        driver.quit()
        print('End!')
