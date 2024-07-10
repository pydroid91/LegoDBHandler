import os
import requests
import gzip


"""
Downloads .csv.gz archives from https://rebrickable.com/downloads/ and unpacks them into ../data/ folder.
"""


def download(item):
    url = f"https://cdn.rebrickable.com/media/downloads/{item}.csv.gz"
    response = requests.get(url)
    path = "../data/" + url.split('/')[-1]
    with open(path, mode="wb") as file:
        file.write(response.content)
    file.close()


def unpack(item):
    filename = f"../data/{item}.csv.gz"
    with gzip.open(filename, mode="rb") as archive,\
         open(filename[:-3], mode="wb") as csv:
        csv.write(archive.read())
    archive.close()
    csv.close()
    os.remove(filename)


def collect_csv():
    for db_item in ["themes", "colors", "inventories", "sets", "inventory_parts"]:
        download(db_item)
        unpack(db_item)
