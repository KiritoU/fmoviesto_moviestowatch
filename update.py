import logging
import time

from base import Crawler
from settings import CONFIG

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


crawler = Crawler()

if __name__ == "__main__":
    while True:
        try:
            crawler.crawl_page(f"{CONFIG.FMOVIESTO_TVSHOWS_PAGE}/")
            time.sleep(CONFIG.WAIT_BETWEEN_LATEST)
            crawler.crawl_page(
                f"{CONFIG.FMOVIESTO_MOVIES_PAGE}/", post_type=CONFIG.TYPE_MOVIE
            )
        except Exception as e:
            pass
        time.sleep(CONFIG.WAIT_BETWEEN_LATEST)
