import requests
import selenium
import time
from selenium import webdriver
# Um mit der Seite zu interagieren
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
from os.path import exists

def get_housing_data(self):
    # URL of target website
    url = "https://www.immowelt.de/"

    # get html
    html = requests.get(url)
    html_doc = BeautifulSoup(html.text, "html.parser")

    #test
    Immobilie = html_doc.find_all(text = "Immobilie")
    # print(Immobilie[0].parent)

    # load chrome webdriver with a Service
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

    # call URL
    driver.get(url)

    # Return site title
    print(driver.title)

    # look for search bar
    search = driver.find_element(By.ID, 'tbLocationInput')

    # type string in search bar
    search.send_keys(self)

    # press return
    search.send_keys(Keys.RETURN)

    # wait for site to load
    time.sleep(2)

    # find apartments to click on
    soup = BeautifulSoup(driver.page_source, "html.parser")
    items = soup.find("div", {"class": "SearchList-22b2e"})

    # # Loop through apartments and click all items
    for item in items:
        driver.execute_script("arguments[0].click();", item)
        driver.back()



# call function
print(get_housing_data("Köln"))



