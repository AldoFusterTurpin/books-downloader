import unittest
from download_Springer_books import get_first_n_books_urls_from_webPage, simulate_download_of_first_n_books

from selenium import webdriver


class DownloadBooksTestSuite(unittest.TestCase):

    def test_can_reach_all_the_free_books_urls_from_Springer_main_WebPage(self):
        driver = webdriver.Chrome('./chromedriver')
        main_webPage_url = "https://link.springer.com/search?facet-content-type=\"Book\"&sortOrder=newestFirst&showAll=true&package=mat-covid19_textbooks"

        n = len(get_first_n_books_urls_from_webPage(driver, main_webPage_url, 200))
        self.assertEqual(n, 200)

    def test_simulate_download_of_first_3_books(self):
        driver = webdriver.Chrome('./chromedriver')
        main_webPage_url = "https://link.springer.com/search?facet-content-type=\"Book\"&sortOrder=newestFirst&showAll=true&package=mat-covid19_textbooks"

        responses = simulate_download_of_first_n_books(driver, main_webPage_url, 3)

        correct = True
        for response in responses:
            if response != 200:
                correct = False
                break

        self.assertEqual(correct, True)


if __name__ == "__main__":
    unittest.main()
