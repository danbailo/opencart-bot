from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

chrome_options = ChromeOptions()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--ignore-certificate-errors')

driver = Remote(
    command_executor='http://127.0.0.1:4444',
    desired_capabilities=DesiredCapabilities.CHROME,
    options=chrome_options
)

driver.get('https://open93.com/#/login')

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Please enter username"]')))

driver.find_element(By.XPATH, '//input[@placeholder="Please enter username"]').send_keys('danbailo')
driver.find_element(By.XPATH, '//input[@placeholder="Please enter login password"]').send_keys('22418267BAIGON')
driver.find_element(By.XPATH, '//button[@class="sumbitBtn"]').click()

XPATH_LOADER = '//div[@class="loading_wrap van-loading van-loading--circular"]'

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XPATH_LOADER)))

element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//i[@class="van-icon van-icon-close"]')))
element.click()

driver.find_element(By.XPATH, '//div[@class="grab_wrap"]').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XPATH_LOADER)))

while True:
    driver.find_element(By.XPATH, '//span[@class="bg-blue" and contains(text(), "Automatic grab")]').click()
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Pending")]')))
    submit_order = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//span[@class="btn submit"]')))
    submit_order.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="van-toast__text" and contains(text(), "Order completed")]')))
    WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.XPATH, '//div[@class="van-toast__text" and contains(text(), "Order completed")]')))
