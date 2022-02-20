import base64
from typing import Dict, Optional
import requests
import json
import urllib.parse

from facebook_scraper import _scraper

GRAPHQL_URL = "https://www.facebook.com/api/graphql/"


def __get_proxy() -> Optional[Dict[str, str]]:
    if "proxies" in _scraper.requests_kwargs:
        return _scraper.requests_kwargs["proxies"]
    return None


def __request(url: str, data: str):
    proxy = __get_proxy()

    default_headers = {
        'Accept-Language': 'en-US,en;q=0.5',
        "Sec-Fetch-User": "?1",
        "sec-fetch-site": "same-origin",
        'x-fb-lsd': 'GoogleBot',
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = f"lsd=GoogleBot&__a=GoogleBot&{data}"
    if proxy:
        print("using proxy: " + str(proxy))
        response = requests.request(
            "POST", url, headers=default_headers, data=data, proxies=proxy
        )
    else:
        response = requests.request("POST", url, headers=default_headers, data=data)
    return response


def get_likes(doc_id: int, target_id: int, reaction_id: str):
    url = GRAPHQL_URL
    target = f"feedback:{target_id}"
    variables = {
        "feedbackTargetID": base64.b64encode(target.encode()).decode(),
        "reactionType": "LIKE",
        "reactionID": reaction_id,
        "stagesSessionID": None,
    }
    variables = urllib.parse.quote_plus(json.dumps(variables).replace(" ", ""))
    payload = f"variables={variables}&doc_id={doc_id}"
    response = __request(url, data=payload)
    return response.json()


def get_comments(doc_id: int, target_id: int):
    url = GRAPHQL_URL
    target = f"feedback:{target_id}"
    variables = {
        "UFI2CommentsProvider_commentsKey": "CometSinglePageContentContainerFeedQuery",
        "__false": False,
        "__true": True,
        "after": None,
        "before": None,
        "displayCommentsContextEnableComment": None,
        "displayCommentsContextIsAdPreview": None,
        "displayCommentsContextIsAggregatedShare": None,
        "displayCommentsContextIsStorySet": None,
        "displayCommentsFeedbackContext": None,
        "feedLocation": "PAGE_TIMELINE",
        "feedbackSource": 22,
        "first": 35,
        "focusCommentID": None,
        "includeHighlightedComments": False,
        "includeNestedComments": True,
        "initialViewOption": "RANKED_THREADED",
        "isInitialFetch": False,
        "isPaginating": True,
        "last": None,
        "scale": 2,
        "topLevelViewOption": None,
        "useDefaultActor": False,
        "viewOption": None,
        "id": base64.b64encode(target.encode()).decode(),
    }
    variables = urllib.parse.quote_plus(json.dumps(variables).replace(" ", ""))
    payload = f"variables={variables}&server_timestamps=true&doc_id={doc_id}"
    response = __request(url, data=payload)
    return response.json()


def get_reshares(doc_id: int, target_id: int):
    url = GRAPHQL_URL
    target = f"feedback:{target_id}"
    variables = {
        "feedbackTargetID": base64.b64encode(target.encode()).decode(),
    }
    variables = urllib.parse.quote_plus(json.dumps(variables).replace(" ", ""))
    payload = f"variables={variables}&doc_id={doc_id}"
    response = __request(url, data=payload)
    return response.json()
