from opencart.base_crawler import BaseCrawler
from opencart.actions import login_user, access_grab_ad_page, grab_ad

from get_env_var import get_env_var


if __name__ == '__main__':
    crawler = BaseCrawler()

    user = get_env_var('USER_LOGIN')
    password = get_env_var('PASSWORD')

    login_user(crawler.driver, user, password)

    access_grab_ad_page(crawler.driver)

    while crawler.finish_day_orders:
        grab_ad(crawler.driver)
        crawler.check_if_finish_day_orders()
