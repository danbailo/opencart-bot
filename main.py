from opencart.base_crawler import BaseCrawler
from opencart.actions import (
    login_user, access_grab_ad_page, finished_all_orders,
    submit_order, check_if_order_has_submited
)

from get_env_var import get_env_var


if __name__ == '__main__':
    crawler = BaseCrawler()
    user = get_env_var('USER_LOGIN')
    password = get_env_var('PASSWORD')

    login_user(crawler.driver, user, password)
    access_grab_ad_page(crawler.driver)

    while not finished_all_orders(crawler.driver):
        submit_order(crawler.driver)
        check_if_order_has_submited(crawler.driver)
