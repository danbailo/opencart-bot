from pydantic import BaseModel

from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from .serializers.login_serializer import LoginSerializer


def check_if_form_is_on_screen(driver: Remote, xpath_login: str):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath_login)
        )
    )


def send_keys_from_serializer(driver: Remote, body: BaseModel):
    for xpath, value in body.dict(by_alias=True).items():
        element = driver.find_element(By.XPATH, xpath)
        element.send_keys(value)


def wait_for_loader(driver: Remote):
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((
            By.XPATH,
            '//div[@class="loading_wrap van-loading van-loading--circular"]')
        )
    )
    WebDriverWait(driver, 5).until_not(
        EC.presence_of_element_located((
            By.XPATH,
            '//div[@class="loading_wrap van-loading van-loading--circular"]')
        )
    )


def login_user(driver: Remote, user: str, password: str):
    body = LoginSerializer(
        user=user,
        password=password
    )
    check_if_form_is_on_screen(driver, body.return_alias_value(user))
    send_keys_from_serializer(driver, body)
    driver.find_element(By.XPATH, '//button[@class="sumbitBtn"]').click()
    wait_for_loader(driver)


def close_report_if_necessary(driver: Remote):
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//i[@class="van-icon van-icon-close"]')
            )
        )
        element.click()
    except TimeoutException:
        pass


def access_grab_ad_page(driver: Remote):
    close_report_if_necessary(driver)
    driver.find_element(By.XPATH, '//div[@class="grab_wrap"]').click()
    wait_for_loader(driver)


def grab_ad(driver: Remote):
    driver.find_element(
        By.XPATH,
        '//span[@class="bg-blue" and contains(text(), "Automatic grab")]'
    ).click()

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((
            By.XPATH, '//p[contains(text(), "Pending")]')
        )
    )
    submit_order = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((
            By.XPATH, '//span[@class="btn submit"]')
        )
    )
    submit_order.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH,
            '//div[@class="van-toast__text" and '
            'contains(text(), "Order completed")]')
        )
    )
    WebDriverWait(driver, 10).until_not(
        EC.presence_of_element_located((
            By.XPATH, '//div[@class="van-toast__text" and '
            'contains(text(), "Order completed")]')
        )
    )
