import unittest
from selenium import webdriver
import page 
path = r'C:\Users\Manu\Desktop\Tutto\App\chromedriver.exe'
url = 'https://www.youtube.com'

class pythonOrgSearch(unittest.TestCase):
  
  def setUp(self):
    print("setup")
    self.driver = webdriver.Chrome(path)
    self.driver.get(url)
  
  def test_search_python(self):
    mainPage = page.MainPage(self.driver)
    assert mainPage.is_title_matches()
    mainPage.search_text_element = "pycon"
    mainPage.click_go_button()
    search_result_page = page.SearchResultPage(self.driver)
    assert search_result_page.is_results_found()
  
  def tearDown(self):
    self.driver.close()
    
if __name__ == "__main__":
  unittest.main()
