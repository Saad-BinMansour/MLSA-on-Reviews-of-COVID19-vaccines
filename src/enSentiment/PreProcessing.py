import re
import timeit
import pandas as pd  
import numpy as np 
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer, WordNetLemmatizer 
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#This is main function to clean data and MUST the dataframe contain "tweet" colomun  
def pre_processing(tweets_df):
    #nltk.download()
    start=timeit.default_timer()
    tweets_df= cleanData(tweets_df)
    tweets_df = Lemmatization(tweets_df)
    tweets_df=token_to_string(tweets_df)
    printTime(start,timeit.default_timer(),"END PREPROCESSING")
    # tweets_df.to_csv("AfterPreprocessing.csv")
    return tweets_df



def tokenzation(tweets_df):
    tweets_df['tweet'] = tweets_df['tweet'].apply(lambda x: word_tokenize(x))
    return tweets_df

def stemming(tweets_df):
    stemmer = PorterStemmer()
    tweets_df= tokenzation(tweets_df)

    tweets_df['tweet']= tweets_df['tweet'].apply(lambda x: [stemmer.stem(word) for word in x])
    return tweets_df

def Lemmatization(tweets_df):
    lemmatizer = WordNetLemmatizer()
    tweets_df= tokenzation(tweets_df)

    tweets_df['tweet']= tweets_df['tweet'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])
    return tweets_df

def cleanData(tweets_df):
    def clean(data):
        data = re.sub(r'\d+', '', data)           #remove numbers
        data = re.sub(r'(.)\1+',r'\1\1',data)     #remove repetion (looook=>look)
        data=URLsRemove(data)                     #remove Urls and montion
        data=removeSpecialCharacters(data)        #remove (? / ! ? * /&)

        data = data.lower().split()               # this for make words lower case and sprite them ex => [[this],[is],[my]]
        
        cleanData = remove_stopwords(data)
        return cleanData

    tweets_df['tweet'] = tweets_df['tweet'].apply(lambda x : clean(np.str_(x)))
    return tweets_df


def removeSpecialCharacters(data):
    dataWithSpecialCharacters=data
    WithoutSpecialCharacters = re.sub(r'&\S+','', dataWithSpecialCharacters)
    WithoutSpecialCharacters =re.sub(r"[^a-zA-Z0-9.]|(?<!\d)\.|\.(?!\d)", " ",WithoutSpecialCharacters)
    return WithoutSpecialCharacters

def URLsRemove(data):
    dataWithURLs=data
    whithoutURLs=re.sub(r'http\S+', '', dataWithURLs)
    whithoutURLs=re.sub(r'www.\S+', '', whithoutURLs)
    whithoutURLs=re.sub(r'@\S+', '', whithoutURLs)      #remove montion
    whithoutURLs=re.sub(r'#\S+', '', whithoutURLs)      #remove hashtags
    return whithoutURLs

def remove_stopwords(str):
    cleanData =''                                       # declare for use later

    arr = stopwords.words('english')                    # here will have all stopWords
    newStopWords=['people','get','one','getting','u','covid','vaccine'
    ,'vaccines','vaccinated','vaccination','pfizer','virus','oxford'
    ,'pfizer','moderna','coronavirus','covid19','covidvaccine','biontech'
    , 'moderna', 'johnson & johnson', 'astrazeneca', 'novavax']
    arr.extend(newStopWords)
    c = '\''                                            # becuse remove any word has this  sign => '
    for word in str :                                                   
        if word not in arr and word.find(c) == -1   :   # this will check if word not on arr(stopwrods) and word not have this sign ' 
            cleanData += word +' '
    return cleanData

def token_to_string(tweets_df):
    tweets_df['tweet']= tweets_df['tweet'].apply(lambda x: ' '.join(x))
    return tweets_df

#This function for label the tweets by using Lexicon approacah with VADER dictionary 
def labelWith_VADER(tweets_df, URL=True, Clean=False):
    if(URL==False):
        tweets_df['tweet'] = tweets_df['tweet'].apply(lambda x : URLsRemove(x))
    if(Clean==True):
        tweets_df= pre_processing(tweets_df)

    analyzer=SentimentIntensityAnalyzer()
    tweets_df['label']= tweets_df['tweet'].apply(lambda x: analyzer.polarity_scores(x)['compound'])

    def categorise_sentiment(sentiment):
        neg_threshold=-0.05
        pos_threshold=0.05

        if sentiment < -0.05:
            label = -1
        elif sentiment > 0.05:
            label = 1
        else:
            label = 0
        return label    

    tweets_df['label']= tweets_df['label'].apply(categorise_sentiment)
    return tweets_df

def printTime(start,stop,word):
    time=stop-start
    print(f"\n{'='*20}{word}{'='*20}\n {time}")

def save_DF(tweets_df,filename):
    tweets_df.to_csv(filename)

