import requests
from logger import logger


def count_words_at_url(url):
    """counts word in url website"""
    resp = requests.get(url)
    logger.log("WORKER", "A worker completed its job!")
    return len(resp.text.split())
