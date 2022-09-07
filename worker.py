import time
import requests


def count_words_at_url(url):
    """counts word in url website"""
    time.sleep(15)
    resp = requests.get(url)
    return len(resp.text.split())
