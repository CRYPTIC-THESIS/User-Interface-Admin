import snscrape.modules.twitter as sntwitter
import pandas as pd
import csv
maxTweets = 1000000

print ("[!] Scraping Start !!!")

cryptoData = pd.DataFrame({'searchTerm':['#bitcoin OR #btc','#ethereum OR #eth','#dogecoin OR #doge'],'dailyDataName':['Daily-Twitter-Data/BTC_Daily.csv','Daily-Twitter-Data/ETH_Daily.csv','Daily-Twitter-Data/DOGE_Daily.csv'],'cryptoName':['bitcoin','ethereum','dogecoin']})
dateSince = '2021-06-01' #Get Yesterday's Date
dateUntil = '2021-06-01' #Get Today's Date

#=====================================================================================================================
#Get Twitter Data
for index, col in cryptoData.iterrows():
    #Set Snscrape parameters
    twitterScraperParams = str(str(col["searchTerm"]) + ' + since:' + str(dateSince) + ' until:' + str(dateUntil) +  ' -filter:links -filter:replies')
    
    #Set FileName
    fileName = str(col["dailyDataName"])
    csvFile = open(fileName, 'w', newline='', encoding='utf8')

    #Use csv writer
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['id','date','username','tweet']) 

    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(twitterScraperParams).get_items()):
            if i > maxTweets :
                break  
            if (i%10000==0):
                print(i) 
            csvWriter.writerow([tweet.id, tweet.date, tweet.user.username, tweet.content])
    csvFile.close()
    print ("[!] Scraping Done !!!")

#=====================================================================================================================
#Remove Duplicate Data
for index, col in cryptoData.iterrows():
    #Set FileName
    fileName = str(col["dailyDataName"])

    #Open
    data = pd.read_csv(fileName)

    #Split date column
    data[['date', 'time']] = data["date"].str.split(" ", 1, expand=True)

    #New dataframe
    newdata_cols = ['date', 'time' , 'username', 'tweet']
    newdata = pd.DataFrame(data[['date', 'time', 'username', 'tweet']].values, columns = newdata_cols)

    #Reverse Data Order
    newdata = newdata[::-1].reset_index(drop = True)

    #Print total Raw Data Rows
    rows  = newdata.count()[0]
    print ("\nNo. of Rows (Raw): " + str(rows) + "\n")
    print (newdata[['date','time','username']].head(5))
    print (newdata[['date','time','username']].tail(5))

    #Drop Duplicate Username on the same day
    newdata.drop_duplicates(subset=['date','username'], keep='first', inplace=True)

    #Save filtered data
    newdata.to_csv(fileName, mode='w', index=False, header=True)

    #Print total Filtered Data Rows
    filtered_data = pd.read_csv(fileName)
    rows  = filtered_data.count()[0]
    print ("\nNo. of Rows (Filtered): " + str(rows) + "\n")
    print (filtered_data[['date','time','username']].head(5))
    print (filtered_data[['date','time','username']].tail(5))

#=====================================================================================================================
#Total the Data
total_data = pd.DataFrame({'date':[dateSince],'bitcoin':[0],'ethereum':[0],'dogecoin':[0]})

for index, col in cryptoData.iterrows():
    #Set FileName
    fileName = str(col["dailyDataName"])

    #Open 
    data = pd.read_csv(fileName)

    #New dataframe
    data_cols = ['date']
    data = pd.DataFrame(data[['date']], columns = data_cols)

    #Print total Rows
    rows  = data.count()[0]
    print ("\nNo. of Rows: " + str(rows) + "\n")

    i=0
    for index, row in data.iterrows():
        if (row["date"]!=(total_data.loc[i,"date"])):
            i = i + 1
            total_data.loc[i,"date"]=row["date"]
            total_data.loc[i,str(col["cryptoName"])] = 0
            total_data.loc[i,str(col["cryptoName"])]= total_data.loc[i,str(col["cryptoName"])] + 1
        else:
            total_data.loc[i,str(col["cryptoName"])]= total_data.loc[i,str(col["cryptoName"])] + 1

total_data.to_csv('Daily_Twitter_Total.csv', mode='w', index=False, header=True)