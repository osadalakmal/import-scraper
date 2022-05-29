#!/bin/env python3

import requests
from bs4 import BeautifulSoup
import urllib
from camelot import read_pdf
import pandas as pd
import fnmatch


def check_file_exists(file):
    """Make sure a file exists if not throw exception"""
    try:
        with open(file):
            pass
    except FileNotFoundError:
        return False
    return True


def extract_links_from_html():
    """Return the set of links that contain the pdf files for hs codes. This includes section files as well
    but for the moment I am just returning these"""
    return [
        None
        if item is None
        else root + item[0]["href"]
        if root not in item[0]["href"]
        else item[0]["href"]
        for item in [
            item.findChildren("a", recursive=False)
            for item in soup.find_all("td", class_="htLeft htTop")
        ]
    ]


def download_files_if_not_already_present(dirname, links, name_filter):
    """This downloads a given set of links to given directory if they are not already present on disk"""
    files = []
    for link in links:
        filename = "./" + dirname + "/" + link.split("/")[-1]
        if (
            link is not None
            and fnmatch.fnmatch(filename, name_filter)
            and not check_file_exists(filename)
        ):
            print("Downloading: " + link)
            with open(filename, "wb") as file:
                file.write(requests.get(link).content)
        if link is not None and fnmatch.fnmatch(filename, name_filter):
            files.append(filename)
    return files


URL = "https://www.customs.gov.lk/customs-tariff/import-tariff/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
root = "{uri.scheme}://{uri.netloc}/".format(uri=urllib.request.urlparse(URL))

filenames = download_files_if_not_already_present(
    "pdfs", extract_links_from_html(), "*Ch*.pdf"
)

print("Working with " + filenames[0])
all_tables = read_pdf(filenames[0], pages="all")

# Show the total number of tables in the file
print("Total number of table: {}".format(all_tables.n))

# Combine all the tables to one
dfs = []
for t in range(all_tables.n):
    df = all_tables[t].df

    # Set the column names correctly
    df.columns = df.iloc[0]
    df.drop(df.index[0])

    # Filter the rows with empty HS Codes or table headers that have "HS Code" in that column
    df = df[df["HS Code"] != ""]
    df = df[df["HS Code"] != "HS Code"]
    dfs.append(df)

res_1 = pd.concat(dfs, ignore_index=True)
res_1.to_csv("result.csv")
