# Import Tariff Scraper

This python script scrapes the pdf files off of the [customs site for import tariffs in sri lanka](https://www.customs.gov.lk/customs-tariff/import-tariff/) and attempts to create a CSV file of all the rates so people can actually make use of the data in those PDFs

The PDFs are an absolute nightmare to work with if you only need to find one rate. There is no index and the files are named by chapters. There is no central index as far as I can see

As a self respecting programmer when presented with such an issue, there is only one thing to do - Write a program to solve this!

So I went ahead and wrote a program that creates a CSV file from all the data. This is still a work in progress but it is a good place to start with if you want to learn about using python to automate tedious manual tasks on the web

I am using pandas for data processing and requests library for HTTP operations. I am also using beautiful soup library for scraping the HTML and parsing it.

To run the program use [venv](https://docs.python.org/3/library/venv.html) for virtual environment creation

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
./main.py
```
