from dataclasses import dataclass, field

import os
import os.path


from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Remote, Chrome, ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from env_var import get_env_var


@dataclass
class BaseCrawler:
    url: str = field(default=get_env_var('URL_LOGIN') or
                     'https://open93.com/#/login', init=False)

    # TODO: define web driver using a property
    def __init__(self, use_driver):
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")

        if use_driver:
            chrome_options.add_argument("--headless")
            self.driver = Chrome(
                executable_path=os.path.join(
                    '..', 'resources', 'chromedriver.exe' if os.name == 'nt'
                    else 'chromedriver'
                ),
                options=chrome_options
            )
        else:
            self.driver = Remote(
                command_executor=get_env_var('CHROME_PATH'),
                desired_capabilities=DesiredCapabilities.CHROME,
                options=chrome_options
            )

    def __del__(self):
        self.driver.quit()

    def _check_if_form_is_on_screen(self, xpath_login: str):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath_login)
            )
        )

    def _wait_for_loader(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//div[@class="loading_wrap van-loading '
                    'van-loading--circular"]')
                )
            )
            WebDriverWait(self.driver, 5).until_not(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//div[@class="loading_wrap van-loading '
                    'van-loading--circular"]')
                )
            )
        except TimeoutException:
            self.driver.implicitly_wait(1)
