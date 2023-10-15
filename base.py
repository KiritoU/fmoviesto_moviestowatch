import json
import logging
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

from helper import helper
from moviestowatch import Moviestowatch
from settings import CONFIG

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
Path(CONFIG.COVER_SAVE_PATH).mkdir(parents=True, exist_ok=True)


class Crawler:
    def crawl_soup(self, url):
        logging.info(f"Crawling {url}")

        html = helper.download_url(url)
        soup = BeautifulSoup(html.content, "html.parser")

        return soup

    def get_episode_links(self, soup: BeautifulSoup) -> str:
        res = []
        player2 = soup.find("div", {"id": "player2"})
        if not player2:
            return res

        iframes = player2.find_all("iframe")
        if not iframes:
            return res

        for iframe in iframes:
            try:
                src = iframe.get("src", "")
                if src:
                    res.append(src)
            except Exception as e:
                print(e)

        return res

    def get_server_episodes_links(self, href, server_data_id) -> dict:
        res = {}
        soup = self.crawl_soup(href)
        list_episodes = soup.find("ul", class_="list-episodes")
        lis = list_episodes.find_all("li", class_="episode-item")
        for li in lis:
            episode_name = li.text.strip()
            episode_href = li.find("a").get("href")

            if not f"&server={int(server_data_id) + 1}" in episode_href:
                matches = re.search(r"&server=(\d+)&", episode_href)
                if matches:
                    episode_href = episode_href.replace(
                        matches.group(0), f"&server={int(server_data_id) + 1}&"
                    )
                # episode_href = episode_href.replace(
                #     f"&server={server_data_id}", f"&server={int(server_data_id) + 1}"
                # )
            episode_link = self.get_episode_link(href=episode_href)
            res[episode_name] = episode_link
        return res

    def get_episodes_data(
        self, href: str, post_type: str = CONFIG.TYPE_TV_SHOWS
    ) -> dict:
        soup = self.crawl_soup(href)
        res = {}

        try:
            if post_type == CONFIG.TYPE_TV_SHOWS:
                servers_list = soup.find("ul", {"id": "servers-list"})
                lis = servers_list.find_all("li")
                for li in lis:
                    a_element = li.find("a")
                    data_id = a_element.get("data-id")
                    server_href = a_element.get("href")
                    server_name = (
                        a_element.text.lower()
                        .replace("server", "")
                        .strip()
                        .capitalize()
                    )
                    res[data_id] = {
                        "name": server_name,
                        "episodes": self.get_server_episodes_links(
                            href=server_href, server_data_id=data_id
                        ),
                    }
            else:
                list_episodes = soup.find("ul", class_="list-episodes")
                lis = list_episodes.find_all("li", class_="episode-item")
                for li in lis:
                    server_name = (
                        li.text.lower().replace("server", "").strip().capitalize()
                    )
                    episode_link = self.get_episode_link(href=li.find("a").get("href"))
                    data_id = li.find("a").get("data-id")
                    res[data_id] = {
                        "name": server_name,
                        "episodes": {"movie_episode": episode_link},
                    }

        except Exception as e:
            helper.error_log(
                f"Failed to get_episodes_data. Href: {href}\n{e}",
                log_file="base.episodes.log",
            )

        return res

    def crawl_film(
        self,
        slug: str,
        href: str,
        post_type: str = CONFIG.TYPE_TV_SHOWS,
    ):
        soup = self.crawl_soup(href)
        m_i_detail = soup.find("div", class_="m_i-detail")

        title = helper.get_title(href=href, m_i_detail=m_i_detail)
        description = helper.get_description(href=href, m_i_detail=m_i_detail)

        cover_src = helper.get_cover_url(href=href, m_i_detail=m_i_detail)

        trailer_id = helper.get_trailer_id(soup)
        extra_info = helper.get_extra_info(m_i_detail=m_i_detail)

        if not title:
            helper.error_log(
                msg=f"No title was found. Href: {href}", log_file="base.no_title.log"
            )
            return

        film_data = {
            "title": title,
            "slug": slug,
            "description": description,
            "post_type": post_type,
            "trailer_id": trailer_id,
            "cover_src": cover_src,
            "extra_info": extra_info,
        }

        if post_type == CONFIG.TYPE_MOVIE:
            iframe = soup.find("iframe", {"id": "iframe-embed"})
            episodes_data = {"Episode 1": iframe.get("src", "")}
        else:
            episodes_data = {}
            myDIV = soup.find("div", {"id": "myDIV"})
            nav_items = myDIV.find_all("li", class_="nav-item")
            for nav_item in nav_items:
                ep_name = nav_item.text.strip("\n").strip()
                ep_link = nav_item.find("a").get("href", "")
                episodes_data[ep_name] = ep_link

        return film_data, episodes_data

    def crawl_entryBlock(
        self, entryBlock: BeautifulSoup, post_type: str = CONFIG.TYPE_TV_SHOWS
    ):
        try:
            href = entryBlock.find("a").get("href")

            if not href.startswith("https://"):
                href = CONFIG.FMOVIESTO_HOMEPAGE + href

            slug = href.strip().strip("/").split("/")[-1]

            film_data, episodes_data = self.crawl_film(
                slug=slug,
                href=href,
                post_type=post_type,
            )

            # film_data["episodes_data"] = episodes_data

            # with open("json/crawled.json", "w") as f:
            #     f.write(json.dumps(film_data, indent=4, ensure_ascii=False))

            Moviestowatch(film=film_data, episodes=episodes_data).insert_film()
            # sys.exit(0)
        except Exception as e:
            helper.error_log(
                msg=f"Error crawl_flw_item\n{e}", log_file="base.crawl_flw_item.log"
            )

    def crawl_page(self, url, post_type: str = CONFIG.TYPE_TV_SHOWS):
        soup = self.crawl_soup(url)

        entryBlocks = soup.find_all("div", class_="entryBlock")
        if not entryBlocks:
            return 0

        for entryBlock in entryBlocks:
            self.crawl_entryBlock(entryBlock=entryBlock, post_type=post_type)
            # break

        return 1


if __name__ == "__main__":
    # Crawler().crawl_page(url=CONFIG.FMOVIESTO_TVSHOWS_PAGE + "?page1")
    Crawler().crawl_page(
        url=CONFIG.FMOVIESTO_MOVIES_PAGE + "?page1", post_type=CONFIG.TYPE_MOVIE
    )
    # Crawler().crawl_page(url=CONFIG.TINYZONETV_MOVIES_PAGE, post_type=CONFIG.TYPE_MOVIE)
