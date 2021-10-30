import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("facebook_scraper.log"),
        logging.StreamHandler()
    ]
)

import csv
import random
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Tuple
from enum import Enum
from urllib.parse import urlparse
from concurrent import futures
# from froxy import Froxy
from facebook_scraper import set_proxy, set_user_agent, get_posts


load_dotenv()


logger = logging.getLogger(__name__)


class FbType(Enum):
    PAGE = "page"
    GROUP = "group"


seed_urls = [
    "https://m.facebook.com/scmp/posts/",
    "https://m.facebook.com/standnewshkposts/",
    "https://m.facebook.com/hongkongfpposts/",
    "https://m.facebook.com/hketpage/posts/",
    "https://m.facebook.com/chinadailyhkedition/posts/",
    "https://m.facebook.com/sunwebhkposts/",
    "https://m.facebook.com/hkibcnews/posts/",
    "https://m.facebook.com/hkcnews/posts/",
    "https://m.facebook.com/thestandardhk/posts/",
    "https://m.facebook.com/timeouthk/posts/",
    "https://m.facebook.com/POLO-Hong-Kong-News-and-Updates-100248792291936/posts/",
    "https://m.facebook.com/hongkongnewsdaily/posts/",
    "https://m.facebook.com/hk01wemedia/posts/",
    "https://m.facebook.com/cnninternational/posts/",
    "https://m.facebook.com/realhknews/posts/",
    "https://m.facebook.com/RTHKEnglishNews/posts/",
    "https://m.facebook.com/yurikhy/posts/",
    "https://m.facebook.com/inmediahknet/posts/",
    "https://m.facebook.com/mingpaoinews/posts/",
    "https://m.facebook.com/OpenRiceHK/posts/",
    "https://m.facebook.com/travelnhk/posts/",
    "https://m.facebook.com/Reuters/posts/",
    "https://m.facebook.com/FoxNewsPolitics/posts/",
    "https://m.facebook.com/icable.news/posts/",
    "https://m.facebook.com/YahooHongKong/posts/",
    "https://m.facebook.com/hkdnracing/posts/",
    "https://m.facebook.com/YahooHKFinance/posts/",
    "https://m.facebook.com/HongKongPoliceForce/posts/",
    "https://m.facebook.com/EUOfficeHongKongMacao/posts/",
    "https://m.facebook.com/hongkongbk/posts/",
    "https://m.facebook.com/UKandHongKong/posts/",
    "https://m.facebook.com/hkmoa/posts/",
    "https://m.facebook.com/hk.observatory/posts/",
    "https://m.facebook.com/PakistanConsulateHongKongSAR/posts/",
    "https://m.facebook.com/hkairport.official/posts/",
    "https://m.facebook.com/hongkongballet/posts/",
    "https://m.facebook.com/hongkongsinfoniettaposts/",
    "https://m.facebook.com/groups/expathongkong/posts/",
    "https://m.facebook.com/groups/FindYourRoomInHongKong/posts/",
    "https://m.facebook.com/groups/livinginhongkong/posts/",
    "https://m.facebook.com/groups/406820049365242/posts/",
    "https://m.facebook.com/groups/139446906759464/posts/",
    "https://m.facebook.com/groups/LammaIslandGroup/posts/",
    "https://m.facebook.com/groups/1477218198968198/posts/",
    "https://m.facebook.com/groups/lammamarketplaceposts/",
    "https://m.facebook.com/groups/326752280722780/posts/",
    "https://m.facebook.com/groups/HongKongTrailRunning/posts/",
    "https://m.facebook.com/groups/176135783620354/posts/",
]

