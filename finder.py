import requests
from bs4 import BeautifulSoup


def get_subs_channel(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 4.1.2; GT-P3100 Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.109 Safari/537.36",
    }
    r = requests.get(link, headers=headers)
    if r.status_code < 300:
        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for link in soup.find_all("a"):
            if link.get("href") is not None:
                links.append(link.get("href"))
        return [i for i in links if i.startswith("https://tlgrm.ru/channels/")]
    else:
        return None


def get_close_channel(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 4.1.2; GT-P3100 Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.109 Safari/537.36",
    }
    r = requests.get(link, headers=headers)
    if r.status_code < 300:
        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for link in soup.find_all("a"):
            if link.get("href") is not None:
                links.append(link.get("href"))
        return links
    else:
        return None


# result = get_subs_channel("https://tlgrm.ru/channels/@naebnet")[0]
# print(get_subs_channel(result))
