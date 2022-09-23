from os import name
import requests
import fake_useragent
from bs4 import BeautifulSoup
import time
import json

useragent = fake_useragent.UserAgent()

def get_links(text):
    data = requests.get(
        url=f"https://tyumen.hh.ru/search/vacancy?no_magic=true&L_save_area=true&text={text}&area=95&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&page=1",
        headers={"user-agent": useragent.random}
    )
    if data.status_code != 200:
        return
    page_content = BeautifulSoup(data.content, "lxml")
    try:
        page_count = int(page_content.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("span").find("span").text)
    except:
        return
    for page in range(page_count):
        try:
            data = requests.get(
                url=f"https://tyumen.hh.ru/search/vacancy?no_magic=true&L_save_area=true&text={text}&area=95&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&page={page}",
                headers={"user-agent": useragent.random}
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, "lxml")
            for a in soup.find_all("a", attrs={"class": "serp-item__title"}):
                yield f"{a.attrs['href'].split('?')[0]}"
        except Exception as e:
            print(f"{e}")
        time.sleep(1)


def get_vacancy(link):
    data = requests.get(
        url=link,
        headers={"user-agent": useragent.random},
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        salary = soup.find(attrs={"class": "bloko-header-section-2"}).text.replace("\u202f", "").replace("ООО\xa0", " ")\
            .replace("\xa0", " ")
    except:
        salary = ""
    try:
        name = soup.find(attrs={"class": "bloko-header-section-1"}).text
    except:
        name = ""
    resume = {
        "name": name,
        "salary": salary,
        "link": link,
    }
    return resume


if __name__ == "__main__":
        data = []
        for a in get_links("python"):
            data.append(get_vacancy(a))
            time.sleep(1)
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
