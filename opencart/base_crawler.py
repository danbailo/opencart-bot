from dataclasses import dataclass, field


from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from env_var import get_env_var


@dataclass
class BaseCrawler:
    url: str = field(default=get_env_var('URL_LOGIN'), init=False)

    def __init__(self):
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--ignore-certificate-errors')

        self.driver = Remote(
            command_executor=get_env_var('CHROME_PATH'),
            desired_capabilities=DesiredCapabilities.CHROME,
            options=chrome_options
        )

    def _check_if_form_is_on_screen(self, xpath_login: str):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath_login)
            )
        )

    def _wait_for_loader(self):
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
