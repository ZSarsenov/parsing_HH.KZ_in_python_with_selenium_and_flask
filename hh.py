import csv
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
ITEMS = 50


# take last page of paginator
def take_last_page_paginator(url):
    browser.get(url)
    try:
        last_page = int(browser.find_elements(By.CLASS_NAME, 'pager-item-not-in-short-range')[3].find_element(By.CLASS_NAME, 'bloko-button').text)
    except IndexError:
        return 0
    return last_page


# pasring all data from every blocks
def extract_hh_jobs(last_page, url):
    data = []
    for page in range(last_page):
        print(f'parsing page - {page}')
        browser.get(f'{url}&page={page}')
        blocks = browser.find_elements(By.CLASS_NAME, 'vacancy-serp-item__layout') # take all blocks
        for block in blocks:
            title = block.find_element(By.TAG_NAME, 'a').text
            link = block.find_element(By.TAG_NAME, 'a').get_attribute('href')
            company = block.find_element(By.CLASS_NAME, 'vacancy-serp-item__meta-info-company').text
            location = block.find_element(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-address"]').text
            dict_data = {"title": title, "link": link, 'company': company, 'location': location}
            data.append(dict_data)
    return data


# save data to scv file
def save_data_to_csv(jobs):
    file = open('HeadHunter.csv', mode='w', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(["title", "link", 'company', 'location'])
    for job in jobs:
        writer.writerow(list(job.values()))


# call all methods of parsing
def get_jobs(keyword):
    url = f"https://aktau.hh.kz/search/vacancy?text={keyword}&items_on_page={ITEMS}"
    last_page = take_last_page_paginator(url) #take last page of paginator
    data = extract_hh_jobs(last_page, url) #pasring all data from every blocks
    save_data_to_csv(data) #save data to scv file
    return data