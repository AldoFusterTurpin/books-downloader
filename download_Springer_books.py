#!/usr/bin/env python3

# download your chrome dirver acording to your Google Chrome version
# https://chromedriver.storage.googleapis.com/index.html?path=81.0.4044.69/

# springer books
# https://link.springer.com/search?facet-content-type=%22Book%22&sortOrder=newestFirst&showAll=true&package=mat-covid19_textbooks

import pathlib
import os
import requests

import logging
logging.basicConfig(level=logging.INFO)

import selenium
from selenium import webdriver


def simulate_download_of_book(driver, url_of_book_details_page):
    driver.get(url_of_book_details_page)

    title_xpath = "//*[@id='main-content']/article[1]/div/div/div[1]/div/div/div[1]/div[2]/h1"
    book_title_element = try_to_get_element_by_xpath(driver, title_xpath, url_of_book_details_page)
    book_title = book_title_element.get_attribute('innerHTML').replace(" ", "_")

    download_button_element = None
    xpath_to_find = "//*[@id='main-content']/article[1]/div/div/div[2]/div[1]/a"
    download_button_element = try_to_get_element_by_xpath(driver, xpath_to_find, url_of_book_details_page)
    if download_button_element is None:        
        xpath_to_find = "//*[@id='main-content']/article[1]/div/div/div[2]/div/div/a"
        download_button_element = try_to_get_element_by_xpath(driver, xpath_to_find, url_of_book_details_page)
    
    download_url = download_button_element.get_attribute('href')

    response = requests.get(download_url)
    if response.status_code == 200:
        logging.info(f"In Url {url_of_book_details_page} everything is okay")
    else:
        logging.error(f"Can't get url {download_url} in the book detail page: {url_of_book_details_page}")


def simulate_download_of_books(driver, url):
    driver.get(url)
    # for i in range(1, 11):
    i = 1
    xpath_to_find = f"//*[@id='results-list']/li[{i}]/div[2]/h2/a"
    my_element = try_to_get_element_by_xpath(driver, xpath_to_find, url)
    url_of_book_details_page = my_element.get_attribute('href')
    simulate_download_of_book(driver, url_of_book_details_page)



# if the element identified by xpath_to_find exists in the url: 
#   returns True
# else: 
#   returns False
def does_exist_element_identified_by_xpath(driver, xpath_to_find, url):
    try :
        my_element = driver.find_element_by_xpath(xpath_to_find)
        return True
    except selenium.common.exceptions.NoSuchElementException as e:
        logging.warning(f"{type(e)} raised when looking for this XPath: {xpath_to_find}, in this url: {url}")
        return False


# if the element identified by xpath_to_find exists in the url: 
#   the function will return an object pointing to the element
# else: 
#   it will return None indicating that the element doesn't exist
def try_to_get_element_by_xpath(driver, xpath_to_find, url):
    my_element = None
    try :
        my_element = driver.find_element_by_xpath(xpath_to_find)
    except selenium.common.exceptions.NoSuchElementException as e:
        logging.warning(f"{type(e)} raised when looking for this XPath: {xpath_to_find}, in this url: {url}")
    finally:
        return my_element


def download_book_from_url(driver, url_of_book_details_page):
    driver.get(url_of_book_details_page)

    title_xpath = "//*[@id='main-content']/article[1]/div/div/div[1]/div/div/div[1]/div[2]/h1"
    book_title_element = try_to_get_element_by_xpath(driver, title_xpath, url_of_book_details_page)
    book_title = book_title_element.get_attribute('innerHTML').replace(" ", "_")

    download_button_element = None
    xpath_to_find = "//*[@id='main-content']/article[1]/div/div/div[2]/div[1]/a"
    download_button_element = try_to_get_element_by_xpath(driver, xpath_to_find, url_of_book_details_page)
    if download_button_element is None:        
        xpath_to_find = "//*[@id='main-content']/article[1]/div/div/div[2]/div/div/a"
        download_button_element = try_to_get_element_by_xpath(driver, xpath_to_find, url_of_book_details_page)
    
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


def download_books_from_file_containing_urls(driver, file_name_that_contains_urls):
    unique_urls = set()
    with open(file_name_that_contains_urls) as f:
        for url in f:
            if url not in unique_urls:
                unique_urls.add(url)
                download_book_from_url(driver, url)


def main(): 
    # create_destination_folder()

    driver = webdriver.Chrome('./chromedriver')

    # file_name_that_contains_urls = "input.txt"
    # download_books_from_file_containing_urls(driver, file_name_that_contains_urls)

    simulate_download_of_books(driver, "https://link.springer.com/search?facet-content-type=\"Book\"&sortOrder=newestFirst&showAll=true&package=mat-covid19_textbooks")
    
    driver.close()


if __name__ == "__main__":
   main()
