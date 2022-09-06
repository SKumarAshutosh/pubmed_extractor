import json
import dotenv
import os
import sys
import requests
import xml
import pandas as pd
from tqdm import tqdm
from tabulate import tabulate
from bs4 import BeautifulSoup as bs
#from pmids_extract_solr import pmids_solr_list
from dotenv import load_dotenv

load_dotenv()
#environment variable
# API_KEY = os.getenv("API_KEY")
API_KEY = "9446fd13127051ca7343c2018204779d8007"
##
def author_details(pmid):
    keyword = pmid
    esearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term="
    # covid19&usehistory=true&webenv=true&retmax=10&api_key=9446fd13127051ca7343c2018204779d8007"
    search_resp = requests.get(esearch + keyword + "&usehistory=true&webenv=true" + "api_key=" + API_KEY)
    search_soup = bs(search_resp.content, features="lxml")
    if search_soup:
        # print(search_soup)
        webenv = search_soup.find("webenv")
        if webenv:
            webenv = webenv.text
            # print(webenv)
            count = search_soup.find("count").text
            print(count)
            batch_size = 2000
            batches = []
            for batch in range(0, int(count), 2001):
                efetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key=1&webenv="
                fetch_resp = requests.get(
                    efetch + webenv + "&rettype=xml&api_key=" + API_KEY + "&retmode=xml&retmax=2000&retstart=" + str(
                        batch))
                fetch_soup = bs(fetch_resp.content, features="lxml")
                articles_list = []
                PubmedArticleSet = fetch_soup.find("pubmedarticleset")
                if PubmedArticleSet:
                    articles = PubmedArticleSet.find_all("pubmedarticle")
                    for article in articles:
                        article_dict = {}
                        title = article.find("articletitle").text
                        pmid = article.find("pmid").text
                        authors = article.find("authorlist")
                        abstract = article.find("abstract")
                        author_list = []
                        try:
                            author_l = authors.find_all("author")
                        except AttributeError:
                            break
                        for auth in author_l:
                            author_dict = {}
                            try:
                                first_name = auth.find("forename").text
                            except:
                                first_name = ""
                            try:
                                second_name = auth.find("lastname").text
                            except:
                                second_name = ""
                            try:
                                initials = auth.find("initials").text
                            except:
                                initials = ""
                            author_name = initials + " " + first_name + " " + second_name
                            try:
                                affiliation = auth.find("affiliation").text
                            except:
                                affiliation = ""
                            author_dict["author_name"] = author_name
                            author_dict["initials_name"] = initials
                            author_dict["forename_name"] = first_name
                            author_dict["last_name"] = second_name
                            author_dict["affiliation"] = affiliation
                            author_list.append(author_dict)
                        article_dict["title"] = title
                        article_dict["pmid"] = pmid
                        article_dict["author"] = author_list
                        article_dict["abstract"] = abstract
                        batches.append(article_dict)

            if batches:
                df = pd.DataFrame(batches)
                df.columns = ['title', 'pmid', 'author','abstract']
                # ref:https://stackoverflow.com/questions/63875682/pandas-dataframe-splitting-a-column-with-dict-values-into-columns
                #  explode the list
                df = df.explode('author').reset_index(drop=True)
                # now fill the NaN with an empty dict
                df.author = df.author.fillna({i: {} for i in df.index})
                # then normalize the column
                df = df.join(pd.json_normalize(df.author))
                # drop the column
                df.drop(columns=['author'], inplace=True)
                # droping duplicates
                dff = df.drop_duplicates()
                return dff


def my_function(pmid_item):
    results = pd.DataFrame()
    for x in pmid_item:
        df = author_details(x)
        results = pd.concat([results, df], axis=0).reset_index(drop=True)
    print(tabulate(results, headers='keys', tablefmt='psql'))
    # print(results)
#results.to_csv('/mnt4/aims/KOL_network/Author_name_disambiguation/author_details.csv')



#alist = pmids_solr_list

# my_function("Covid")

# author_details("Covid")