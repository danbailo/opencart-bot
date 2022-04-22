import click


from opencart.crawler import Crawler


@click.group()
def cli():
    pass


@cli.command()
@click.option('--user', required=True, type=str)
@click.option('--password', required=True, type=str)
@click.option('--use-driver/--no-use-driver', required=True, type=bool)
def execute(user: str, password: str, use_driver: bool):
    crawler = Crawler(use_driver=use_driver)

    crawler._login_user(user, password)
    crawler._access_grab_ad_page()
    while True:
        crawler._grab_ad()
        if crawler._finished_all_orders():
            break
        crawler._submit_order()
        crawler._check_if_order_has_submited()


if __name__ == '__main__':
    cli()