import unittest
from download_Springer_books import get_all_books_urls_from_webPage

from selenium import webdriver


class DownloadBooksTestSuite(unittest.TestCase):

    def test_can_reach_all_the_free_books_urls_from_Springer_main_WebPage(self):
        driver = webdriver.Chrome('./chromedriver')
        main_webPage_url = "https://link.springer.com/search?facet-content-type=\"Book\"&sortOrder=newestFirst&showAll=true&package=mat-covid19_textbooks"
        n = len(get_all_books_urls_from_webPage(driver, main_webPage_url))
        self.assertEqual(n, 200)


if __name__ == "__main__":
    unittest.main()
