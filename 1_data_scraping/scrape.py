import requests

from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import time
import pandas as pd
from os import path


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False

    if isinstance(element, Comment):
        return False
    return True

def text_from_url(url):
    html = urllib.request.urlopen("https://" + url).read()
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

df = pd.read_pickle("output/dedup_combined_df_2020_1_1_to_2021_7_1.pkl")
df = df.sample(frac=1)

for i, row in df.iterrows():
    f = "output/article_texts/" + row["guid"] + ".txt"
    #if not path.exists(f):
    if not path.exists(f) and not row["url"].startswith("kansascity.com") and not row["url"].startswith("huffingtonpost.com") and not row["url"].startswith("sacbee.com"):
        print("Downloading", i, row["url"], row["guid"])

        try:
            text = text_from_url(row["url"])
            file1 = open(f, "a")
            file1.write(text)
            file1.close()
            print("Success! Sleeping..", i, row["url"], row["guid"])
            time.sleep(2)

        except Exception as e:
            #print(e)
            pass
            print("Failed", i, row["url"], row["guid"])

    else:
        print("already exists", i, row["url"], row["guid"])