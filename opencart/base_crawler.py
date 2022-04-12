from dataclasses import dataclass, field


from selenium.webdriver import Remote, ChromeOptions, Chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


from get_env_var import get_env_var


@dataclass
class BaseCrawler:
    url: str = field(default=get_env_var('URL_LOGIN'), init=False)
    finish_day_orders: bool = field(default=False, init=False)

    def __post_init__(self):
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--ignore-certificate-errors')

        self.driver = Remote(
            command_executor=get_env_var('CHROME_PATH'),
            desired_capabilities=DesiredCapabilities.CHROME,
            options=chrome_options
        )

        self.driver.get(self.url)
