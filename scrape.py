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



def parse_vampire_page(driver):

    try: 
        aside = driver.find_element(By.CSS_SELECTOR, ".portable-infobox")
    except NoSuchElementException:
        return None

    driver.implicitly_wait(5)

    characteristics = aside.find_elements(By.TAG_NAME, "h3")

    characteristics_values = aside.find_elements(By.CSS_SELECTOR, "[class='pi-data-value pi-font']")

    character_dict = {}

    for i in zip(characteristics, characteristics_values): 
    
        #if i[0].text == "Childer":
        if i[0].text in ["Childer", "Sire", "Clan", "Generation"]:

            if "\n" in i[1].text:
                character_dict[i[0].text] = [child.text for child in i[1].find_elements(By.TAG_NAME, "li")]

                if  len(character_dict[i[0].text]) == 0 : #check if empty list
                    character_dict[i[0].text] = i[1].text
            else:
                character_dict[i[0].text] = i[1].text
        
        if i[0].text == "Sire":
            try: 
                character_dict["Sire_Link"] = i[1].find_element(By.TAG_NAME, "a").get_attribute("href")
            except NoSuchElementException:
                pass
                

    if not character_dict:
        return None
    
    character_dict["Name"] = driver.find_element(By.CSS_SELECTOR, "[class='mw-page-title-main']").text
    character_dict["Link"] = driver.current_url

    #try:
    #    character_dict["Image"] = driver.find_element(By.CLASS_NAME, "pi-image-thumbnail").get_attribute("src")

    #except NoSuchElementException:
    #    character_dict["Image"] = np.nan

    return character_dict

def parse_category_page(driver):

    complete_chars = []
    page_members = driver.find_element(By.CLASS_NAME, 'category-page__members')
    chars = page_members.find_elements(By.CLASS_NAME, 'category-page__member-link')

    main_tab = driver.current_window_handle

    for char in chars:
        link = char.get_attribute("href")
        print(f"Link: {link}")
        driver.implicitly_wait(2)
        
        driver.switch_to.new_window('tab')
        driver.get(link)

        character_attributes = parse_vampire_page(driver)

        if character_attributes:
            complete_chars.append(character_attributes)

        driver.close()

        driver.switch_to.window(main_tab)

        driver.implicitly_wait(2)

    return complete_chars

def parse_category(driver, STARTING_URL = "https://whitewolf.fandom.com/wiki/Category:Vampire:_The_Masquerade_character"):

    #driver.get(STARTING_URL)

    dfs = []

    while 1: 

        dfs.append(pd.DataFrame(parse_category_page(driver)))

        try:
            next = driver.find_element(By.CSS_SELECTOR, "[class='category-page__pagination-next wds-button wds-is-secondary']")
        except NoSuchElementException:
            break

        driver.execute_script("arguments[0].scrollIntoView(false);", next)

        time.sleep(2)

        next.click()

        time.sleep(2)

    all_vampires = pd.concat(dfs)
    return all_vampires
    #all_vampires.to_csv("vampires_salubri.csv")
    #print(all_vampires.head())
    #driver.quit()


#parse_category(STARTING_URL= "https://whitewolf.fandom.com/wiki/Category:Salubri")

def parse_categories(STARTING_URL = "https://whitewolf.fandom.com/wiki/Category:Clans_(VTM)"):

    driver.get(STARTING_URL)

    pages = driver.find_elements(By.CLASS_NAME, 'category-page__member-link')

    category_page = driver.current_window_handle

    i = 0

    for page in pages: 

    
        if "Category:Vampires of unknown clan" in page.text:

            #if i >= 11:  #i <= ...
            text = page.text
            link = page.get_attribute("href")

            driver.implicitly_wait(2)

            driver.switch_to.new_window('tab')

            driver.get(link)

            clan_data = parse_category(driver)

            clan_data.to_csv(f"data_updated/{text}.csv")

            driver.close()

            driver.switch_to.window(category_page)

            driver.implicitly_wait(2)

            #i += 1

    driver.quit()


def find_first_substring(sentence, substrings):
    earliest_index = len(sentence) + 1
    first_substring = None
    for substring in substrings:
        index = sentence.find(substring)
        if index != -1 and index < earliest_index:
            earliest_index = index
            first_substring = substring
    return first_substring

