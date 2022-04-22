from dataclasses import dataclass


from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from extensions.logger import logger

from .base_crawler import BaseCrawler

from .forms import send_keys_from_serializer

from .serializers.login_serializer import LoginSerializer

TIME_TO_WAIT = 20


@dataclass
class Crawler(BaseCrawler):

    def __post_init__(self):
        super().__init__()
        logger.debug('accessing target page')
        self.driver.get(self.url)

    def _login_user(self, user: str, password: str):
        logger.debug('logging in user')
        body = LoginSerializer(
            user=user,
            password=password
        )
        self._check_if_form_is_on_screen(body.return_alias_value(user))
        send_keys_from_serializer(self.driver, body)
        self.driver.find_element(
            By.XPATH, '//button[@class="sumbitBtn"]'
        ).click()
        self._wait_for_loader()
        logger.debug('user logged!\n')

    def _close_report_if_necessary(self):
        try:
            element = WebDriverWait(self.driver, TIME_TO_WAIT).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//i[@class="van-icon van-icon-close"]')
                )
            )
            element.click()
            logger.debug('report closed')
        except TimeoutException:
            pass

    def _access_grab_ad_page(self):
        self._close_report_if_necessary()
        logger.debug('accesing ad page\n')
        self.driver.find_element(By.XPATH, '//div[@class="grab_wrap"]').click()
        self._wait_for_loader()

    def _grab_ad(self):
        logger.debug('grabbing new ad')
        self.driver.find_element(
            By.XPATH,
            '//span[@class="bg-blue" and contains(text(), "Automatic grab")]'
        ).click()

    def _finished_all_orders(self):
        try:
            WebDriverWait(self.driver, TIME_TO_WAIT).until(
                EC.presence_of_element_located((
                    By.XPATH, '//div[contains(text(), '
                              '"You have completed all orders")]')
                )
            )
            logger.debug('completed all orders!')
            return True
        except TimeoutException:
            return False

    def _submit_order(self):
        logger.debug('submiting order')
        WebDriverWait(self.driver, TIME_TO_WAIT).until(
            EC.presence_of_element_located((
                By.XPATH, '//p[contains(text(), "Pending")]')
            )
        )
        self.driver.find_element(
            By.XPATH, '//span[@class="btn submit"]'
        ).click()

    def _check_if_order_has_submited(self):
        WebDriverWait(self.driver, TIME_TO_WAIT).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//div[@class="van-toast__text" and '
                'contains(text(), "Order completed")]')
            )
        )
        WebDriverWait(self.driver, TIME_TO_WAIT).until_not(
            EC.presence_of_element_located((
                By.XPATH, '//div[@class="van-toast__text" and '
                'contains(text(), "Order completed")]')
            )
        )
        logger.debug('order submited!\n')
