import logging
from facebook_scraper import get_posts, set_proxy

logging.basicConfig(level=logging.DEBUG, filename="sample_scraper.log")


def main():
    # uncomment and use a valid proxy url here
    print("proxy is used.")
    proxy_server = "proxy.packetstream.io"
    proxy_user = "hyperlab"
    proxy_password = "XRL7J06udwDCiqkA"
    proxy_port = 31112
    proxy_url = f"http://{proxy_user}:{proxy_password}@{proxy_server}:{proxy_port}"
    set_proxy(proxy=proxy_url, verify=False)
    for post in get_posts(account="medicalinspire", pages=100):
        print(post)


if __name__ == "__main__":
    main()
