import requests


def count_words_at_url(url):
    """counts word in url website"""
    resp = requests.get(url)
    return len(resp.text.split())
