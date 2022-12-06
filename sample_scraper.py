import argparse
import logging
import random

from facebook_scraper import get_posts, set_proxy

logging.basicConfig(level=logging.DEBUG, filename="sample_scraper.log")


def get_proxy(proxy: str) -> str:
    if proxy == "proxyrack":
        PROXY_SERVER = "private.residential.proxyrack.net"
        PROXY_USER = "hyperlab"
        PROXY_PASSWORD = "3668c4-2190dd-330488-8edf6c-8279c9"
        PROXY_PORT_RANGE = (10000, 10004)
    elif proxy == "proxycheap":
        PROXY_SERVER = "proxy.proxy-cheap.com"
        PROXY_USER = "jnyuig0v"
        PROXY_PASSWORD = "0Wcz1abjXbg7ZFp7"
        PROXY_PORT_RANGE = (31112, 31112)
    elif proxy == "packetstream":
        PROXY_SERVER = "proxy.packetstream.io"
        PROXY_USER = "hyperlab"
        PROXY_PASSWORD = "XRL7J06udwDCiqkA"
        PROXY_PORT_RANGE = (31112, 31112)
    else:
        raise Exception("Unknown proxy")
    PROXY_PORT = random.randint(*PROXY_PORT_RANGE)
    PROXY_URL = f"http://{PROXY_USER}:{PROXY_PASSWORD}@{PROXY_SERVER}:{PROXY_PORT}"
    return PROXY_URL


def main():
    parser = argparse.ArgumentParser(
        prog='facebook-scraper',
        description="Scrape Facebook public pages without an API key",
    )
    parser.add_argument('account', type=str, help="Facebook account or group")
    parser.add_argument('-p', '--pages', type=int, help="Number of pages to download", default=10)
    parser.add_argument(
        '-x',
        '--proxy',
        type=str,
        choices=["proxyrack", "packetstream", "proxycheap"],
        help="Choose the proxy",
    )

    args = parser.parse_args()

    print(
        f"calling get_posts(account={args.account}, pages={args.pages}) with proxy {args.proxy}"
    )
    if args.proxy:
        set_proxy(proxy=get_proxy(args.proxy), verify=False)
    for post in get_posts(account=args.account, pages=args.pages):
        print(post)


if __name__ == "__main__":
    main()
