from bs4 import BeautifulSoup as bs
from bs4 import NavigableString
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import pandas as pd
from pandas import Series, DataFrame
from numpy import around
import os.path
import json

## indices and Graphs
major_indices = "https://uk.investing.com/indices/major-indices"
metals_indices = "https://uk.investing.com/commodities/metals"
commodities = "https://uk.investing.com/commodities/real-time-futures"
world_bonds = "https://uk.investing.com/rates-bonds/world-government-bonds"


## Main Websites
zerohedge = "https://www.zerohedge.com/"
investingUK = "https://uk.investing.com/"
wsj = "https://www.wsj.com/"
forbes = "https://www.forbes.com/#3284a16e2254"
investingUK_new = "https://uk.investing.com/news/latest-news"

## Central banks gold possession
boe_gold = "https://www.bankofengland.co.uk/statistics/gold"

# file that contains the list of coutries to search the bonds
COUNTRIES = os.path.join(os.getcwd(), 'countries.json') 
    


def get_news(latests= True, most_popular= False):
    ''' Shows the last 20 stories '''
    # print("NEW STORIES")
    ### Getting new stories from Uk Investing
    req = Request(investingUK_new, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = bs(html, "html.parser")
    
    column = soup.find("div", class_="largeTitle")
    articles = column.find_all("article", class_="js-article-item")
    span = column.find_all("span", class_ = "date")
    df = DataFrame(columns=["title", "link", "hour"]) 

    for idx,post in enumerate(articles):
        div = post.find("div", class_="textDiv")
        title = div.find("a").get("title")
        link = div.find("a").get("href")
        link = urljoin(investingUK, link)
        hour = span[idx].text
        df.loc[idx] = [title,link,hour]

        # print(div.contents)
        # print("Header: ", title)
        # print("Link: ", urljoin(investingUK, link))
        # print("Posted: ", hour, end="\n")  
        # print("\n")
    return df
  
def get_indices():
    req = Request(major_indices, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = bs(html, "html.parser")


    ## To get Major indices
    tb_indices = soup.select("table.genTbl.closedTbl.elpTbl.elp20.crossRatesTbl")

    for table in tb_indices:
       df = pd.read_html(table.prettify(), index_col = "Index")
       df = df[0]
       df.dropna(axis="columns", inplace=True)
       df.drop(columns=["Time"], inplace=True)
    #    print(df)
       return df

def get_commodities():
    req = Request(commodities,  headers={'User-Agent': 'Mozilla/5.0'})
    html  = urlopen(req).read()
    soup = bs(html, "html.parser")
    table = soup.find(id="cross_rate_1")
    df = pd.read_html(table.prettify(), index_col="Commodity")
    df = df[0]
    df.dropna(axis="columns", inplace=True)
    df.drop(columns=["Time"], inplace=True)
    return(df)
    
def get_metals():
    req = Request(metals_indices, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = bs(html, "html.parser")

    table = soup.find(id="cross_rate_1")
    df = pd.read_html(table.prettify(), index_col="Commodity")
    df = df[0]
    df.dropna(axis="columns", inplace=True)
    df.drop(columns=["Prev.", "Time"], inplace=True)
    return df

def get_gold_silver():
    req = Request(metals_indices, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = bs(html, "html.parser")

    table = soup.find(id="cross_rate_1")
    df = pd.read_html(table.prettify(), index_col="Commodity")
    df = df[0]
    df.dropna(axis="columns", inplace=True)
    df.drop(columns=["Prev.","Time"], inplace=True)
    gold = df.loc["Gold"]
    silver = df.loc["Silver"]
    return DataFrame([gold,silver])


def get_countries():
    ''' Gets the contries in the page Bonds from uk.investing.com and saves them into a json file '''
    req = Request(world_bonds, headers={'User-Agent':'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = bs(html, 'html.parser')   
    lcol = soup.find(id='leftColumn')
    
    # gets all scroll down selection tag
    countries_lst = lcol.find(attrs={'name':'country'})

    # get the text, which is the country name from each option tag
    # which each is a content from the main selection tag 
    countries = [country.text for country in countries_lst.contents if type(country) != NavigableString ]

    # Remove the initial option which is 'All Countries'
    if countries[0] == 'All Countries': 
        countries.pop(0)

    save_file(countries, COUNTRIES)

    return countries

def save_file(data, filename):
    try:
        with open(filename, 'w+') as fp:
            fp.write(json.dumps(data))
    except:
        pass

def get_bonds(country = 'Brazil'):
    # make a request faking as a browser so that the server responds
    req = Request(world_bonds, headers={'User-Agent':'Mozilla/5.0'})

    # get the html code from the response
    html = urlopen(req).read()

    # make an beautifulsoup object that uses html.parser 
    # to navigate within the html code
    soup = bs(html, 'html.parser')   
    
    # get left column
    lcol = soup.find(id='leftColumn')
    all_tables = lcol.find_all('table')

    # Get all the tables in the left colum of the page for analyzing
    all_tables = lcol.find_all('table')

    # Get the table based on the country input by the user
    df = None
    for tb in all_tables:
        if tb.td.span.attrs['title'] == country:
            df = pd.read_html(str(tb), index_col='Name')[0]
    df.dropna(axis='columns', inplace=True)
    df.drop(columns=['Time'], inplace=True)

    # Rounding the values on the following columns so that numbers aren't bigger than 5 decimals
    df[['Yield', 'Prev.', 'High','Low', 'Chg.']] = df[['Yield', 'Prev.', 'High','Low', 'Chg.']].applymap(lambda x: around(x,5))

    return df
    

if __name__ == "__main__":
    # print(get_indices())
    # get_metals()
    get_news()
    # print(get_gold_silver())
