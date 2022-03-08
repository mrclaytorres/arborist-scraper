from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import urllib3
import ssl
import subprocess
import random
import pandas as pd
import datetime
import sys
import os
import os.path
import time
import csv
import re
import paths


def initialize_browser():

    # Chrome Options
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--start-maximized")
    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": paths.default_directory,
        "directory_upgrade": True}
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(paths.default_directory)

    browser = webdriver.Chrome(service=service, options=chrome_options)

    url = browser.command_executor._url

    session_id = browser.session_id

    print(f'{url}\n')
    print(f'{session_id}\n')

    #browser.session_id = '05A6484CF695076050314F602AEC3566'

    return browser


def scraper():

    time_start = datetime.datetime.now().replace(microsecond=0)

    name_list = []
    address_list = []
    phone_list = []
    state_list_csv = []
    city_list_csv = []

    state_list = ["AA","AK","AL","AP","AR","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","PR","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"]

    browser = initialize_browser()

    browser.get('https://www.treesaregood.org/findanarborist/findanarborist')

    try:

        select_country = Select(browser.find_element(
            By.ID, 'dnn_ctr437_FindAnArborist_ddl_strCountry'))

        # Select a country
        select_country.select_by_value('UNITED STATES')

        # Loop through all states
        for state in state_list:

            print(f"Extracting cities for {state}")

            select_state = Select(browser.find_element(
            By.ID, 'dnn_ctr437_FindAnArborist_ddl_strStateProv'))

            # Select a state
            select_state.select_by_value(state)

            time.sleep(5)

            #city_dropdown = Select(browser.find_element(By.ID, 'dnn_ctr437_FindAnArborist_ddl_strCity'))
            
            city_dropdown = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located(
                    (By.ID, 'dnn_ctr437_FindAnArborist_ddl_strCity'))
            )

            city_options = [x for x in city_dropdown.find_elements_by_tag_name("option")]

            for city in city_options:
                city_list_csv.append(city.get_attribute("value"))
                state_list_csv.append(state)

    except:
        pass

    browser.quit()

    print('All assets finished downloading.\n')

    # Save scraped URLs to a CSV file
    now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
    print('Saving to a CSV file...')
    print(' ')
    data = {"State": state_list_csv, 'City': city_list_csv}
    df = pd.DataFrame(data=data)
    df.index += 1
    directory = os.path.dirname(os.path.realpath(__file__))
    filename = "state_city_list" + now + ".csv"
    file_path = os.path.join(directory, 'csvfiles/', filename)
    df.to_csv(file_path)

    time_end = datetime.datetime.now().replace(microsecond=0)
    runtime = time_end - time_start
    print(f"Script runtime: {runtime}.\n")


if __name__ == '__main__':
    scraper()
