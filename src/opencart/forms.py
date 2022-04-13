from pydantic import BaseModel

from selenium.webdriver import Remote
from selenium.webdriver.common.by import By


def send_keys_from_serializer(driver: Remote, body: BaseModel):
    for xpath, value in body.dict(by_alias=True).items():
        element = driver.find_element(By.XPATH, xpath)
        element.send_keys(value)
