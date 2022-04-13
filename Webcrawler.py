import pandas as pd
from selenium import webdriver
import numpy as np
# Um mit der Seite zu interagieren
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time

# settings for printing in console
width = 320
pd.set_option("display.width", width)
pd.set_option("display.max_rows", 100)
np.set_printoptions(linewidth=width)
pd.set_option("display.max_columns", 30)

def get_housing_data(self):
    # Input city to lowercase
    self = self.lower()

    # URL of target website
    url = "https://www.immowelt.de/"

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

    result = []
    # Loop through the first 5 sites
    for i in range(1, 3):
        if i != 1:
            # go to next site
            driver.get(f"https://www.immowelt.de/liste/{self}/wohnungen/mieten?d=true&sd=DESC&sf=RELEVANCE&sp={i}")

            time.sleep(2)
            # find next apartments
            soup = BeautifulSoup(driver.page_source, "html.parser")
            items = soup.find("div", {"class": "SearchList-22b2e"})

        # Loop through apartments and click all items (loop through children)
        for item in items.children:
            tag_element = item.findChild()

            # check if NoneType
            if tag_element is not None:
                link = tag_element.get("href")
                driver.get(link)
                time.sleep(2)


                # get data
                try:
                    name = driver.find_element(By.XPATH, '// *[ @ id = "aUebersicht"] / h1')
                    price = driver.find_element(By.XPATH,
                                                '//*[@id="aUebersicht"]/app-hardfacts/div/div/div[1]/div[1]/strong')
                    sm = driver.find_element(By.XPATH,
                                                 '//*[@id="aUebersicht"]/app-hardfacts/div/div/div[2]/div[1]/span')
                    rooms = driver.find_element(By.XPATH,
                                                '//*[@id="aUebersicht"]/app-hardfacts/div/div/div[2]/div[2]/span')
                    address = driver.find_element(By.XPATH, '//*[@id="aUebersicht"]/app-estate-address')
                    info_1 = driver.find_element(By.XPATH, '//*[@id="aImmobilie"]/sd-card')

                    result.append(
                        [name.text, price.text, sm.text, rooms.text, address.text, info_1.get_attribute("textContent")])

                except:
                    print("exception")

    # result as pandas data frame
    result = pd.DataFrame(result, columns=["Description", "Price", "square-meters", "rooms", "address", "information"])
    return (result)


data = get_housing_data("köln")
print(data)