page_fields = ['post_id', 'text', 'post_text', 'shared_text', 'time', 'timestamp', 'image', 'image_lowquality', 'images', 'images_description', 'images_lowquality', 'images_lowquality_description', 'video', 'video_duration_seconds', 'video_height', 'video_id', 'video_quality', 'video_size_MB', 'video_thumbnail', 'video_watches', 'video_width', 'likes', 'comments', 'shares', 'post_url', 'link', 'links', 'user_id', 'username', 'user_url', 'is_live', 'factcheck', 'shared_post_id', 'shared_time', 'shared_user_id', 'shared_username', 'shared_post_url', 'available', 'comments_full', 'reactors', 'w3_fb_url', 'reactions', 'reaction_count', 'with', 'page_id', 'image_id', 'image_ids', 'was_live']
group_fields = ['post_id', 'text', 'post_text', 'shared_text', 'time', 'timestamp', 'image', 'image_lowquality', 'images', 'images_description', 'images_lowquality', 'images_lowquality_description', 'video', 'video_duration_seconds', 'video_height', 'video_id', 'video_quality', 'video_size_MB', 'video_thumbnail', 'video_watches', 'video_width', 'likes', 'comments', 'shares', 'post_url', 'link', 'links', 'user_id', 'username', 'user_url', 'is_live', 'factcheck', 'shared_post_id', 'shared_time', 'shared_user_id', 'shared_username', 'shared_post_url', 'available', 'comments_full', 'reactors', 'w3_fb_url', 'reactions', 'reaction_count', 'with', 'page_id', 'image_id', 'image_ids', 'was_live']

def get_user_agents() -> list[str]:
    with open("user-agents.txt") as f:
        user_agents = f.readlines()
    user_agents = [ua.strip() for ua in user_agents]
    return user_agents

user_agents = get_user_agents()


def get_proxies() -> list[str]:
    # froxy = Froxy()

    # def format_proxy(froxy_proxy: list[str]) -> str:
    #     return f"http://{froxy_proxy[0]}:{froxy_proxy[1]}"

    # return [format_proxy(p) for p in froxy.https()]
    pass


def pick_proxy(lst: list[str]) -> str:
    """pick a random proxy from list"""
    p = random.choice(lst)
    logger.info("Picked proxy: %s", p)
    return p


def pick_user_agent(lst: list[str]) -> str:
    """pick a random user agent from list"""
    p = random.choice(lst)
    logger.info("[user-agent] picked: %s", p)
    return p


def get_seed_type(seed_url: str) -> Tuple[FbType, str]:
    parsed = urlparse(seed_url).path.split("/")
    if "/groups/" in seed_url:
        return FbType.GROUP, parsed[-3]
    return FbType.PAGE, parsed[-3]


def download_page_posts(account: str, pages=10) -> bool:
    folder = "output/pages"
    Path(folder).mkdir(parents=True, exist_ok=True)

    with open(f"{folder}/{account}.csv", 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=page_fields)
        writer.writeheader()
        for p in get_posts(account=account, pages=pages):
            writer.writerow(p)
            set_user_agent(pick_user_agent(user_agents))

        return True


def download_group_posts(account: str, pages: int=10) -> bool:
    folder = "output/groups"
    Path(folder).mkdir(parents=True, exist_ok=True)

    with open(f"{folder}/{account}.csv", 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=group_fields)
        writer.writeheader()
        for p in get_posts(group=account, pages=pages):
            useless_keys = [k for k in p.keys() if k not in group_fields]
            for k in useless_keys:
                p.pop(k) 
            writer.writerow(p)
            set_user_agent(pick_user_agent(user_agents))

        return True


def download_posts(seed_url: str, pages: int=10) -> bool:
    t, page_or_group = get_seed_type(seed_url)
    if t == FbType.PAGE:
        return download_page_posts(page_or_group, pages)
    elif t == FbType.GROUP:
        return download_group_posts(page_or_group, pages)
    else:
        logger.error("incorrect FbType for %s" % t)
        return False


if __name__ == '__main__':
    # proxies = get_proxies()
    # set_proxy(pick_proxy(proxies))
    proxy = os.environ.get("PROXY_URL")
    set_proxy(proxy)

    set_user_agent(pick_user_agent(user_agents))

    with futures.ThreadPoolExecutor(max_workers=25) as executor:
        tasks = { executor.submit(download_posts, seed, 10000): seed for seed in seed_urls }
        for future in futures.as_completed(tasks):
            seed = tasks[future]
            try:
                data = future.result()
            except Exception as e:
                logger.error("%r generated an exception: %s" % (seed, e))
            else:
                logger.info("%r is downloaded" % seed)
        