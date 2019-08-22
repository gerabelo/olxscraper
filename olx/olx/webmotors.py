import requests     #
import time         # para o sleep()
import sys          # para exibir o erro

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client['webmotors']
collection = db['carros']
# http://leg.ufpr.br/~walmes/ensino/web-scraping/scripts/webmotors-pr-curitiba.R
# https://www.webmotors.com.br/api/search/car?url=https://www.webmotors.com.br/carros%2Fam-manaus&actualPage=1&displayPerPage=24&order=1&showMenu=true&showCount=true&showBreadCrumb=true&testAB=false&returnUrl=false

URL = "https://www.webmotors.com.br/api/search/car"
HEADERS = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

for i in range(1,300):  
    PARAMS = {
        'url' : 'https://www.webmotors.com.br/carros/am-manaus',
        'actualPage' : i,
        'displayPerPage' : 200,
        'order' : 1,
        'showMenu' : True,
        'showCount' : True,
        'showBreadCrumb' : True,
        'testAB' : False,
        'returnUrl' : False
    }
    r = requests.get(url = URL, params = PARAMS, headers = HEADERS) 
    if r.status_code == 200:
        data = []
        data = r.json()
        print("[Page]: ",i)
        print("[count]: ",len(data["SearchResults"]))
        if len(data["SearchResults"]) == 0:
            break
        time.sleep(5)
        for item in data["SearchResults"]:
            try:
                j = collection.insert_one(item)
                print("[id]: ",item["UniqueId"],": ",j.acknowledged)
            except:

                print(item["UniqueId"],": ",sys.exc_info()[0])
    else:
        print(r.status_code,": ",sys.exc_info()[0])