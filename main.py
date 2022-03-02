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
   
  def test_title(self):
    mainPage = page.MainPage()
    assert mainPage.is_title_matches()
  
  def tearDown(self):
    self.driver.close()
    
if __name__ == "__main__":
  unittest.main()
