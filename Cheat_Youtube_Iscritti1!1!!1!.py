from selenium import webdriver
PATH = r'C:\Users\Manu\Desktop\Tutto\App\chromedriver.exe'
url = 'https://www.youtube.com'
driver = webdriver.Chrome(PATH)

driver.get(url)