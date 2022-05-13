import datetime
import timeit
from dateutil.relativedelta import relativedelta
from . import configKEYS as twtkeys
import tweepy
import twint
import pandas as pd 
import numpy as np
from .models import Tweets
from .PreProcessing import printTime
import langdetect


#This function make connection with twitter by use extretnal python file with keys
def twitterAPI():
    auth = tweepy.OAuthHandler(twtkeys.consumer_key,twtkeys.consumer_secret)
    auth.set_access_token(twtkeys.access_token, twtkeys.access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return(api)

def get_tweets(keyword, Startdate, EndDate, limit, lang, inDatabase, api_name, resultID=None):
    start=timeit.default_timer()
    keyword= keyword #+ "exclude:replies"  
    if(api_name.lower()=="twint"):
        tweet= twint.Config() 
        tweet.Search = keyword   
        tweet.Lang=lang                 
        tweet.Filter_retweets= True     
        tweet.Pandas=True              
        tweet.Hide_output=True
        tweet.Replies=False

        #Convert the dates to datetime object to deal with days easily 
        startDate= datetime.datetime.strptime(Startdate, "%Y-%m-%d")
        endDate= datetime.datetime.strptime(EndDate, "%Y-%m-%d")
        daysDiff= abs((endDate - startDate).days)+1                     #return the days differance between entered startDate and EndDate                   
        add_day= relativedelta(days=1)                                  #This and reletive object with day 1 which when you sum it with datetime opject will increse the day by one
        
        limitPerDay=int(limit/(daysDiff))                               #To make the fetch balanced and pass all the days of the month by taking the required limit divided by the number of days  

        sinceDate=startDate - add_day
        count=1
        ErrorCount=0
        maintweets_df=pd.DataFrame() #store all tweets 
        #Go through all the days from the start date to the end
        while(str(sinceDate) != str(endDate)): 
            tweet.Since = str(sinceDate)         
            tweet.Until = str(sinceDate+add_day)
            tweet.Limit = limitPerDay

            #to scraping the tweets from above configration 
            twint.run.Search(tweet)

            #Try to storage the search result to panda dataframe, if there an exeption that is mean no tweets scrapped  
            try:
                columns=["id", "date", "name", "username", "tweet", "nlikes", "nretweets","nreplies", "place", "link"]

                #It's an function in twint to convert the serach result to panada dataframe with choosen columns
                tweets_df = twint.storage.panda.Tweets_df[columns] #store one day tweets
                #add more column to the dataframe to ensure set the polirtay(pos,neg) later  
                tweets_df["label"]=np.nan
                tweets_df = check_lang(tweets_df, lang)
                df_length=len(tweets_df.index)

                #because the twint limit is always return 20 or 20times we should delete the extra rows
                if(limitPerDay<df_length):
                    try:
                        tweets_df=tweets_df.iloc[:-(df_length-limitPerDay)]
                        maintweets_df=pd.concat([maintweets_df,tweets_df],ignore_index=True, axis=0)
                    except:
                        print("can't drop the frame")                  
                else:
                    maintweets_df=pd.concat([maintweets_df,tweets_df],ignore_index=True, axis=0)
                if(inDatabase):
                    #Create an object in database
                    row_iter = tweets_df.itertuples()
                    objs = [
                        Tweets(
                            tweetlID   =  row.id,
                            tweetDate  = row.date,
                            tweetNickname  = row.name,
                            tweetText  = row.tweet,
                            result   = resultID ,
                            tweetUsername  = row.username,
                            tweetLikes  = row.nlikes,
                            tweetRetweets   = row.nretweets , 
                            tweetLocation   = row.place  ,
                            tweetLink       = row.link   ,     
                            tweetReplies    = row.nreplies           
                        )
                        for  row in row_iter
                    ]
                    Tweets.objects.bulk_create(objs)
                
                else:
                    #Create an CSV file in same dirct
                    filename = str(limit)+'twts_From'+str(Startdate)+'_to_'+str(EndDate)+'.csv'
                    #tweets_df.to_csv(filename, encoding='utf-8-sig', index=False,mode='a', header= not os.path.exists(filename))

            except KeyError:
                ErrorCount+=1
                print("There is no data in this day search")
                #If scraping the data failed for one day should stop the function 
                if(ErrorCount>=limitPerDay):
                    return(None)
            try:
                maintweets_df['orginalTweet']=maintweets_df['tweet']
            except:
                print('error in colomus')
            #Change since date to next day 
            sinceDate= sinceDate + add_day
            print("This is day Number==>",count)
            count+=1
        printTime(start,timeit.default_timer(),"COLLICTION TIME")
        return(maintweets_df)
        
    elif(api_name.lower()=="tweepy"):
        #NOW THIS FUNCTION NOT WORK BECAUSE ATTIRBUTE ERROR and Twint is enough for now
        #Generate an API object by call twitterAPI function 
        api=twitterAPI()

        if(limit>100):
            count=100
        else:
            count=limit

        tweets = tweepy.Cursor(api.search_tweets, q=keyword, count=count, tweet_mode="extended").items(limit)
        tweets_df = pd.DataFrame([tweet.full_text for tweet in tweets], columns=['Tweets','id'])

        return(tweets_df)  

    else:
        print("Check of the spelling of the api name (should be in small letters)")
        return(None)

#this function is to check if the language is same user asked
def check_lang(tweets_df, lang):
    def detect(x):
        try:
            lang= langdetect.detect(x)
            return lang
        except:
            print("#############Error in dection the lanuage!!##############")
            return "Error"

    tweets_df['lang']= tweets_df['tweet'].apply(lambda x: detect(x))
    tweets_df =tweets_df.loc[tweets_df['lang']== lang]
    tweets_df = tweets_df.drop('lang', 1)
    return tweets_df

