from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time

import pandas as pd
import numpy as np

options = Options()
options.add_argument("--headless")

service = webdriver.FirefoxService("/usr/local/bin/geckodriver")

driver = webdriver.Firefox(options=options, service=service)

driver.implicitly_wait(2)

driver.set_window_size(1024, 3000)

driver.get("https://vtm.paradoxwikis.com/Clans")

text_blobs = driver.find_elements(By.TAG_NAME, "p")

clan_descriptions = {}

for pair in zip(range(2, len(text_blobs)-3,2), range(3, len(text_blobs)-3, 2)): #drop the initial blob and thinbloods

    if text_blobs[pair[1]].text != "":
        clan_descriptions[text_blobs[pair[0]].text] = text_blobs[pair[1]].text



pd.DataFrame(clan_descriptions.items(), columns=['Clan', 'Description']).to_csv('clan_descriptions.csv')

driver.quit()