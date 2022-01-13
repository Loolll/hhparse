import argparse
import asyncio
import json
import sys
from typing import List

import aiohttp
import bs4

SETTINGS = {
    "LINK": "https://orenburg.hh.ru/search/vacancy?area=113&clusters=true&employment=full&enable_snippets=true&ored_clusters=true&professional_role=96&schedule=remote&text=python&order_by=publication_time&hhtmFrom=vacancy_search_list",
    "KEYWORD": "python",
    "PAGES": 1,
    "OUTPUT": "results.json"
}


def get_main_settings():
    """ Parses settings from CLI. """
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--link", required=False, help="Paste start link on the vacancies search")
    parser.add_argument("-p", "--pages", required=False, help="Write count of examined pages", type=int)
    parser.add_argument("-k", "--keyword", required=False, help="Keyword")
    parser.add_argument("-f", "--file", required=False, help="Path to result file")
    namespace = parser.parse_args(sys.argv[1:])
    SETTINGS["LINK"] = namespace.link or SETTINGS["LINK"]
    SETTINGS["PAGES"] = namespace.pages or SETTINGS["PAGES"]
    SETTINGS["KEYWORD"] = namespace.keyword or SETTINGS["KEYWORD"]
    SETTINGS["OUTPUT"] = namespace.file or SETTINGS["OUTPUT"]


async def get_vac_links(link):
    """ Gets links on specific vacancies.
        Result -> vacancies dictionary. """
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            html = await response.text()
            html = bs4.BeautifulSoup(html)
            vacs: List[bs4.BeautifulSoup] = html.find_all(name="div", attrs={"class": "vacancy-serp-item"})
            for vac in vacs:
                header = vac.find(name="a", attrs={"class": "bloko-link"})
                if SETTINGS['KEYWORD'].lower() in header.text.lower():
                    link = header.get('href', None)
                    vacancies[link] = {"header": header.text}


async def get_vac_details(link):
    """ Gets details of the concrete vacancy.
        Results -> vacancies dictionary. """
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            html = await response.text()
            soup = bs4.BeautifulSoup(html)
            data = {}
            data['salary'] = soup.find(name="div", attrs={"data-qa": "vacancy-salary"}).text
            data['date'] = soup.find(name="p", attrs={"class": "vacancy-creation-time"}).text
            data['text'] = soup.find(name="div", attrs={"class": "g-user-content"}).text
            data['experience'] = soup.find(name="span", attrs={"data-qa": "vacancy-experience"}).text
            data['tags'] = [x.text for x in soup.find_all(name="div",
                                                          attrs={
                                                              "data-qa": "bloko-tag bloko-tag_inline skills-element"})]
            vacancies[link].update(data)


loop = asyncio.get_event_loop()
tasks = []
vacancies = {}

# load settings
get_main_settings()

# get links on cur vacs
for page in range(SETTINGS["PAGES"]):  # forming tasks via looping through all pages
    tasks.append(loop.create_task(get_vac_links(SETTINGS["LINK"] + f"&page={page}")))
wait_tasks = asyncio.wait(tasks)
loop.run_until_complete(wait_tasks)

# get details of every cur vac
for link in vacancies:
    tasks.append(loop.create_task(get_vac_details(link)))
wait_tasks = asyncio.wait(tasks)
loop.run_until_complete(wait_tasks)

# save results
with open(SETTINGS["OUTPUT"], 'w') as file:
    json.dump(vacancies, file)

print(f"OK, total {len(vacancies)} vacancies")
