from github import Github
import requests_cache
from requests_cache.backends.sqlite import SQLiteCache
from concurrent.futures import ThreadPoolExecutor

gh = Github()
repo = gh.get_repo("lazka/test-cache")
release = repo.get_release("test")
urls = [a.browser_download_url for a in release.assets]

session = requests_cache.CachedSession(
        always_revalidate=True,
        cache_control=False,
        expire_after=requests_cache.EXPIRE_IMMEDIATELY,
        backend=SQLiteCache('http_cache.sqlite')
)

def download_file(url):
    print(url)
    session.get(url)
    return url

while 1:
    # this deadlocks eventually
    with ThreadPoolExecutor(8) as executor:
        for x in executor.map(download_file, urls):
            pass
