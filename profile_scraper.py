import email
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

    service = Service(paths.service)

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
    company_list = []
    address_list = []
    phone_list = []
    mobile_list = []
    email_list = []
    website_list = []
    state_list = []
    city_list = []

    browser = initialize_browser()

    browser.get('https://www.treesaregood.org/findanarborist/findanarborist')

    with open('input.csv') as f:
        reader = csv.DictReader(f)

        for line in reader:

            try:
                state = line['State']
                city = line['City']

                select_country = Select(browser.find_element(
                    By.ID, 'dnn_ctr437_FindAnArborist_ddl_strCountry'))

                # Select a country
                select_country.select_by_value('UNITED STATES')

                print(f"Extracting arborist for {state} - {city}")

                select_state = Select(browser.find_element(
                    By.ID, 'dnn_ctr437_FindAnArborist_ddl_strStateProv'))

                # Select a state
                select_state.select_by_value(state)

                time.sleep(5)

                select_city = Select(browser.find_element(
                    By.ID, 'dnn_ctr437_FindAnArborist_ddl_strCity'))

                # Select a city
                select_city.select_by_value(city)

                time.sleep(5)

                search_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                    (By.ID, 'dnn_ctr437_FindAnArborist_btnLocationSearch')))

                search_button.click()

                time.sleep(5)

                record = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                    (By.ID, 'dnn_ctr437_FindAnArborist_lblSearchCount')))

                clean_prefix = re.sub(r"returned ", "", record.text)
                clean_suffix = re.sub(r" records", "", clean_prefix)

                entry_count = int(clean_suffix)
                current_entry = 0

                while current_entry < entry_count:

                    print(f'Extracting {current_entry + 1} of {entry_count}')

                    link_id = "dnn_ctr437_FindAnArborist_GridViewFindAnArborist_linkbutton_SelectArborist_" + str(current_entry)

                    profile_link = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, link_id)))

                    profile_link.click()

                    time.sleep(10)

                    
                    try:
                        get_name = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'dnn_ctr437_FindAnArborist_lbl_strName')))
                        name_list.append(get_name.text if get_name != '' else 'None')
                    except:
                        name_list.append('Data unavailable')
                        pass

                    try:
                        get_ddress = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'dnn_ctr437_FindAnArborist_lbl_strAddress')))
                        address_list.append(get_ddress.text if get_ddress != '' else 'None')
                    except:
                        address_list.append('Data unavailable')
                        pass

                    try:
                        get_email = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'dnn_ctr437_FindAnArborist_lbl_strEmail')))
                        email_list.append(get_email.text if get_email != '' else 'None')
                    except:
                        email_list.append('Data unavailable')
                        pass

                    try:
                        get_company = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'dnn_ctr437_FindAnArborist_lbl_strCompany')))
                        company_list.append(get_company.text if get_company != '' else 'None')
                    except:
                        company_list.append('Data unavailable')
                        pass

                    try:
                        get_phone = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'dnn_ctr437_FindAnArborist_lbl_strPhone')))
                        phone_list.append(get_phone.text if get_phone != '' else 'None')
                    except:
                        phone_list.append('Data unavailable')
                        pass

                    try:
                        get_mobile = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'dnn_ctr437_FindAnArborist_lbl_strMobile')))
                        mobile_list.append(get_mobile.text if get_mobile != '' else 'None')
                    except:
                        mobile_list.append('An error occured while retrieving data')
                        pass

                    try:
                        get_website = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'dnn_ctr437_FindAnArborist_lbl_strWebsite')))
                        website_list.append(get_website.text if get_website != '' else 'None')
                    except:
                        website_list.append('An error occured while retrieving data')
                        pass

                    state_list.append(state)
                    city_list.append(city)

                    back_to_search = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'dnn_ctr437_FindAnArborist_btn_CloseArboristDetails')))
                    back_to_search.click()

                    current_entry += 1

                    time.sleep(5)

                back_to_location = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'dnn_ctr437_FindAnArborist_btn_CloseFindArboristOutput')))
                back_to_location.click()

                time.sleep(5)

            except:
                pass

    browser.quit()

    print('All assets finished downloading.\n')

    # Save scraped URLs to a CSV file
    now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
    print('Saving to a CSV file...')
    print(' ')
    data = {'State': state_list, 'City': city_list, 'Name': name_list, 'Company': company_list, 'Address': address_list, 'Phone': phone_list, 'Mobile': mobile_list, 'Email': email_list, 'Website': website_list}
    #data = {'Name': name_list, 'Address': address_list, 'Phone': phone_list, 'Email': email_list}
    df = pd.DataFrame(data=data)
    df.index += 1
    directory = os.path.dirname(os.path.realpath(__file__))
    filename = "Arborist" + now + ".csv"
    file_path = os.path.join(directory, 'arborist/', filename)
    df.to_csv(file_path)

    time_end = datetime.datetime.now().replace(microsecond=0)
    runtime = time_end - time_start
    print(f"Script runtime: {runtime}.\n")


if __name__ == '__main__':
    scraper()
