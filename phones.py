import re, unidecode
from pymongo import MongoClient, TEXT

client = MongoClient("mongodb://localhost:27017")

db = client['olx']
db_dst = client['phones']
collections = ['escritorio','casa','esporte','animais','industria','infantis','outrascidades','utensilios','moda','servicos','hobbies','eletronicos','carros','imoveis','construcao']
collection_dst = db_dst['phones']
collection_dst.create_index([('phone',TEXT)],unique=True)

a=0
for collection in collections:
    print('\n',collection)
    source = db[collection]
    docs = source.find({})
    for doc in docs:
        # print('.',end="")
        # try:
        if doc.get('phone'):
            try:
                collection_dst.insert_one({"phone":doc.get('phone'),"location":doc.get('location')})
            except:
                None
        else:
            description = doc.get('description')
            if description:
                words = description.split()
                for word in words:
                    # phone = re.search("^9[0-9]{4,11}[-]{0,1}[_]{0,1}",word)
                    # phone = re.search("/^(?:(?:\+|00)?(55)\s?)?(?:\(?([1-9][0-9])\)?\s?)?(?:((?:9\d|[2-9])\d{3})\-?(\d{4}))$/",word)
                    phone = re.search("(\(?\d{2}\)?\s)?(\d{4,5}[-]{0,1}[_]{0,1}\d{4})",word)
                    # phone = re.sub("[^0-9]", "", phone)
                    if phone:
                        # word = re.sub(r'[a-záàâãéèêíïóôõöúçñ]+','',word,flags=re.I)
                        # word = word.replace('.','').replace(',','').replace('!','').replace(':','').replace('-','').replace('_','').replace('/','').replace('(')
                        results = re.findall(r'\d',word)
                        word = ''.join(results)                        
                        print('phone: ',word)
                        a+=1
                        try:
                            collection_dst.insert_one({"phone":word,"location":doc.get('location')})
                        except:
                            None
        # except:
        #     None
print(a)