from opencart.crawler import Crawler

from env_var import get_env_var


if __name__ == '__main__':
    crawler = Crawler()
    user = get_env_var('USER_LOGIN')
    password = get_env_var('PASSWORD')

    crawler._login_user(user, password)
    crawler._access_grab_ad_page()

    while True:
        crawler._grab_ad()
        if crawler._finished_all_orders():
            break
        crawler._submit_order()
        crawler._check_if_order_has_submited()
