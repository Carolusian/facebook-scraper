import logging
from facebook_scraper import get_posts, set_proxy

logging.basicConfig(level=logging.DEBUG, filename="sample_scraper.log")


def main():
    # uncomment and use a valid proxy url here
    # proxy_url = ""
    # set_proxy(proxy=PROXY_URL, verify=False)
    for post in get_posts(account="Xiaomihongkong", pages=10):
        print(post)


if __name__ == "__main__":
    main()
