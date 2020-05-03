#!/usr/bin/env python3

# download your chrome dirver acording to your Google Chrome version
# https://chromedriver.storage.googleapis.com/index.html?path=81.0.4044.69/

# springer books
# https://link.springer.com/search?facet-content-type=%22Book%22&sortOrder=newestFirst&showAll=true&package=mat-covid19_textbooks

import pathlib
import os
import requests
from selenium import webdriver 


def download_book_from_url(driver, url_book_details_page):
    driver.get(url_book_details_page)

    title_xpath = "//*[@id='main-content']/article[1]/div/div/div[1]/div/div/div[1]/div[2]/h1"
    book_title_element = driver.find_element_by_xpath(title_xpath)
    book_title = book_title_element.get_attribute('innerHTML')
    old = " "
    new = "_"
    book_title = book_title.replace(old, new)

    download_button_xpath = "//*[@id='main-content']/article[1]/div/div/div[2]/div[1]/a"
    download_button_element = driver.find_element_by_xpath(download_button_xpath)
    download_url = download_button_element.get_attribute('href')

    the_book_pdf = requests.get(download_url)

    current_folder = pathlib.Path().absolute()
    destination_folder = "DownloadedBooks"
    destination_path = current_folder / destination_folder
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)

    destination_name = book_title + ".pdf"
    if not os.path.exists(destination_path / destination_name):
        with open(destination_path / destination_name, 'wb') as f:
            f.write(the_book_pdf.content)
            f.close()


def main(): 

    driver = webdriver.Chrome('./chromedriver')
    file_name = "input.txt"
    unique_urls = set()
    with open(file_name) as f:
        for url in f:
            if url not in unique_urls:
                unique_urls.add(url)
                download_book_from_url(driver, url)
    
    driver.close()


if __name__ == "__main__":
   main()
