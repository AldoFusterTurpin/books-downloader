#!/usr/bin/env python3

# download your chrome dirver acording to your Google Chrome version
# https://chromedriver.storage.googleapis.com/index.html?path=81.0.4044.69/

# springer books
# https://link.springer.com/search?facet-content-type=%22Book%22&sortOrder=newestFirst&showAll=true&package=mat-covid19_textbooks

import pathlib
import os
import requests
import logging
import selenium
from selenium import webdriver


def try_to_get_element_by_xpath(driver, xpath_to_find, url_book_details_page):
    my_element = None
    try :
        my_element = driver.find_element_by_xpath(xpath_to_find)
    except selenium.common.exceptions.NoSuchElementException as e:
        logging.warning(f"{type(e)} raised when looking for this XPath: {xpath_to_find}, in this url: {url_book_details_page}")
    finally:
        return my_element


def download_book_from_url(driver, url_book_details_page):
    driver.get(url_book_details_page)

    title_xpath = "//*[@id='main-content']/article[1]/div/div/div[1]/div/div/div[1]/div[2]/h1"
    book_title_element = driver.find_element_by_xpath(title_xpath)
    book_title = book_title_element.get_attribute('innerHTML').replace(" ", "_")

    download_button_element = None
    xpath_to_find = "//*[@id='main-content']/article[1]/div/div/div[2]/div[1]/a"
    download_button_element = try_to_get_element_by_xpath(driver, xpath_to_find, url_book_details_page)
    if download_button_element is None:        
        xpath_to_find = "//*[@id='main-content']/article[1]/div/div/div[2]/div/div/a"
        download_button_element = try_to_get_element_by_xpath(driver, xpath_to_find, url_book_details_page)
    #     xpath_to_find = "//*[@id='main-content']/article[1]/div/div/div[2]/div/div/a/span[2]"
    #     download_button_element = driver.try_to_get_element_by_xpath(driver, xpath_to_find, url_book_details_page)
    
    download_url = download_button_element.get_attribute('href')

    current_folder = pathlib.Path().absolute()
    destination_folder = "DownloadedBooks"
    destination_path = current_folder / destination_folder
    destination_name = book_title + ".pdf"

    if not os.path.exists(destination_path / destination_name):
        with open(destination_path / destination_name, 'wb') as f:
            response = requests.get(download_url)
            f.write(response.content)
            f.close()


def create_destination_folder():
    current_folder = pathlib.Path().absolute()
    destination_folder = "DownloadedBooks"
    destination_path = current_folder / destination_folder
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)


def download_books_from_file_containing_urls(driver, file_name):
    unique_urls = set()
    with open(file_name) as f:
        for url in f:
            if url not in unique_urls:
                unique_urls.add(url)
                download_book_from_url(driver, url)


def main(): 
    create_destination_folder()

    driver = webdriver.Chrome('./chromedriver')

    file_name = "input.txt"
    download_books_from_file_containing_urls(driver, file_name)
    
    driver.close()


if __name__ == "__main__":
   main()
