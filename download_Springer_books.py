#!/usr/bin/env python3

# download your chrome driver according to your Google Chrome version
# https://chromedriver.storage.googleapis.com/index.html?path=81.0.4044.69/

# springer books
# https://link.springer.com/search?facet-content-type=%22Book%22&sortOrder=newestFirst&showAll=true&package=mat-covid19_textbooks

import pathlib
import os
import requests
import logging
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_destination_folder():
    current_folder = pathlib.Path().absolute()
    destination_folder = "DownloadedBooks"
    destination_path = current_folder / destination_folder
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)


# if the element identified by xpath_to_find exists in the url: 
#   the function will return an object pointing to the element
# else: 
#   it will return None indicating that the element doesn't exist
def try_to_get_element_by_xpath(driver, xpath_to_find, url):
    try:
        my_element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath_to_find)))
        return my_element
    except selenium.common.exceptions.TimeoutException as e:
        logging.warning(f"{type(e)} raised when looking for this XPath: {xpath_to_find}, in this url: {url}")
        return None


def simulate_download_of_book(driver, url_of_book_details_page, i):
    book_title, download_url = get_download_url_from_book_details_page(driver, url_of_book_details_page)

    response = requests.get(download_url)
    response_code = response.status_code

    if response_code == 200:
        logging.info(f"In Url {url_of_book_details_page}. The book {i}: {book_title} can be downloaded.")
    else:
        logging.error(
            f"Response of Get Request is {response_code} when performing GET over {download_url}. Url extracted from the book {i}, details page url: {url_of_book_details_page} of the book {book_title}")

    return response_code


def get_download_url_from_book_details_page(driver, url_of_book_details_page):
    driver.get(url_of_book_details_page)
    title_xpath = "//*[@id='main-content']/article[1]/div/div/div[1]/div/div/div[1]/div[2]/h1"
    book_title_element = try_to_get_element_by_xpath(driver, title_xpath, url_of_book_details_page)
    book_title = book_title_element.get_attribute('innerHTML').replace(" ", "_")

    download_button_xpath = "//*[@id='main-content']/article[1]/div/div/div[2]/div[1]/a"
    download_button_element = try_to_get_element_by_xpath(driver, download_button_xpath, url_of_book_details_page)
    if download_button_element is None:
        download_button_xpath = "//*[@id='main-content']/article[1]/div/div/div[2]/div/div/a"
        download_button_element = try_to_get_element_by_xpath(driver, download_button_xpath, url_of_book_details_page)
    download_url = download_button_element.get_attribute('href')
    return book_title, download_url


def simulate_download_of_first_n_books(driver, main_webPage_url, n=200):
    responses_to_return = []

    books_urls = get_first_n_books_urls_from_webPage(driver, main_webPage_url, n)

    counter = 0
    for i, main_webPage_url in enumerate(books_urls):
        response_code = simulate_download_of_book(driver, main_webPage_url, i)
        responses_to_return.append(response_code)
        counter += 1
        if counter >= n:
            return responses_to_return
    return responses_to_return


def get_first_n_books_urls_from_webPage(driver, main_webPage_url, n=200):
    counter = 0
    driver.get(main_webPage_url)
    books_urls = []
    for i in range(1, 11):
        book_link_xpath = f"//*[@id='results-list']/li[{i}]/div[2]/h2/a"
        my_element = try_to_get_element_by_xpath(driver, book_link_xpath, main_webPage_url)
        link_url = my_element.get_attribute('href')
        books_urls.append(link_url)
        logging.info(f"Book {counter} with url {link_url} appended to list of urls to simulate download")
        counter += 1
        if counter >= n:
            return books_urls

    right_arrow_xpath = f"//*[@id='kb-nav--main']/div[3]/form/a/img"
    right_arrow = try_to_get_element_by_xpath(driver, right_arrow_xpath, main_webPage_url)

    while right_arrow is not None:
        right_arrow.click()

        for i in range(1, 11):
            my_element = try_to_get_element_by_xpath(driver, book_link_xpath, main_webPage_url)
            link_url = my_element.get_attribute('href')
            books_urls.append(link_url)
            logging.info(f"Book {counter} with url {link_url} appended to list of urls to simulate download")
            counter += 1
            if counter >= n:
                return books_urls

        right_arrow_xpath = f"//*[@id='kb-nav--main']/div[3]/form/a[2]/img"
        right_arrow = try_to_get_element_by_xpath(driver, right_arrow_xpath, main_webPage_url)

    return books_urls


def download_book_from_url(driver, url_of_book_details_page):
    book_title, download_url = get_download_url_from_book_details_page(driver, url_of_book_details_page)

    current_folder = pathlib.Path().absolute()
    destination_folder = "DownloadedBooks"
    destination_path = current_folder / destination_folder
    destination_name = book_title + ".pdf"

    if not os.path.exists(destination_path / destination_name):
        with open(destination_path / destination_name, 'wb') as f:
            response = requests.get(download_url)
            f.write(response.content)
            f.close()


def download_books_from_file_containing_urls(driver, file_name_that_contains_urls):
    unique_urls = set()
    with open(file_name_that_contains_urls) as f:
        for url in f:
            if url not in unique_urls:
                unique_urls.add(url)
                download_book_from_url(driver, url)


def main():
    logging.basicConfig(level=logging.INFO)

    create_destination_folder()

    driver = webdriver.Chrome('./chromedriver')
    download_books_from_file_containing_urls(driver, "input.txt")

    driver.close()


if __name__ == "__main__":
    main()