def parse_the_clan(sentence):
    possible_clans = ["assamite", "banu haqim", "brujah", "gangrel", "hecata", "giovanni", "cappadocian", "samedi", 
                      "lasombra", "malkavian", "ministry", "nosferatu", "ravnos", "salubri", "toreador", "tremere",
                      "tzimisce", "tentrue"]
    
    return find_first_substring(sentence, possible_clans)


def parse_the_generation(sentence):
    ordinals = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth"]
    ordinal_numerals = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"]

    possible_gens = ordinal_numerals + ordinals

    map = {}

    for count, ordinal in enumerate(zip(ordinals, ordinal_numerals)):
        map.update(dict.fromkeys(ordinal, count+1))
    

    gen = find_first_substring(sentence, substrings=possible_gens)

    if gen:
        return map[gen]
    return None


def parse_minor():
    driver.get("https://whitewolf.fandom.com/wiki/Minor_characters_in_WoD")

    container = driver.find_element(By.CSS_SELECTOR, "[class='mw-content-ltr mw-parser-output']")
    lists= container.find_elements(By.TAG_NAME, "ul")
    headers = container.find_elements(By.TAG_NAME, "h2")

    df = pd.DataFrame(columns=["Name", "Description", "Clan", "Generation", "Link"])

    for header in headers: 
        if header.text == "Q":
            headers.remove(header)

    for list in zip(lists[1:], headers[1:]): #skip the reference list
    
        minor_chars = list[0].find_elements(By.TAG_NAME, 'li')
        letter = list[1].text

        for char in minor_chars:
            #print(char.text)
            name = char.find_element(By.TAG_NAME, 'b').text.lower()
            description = char.text.lower()
            link = "https://whitewolf.fandom.com/wiki/Minor_characters_in_WoD#" + letter

            clan = parse_the_clan(description)

            generation = parse_the_generation(description)

            df.loc[len(df)] = [name, description, clan, generation, link]


        
        #print(df.head())

    df.to_csv("data_updated/minor_characters.csv")
    driver.quit()

def parse_main_page(link_list):

    chars = []

    for link in link_list:

        driver.get(link)

        chars.append(parse_vampire_page(driver))

    antediluvians = pd.DataFrame(chars)
    
    antediluvians.loc[antediluvians["Name"] == "Lasombra Antediluvian", "Sire_Link"] = "https://whitewolf.fandom.com/wiki/Irad"
    antediluvians.loc[antediluvians["Name"] == "Ennoia","Sire_Link"] = "https://whitewolf.fandom.com/wiki/Enoch"

    antediluvians.to_csv("data/antediluvians.csv")

    driver.quit()
    
        

title_page_links = ["https://whitewolf.fandom.com/wiki/Caine",
                    "https://whitewolf.fandom.com/wiki/Irad",
                    "https://whitewolf.fandom.com/wiki/Zillah",
                    "https://whitewolf.fandom.com/wiki/Enoch",
                    "https://whitewolf.fandom.com/wiki/Brujah_Antediluvian",
                    "https://whitewolf.fandom.com/wiki/Cappadocius",
                    "https://whitewolf.fandom.com/wiki/Ennoia",
                    "https://whitewolf.fandom.com/wiki/Haqim",
                    "https://whitewolf.fandom.com/wiki/Lasombra_Antediluvian",
                    "https://whitewolf.fandom.com/wiki/Malkav",
                    "https://whitewolf.fandom.com/wiki/Absimiliard",
                    "https://whitewolf.fandom.com/wiki/Ravnos_Antediluvian",
                    "https://whitewolf.fandom.com/wiki/Saulot",
                    "https://whitewolf.fandom.com/wiki/Set_(VTM)",
                    "https://whitewolf.fandom.com/wiki/Toreador_Antediluvian",
                    "https://whitewolf.fandom.com/wiki/Tzimisce_Antediluvian",
                    "https://whitewolf.fandom.com/wiki/Ventrue_Antediluvian"]

parse_main_page(title_page_links)

#parse_minor()
#parse_categories()


#driver.get("https://whitewolf.fandom.com/wiki/Leslie_Taylor")
#driver.get("https://whitewolf.fandom.com/wiki/Red_Meg")


#print(parse_vampire_page(driver))

#driver.quit()