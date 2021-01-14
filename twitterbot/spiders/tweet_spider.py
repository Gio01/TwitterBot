import scrapy
import os
import time
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
load_dotenv()
# deleted these env vars because we can simply go to the explore page of
# twitter instead of having to log into my account!
# user = os.getenv('USERNAME')
# passw = os.getenv('PASSWORD')


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
                print(div[i].get_attribute("href"))
    """
    def start_requests(self):
        urls = ['https://twitter.com/explore']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.find_links)


    def find_links(self, response):
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
        driver.get("https://twitter.com/explore")

        # We get the login input via the <input> tag name
        # same as -> driver.find_element_by_name('session[...]') I think this
        # is a change in the API from Selium 2 to 3 but the css selector seems
        # to be used by the full function call and not by using By
        # email = driver.find_element(By.NAME, 'session[username_or_email]')
        # password = driver.find_element(By.NAME, 'session[password]')

        # We are injecting in the username and the password into the inputs on
        # the site. Now when we send them we are essentially submitting the
        # form! The Keys.ENTER submits the form for us!
        # email.send_keys(user)
        # password.send_keys(passw, Keys.ENTER)

        # Go to the search page of witter that contains the search bar!
        # search = driver.find_element_by_css_selector("a[data-testid='AppTabBar_Explore_Link']")
        # search.click()

        # the send_keys function acts as us typing into the selected element
        # and then the Keys.Enter will enter the insrted search query that we
        # want
        search_bar = driver.find_element_by_css_selector("input[data-testid='SearchBox_Search_Input']")
        search_bar.send_keys('infosec', Keys.ENTER)

        # Now we need to obtain the link from the posts that I find on the
        # page!
        # Here I am making the driver wait 5 seconds for the posts to load in
        # to the page so that I can actually get data rendered for me to then
        # take the link for those specific posts!

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        driver.implicitly_wait(10)
        time.sleep(10)
        # get the div where the link is inside of its branch
        # Note: Results contains the list of all of the divs for the posts that
        # were found and then from there we can navigate through each of the
        # result posts and get the links inside these results divs!

        result = driver.find_elements_by_xpath("//div[@data-testid='tweet']//div//a")
        links = []
        for element in result:
            links.append(element.get_attribute("href"))

        print('End of finding links!')
        print('Links found in the explore page: ', links)
        visited = []
        post_link = []
        # The links list contains all of the links that are associated for
        # every post. Meaning that it will find hashtag links and photo links
        # but at this point I just need the link for the entire post so that I
        # can navigate to that page and then take the other links for the rest
        # of the post data including the photo links!! I will need all of the
        # links eventually so I have seperated all the links from the links
        # that are the entire post link which are located in the post_link
        for link in links:
            sub_string = link.split('/')[3]

            # print(sub_string)
            if 'status' in link and sub_string in visited and 'photo' not in link:
                post_link.append(link)
                print('Post link: ', post_link, '\n')
                # this get() loads a web page in the current browser session!
                driver.get(link)
                driver.implicitly_wait(5)
                # delay the execution for 2 seconds
                time.sleep(2)
                # I am giving scrapy the source code of the current page in the
                # broswer which we can obtain via the driver.page_source
                sel = Selector(text=driver.page_source)
                # This rn does get the user who made the post but it also gets
                # other names and a lot of repeated users. I need to make it
                # more specific. I can always just get the first item in this
                # list as that is the user who made the post!
                users = sel.xpath("//div/article[1]//div/a//div/span//text()").getall()
                post_data = sel.xpath("//div/article[1]//div[@class='css-1dbjc4n r-156q2ks']").css('span').getall()
                post_img_link = sel.xpath("//div/article[1]").css('img').xpath('@src').getall()
                # post_images = sel.xpath("//div/article[1]//div[@data-testid='tweetPhoto']//img//text()").getall()
                # post_video = sel.xpath("//div//article[1]//div[@data-testid='videoPlayer']//video//text()").getall()
                #  it is more common for there to be img links then actual img
                #  sources!
                print('Username: ', users[1], '\n')
                print('Post Data: ', post_data, '\n')
                print('Post Image Link: ', post_img_link, '\n')
                # print('Post Images: ', post_images, '\n')
                # print('Post Video: ', post_video, '\n')
            if 'hashtag' not in link:
                visited.append(sub_string)
            # print(visited)
        driver.quit()
