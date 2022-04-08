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

    # find next page
    page = soup.find("div", {"class": "Pagination-190de"})
    # save old url
    search_url = driver.current_url

    # Loop through the first 4 sites
    for i in range(4):

        # Loop through apartments and click all items (loop through children)
        result = []
        for item in items.children:
            tag_element = item.findChild()

            # check if NoneType
            if tag_element is not None:
                link = tag_element.get("href")
                driver.get(link)
                time.sleep(2)

                element_result = []
                # get data
                try:
                    name = driver.find_element(By.XPATH, '// *[ @ id = "aUebersicht"] / h1')
                    price = driver.find_element(By.XPATH,
                                                '//*[@id="aUebersicht"]/app-hardfacts/div/div/div[1]/div[1]/strong')
                    sm = driver.find_element(By.XPATH,
                                             '//*[@id="aUebersicht"]/app-hardfacts/div/div/div[2]/div[1]/span')
                    rooms = driver.find_element(By.XPATH,
                                                '//*[@id="aUebersicht"]/app-hardfacts/div/div/div[2]/div[2]/span')
                    adress = driver.find_element(By.XPATH, '//*[@id="aUebersicht"]/app-estate-address')
                    info_1 = driver.find_element(By.XPATH, '//*[@id="aImmobilie"]/sd-card/div[2]/ul/li[1]')
                    info_2 = driver.find_element(By.XPATH, '//*[@id="aImmobilie"]/sd-card/div[2]/ul')
                    info_3 = driver.find_element(By.XPATH, '//*[@id="aImmobilie"]/sd-card/div[3]/ul')
                    element_result.append(
                        [name.text, price.text, sm.text, rooms.text, adress.text, info_1.text, info_2.text,
                         info_3.text])

                except:
                    print("exception")
                result.append(element_result)
        # go back to search result site
        driver.get(search_url)


        # go to next site
        next_page = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div[1]/div/div[7]/div/button[2]")
        next_page.click()
        return (result)



print(get_housing_data("Hamburg"))




