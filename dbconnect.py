import firebase_admin
import pandas as pd
from firebase_admin import firestore 
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = firebase_admin.credentials.Certificate('cryptic-database-firebase-adminsdk-bv1yi-dfd68e9690.json')

# Initialize the app with a None auth variable, limiting the server's access
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cryptic-database-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

def insert_trend_csv(tbl_name,csv_path):
    ref = db.reference(tbl_name,default_app)
    df = pd.read_csv(csv_path)
    for index, row in df.iterrows():
        users_ref = ref.child(str(index))
        users_ref.set({
            'date':row['date'],
            'btc':row['bitcoin'], 
            'eth':row['ethereum'], 
            'doge':row['dogecoin']
    
    })
    print(csv_path+" Successdully Imported")
def insert_crypto_csv(tbl_name,csv_path):
    ref = db.reference(tbl_name,default_app)
    df = pd.read_csv(csv_path)
    for index, row in df.iterrows():
        users_ref = ref.child(str(index))
        users_ref.set({
            'date':row['Date'],
            'price':row['Closing Price'], 
            'open':row['24h Open'], 
            'high':row['24h High'],
            'low':row['24h Low']
    })
    print(csv_path+" Successdully Imported")

def get_data_table(tbl_name):
    ref = db.reference(tbl_name,default_app)
    data = ref.get()
    data = pd.DataFrame(data)
    return data

#insert_trend_csv('Twitter_Data','path of twitter data')
#insert_trend_csv('Reddit_Data','path of reddit data')
#insert_trend_csv('Google_Data','path of google trend data')
#insert_crypto_csv('Bitcoin_Data','BTC_USD_2014-11-04_2021-09-20-CoinDesk.csv')
#insert_crypto_csv('Ethereum_Data','ETH_USD_2016-12-17_2021-09-20-CoinDesk.csv')
#insert_crypto_csv('Dogecoin_Data','DOGE_USD_2019-02-28_2021-09-20-CoinDesk.csv')

#data = get_data_table('Twitter_Data')