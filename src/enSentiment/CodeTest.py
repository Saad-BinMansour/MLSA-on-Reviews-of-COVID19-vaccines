                    #''' This python file to test OUR FUNCTIONS out side django'''

import timeit
import pandas as pd 
import matplotlib.pyplot as plt 
import nltk
import seaborn as sns
from collections import Counter
#Our library 
# from MLmodel import MLmodel
# from DataCollection import get_tweets
# from PreProcessing import pre_processing,labelWith_VADER,printTime,save_DF
import PreProcessing



'''Data Collection Code'''
# start=timeit.default_timer()
# #keywords="vaccine OR \"covid vaccine\" OR \"COVID-19 vaccine\" OR \"COVID19 vaccine\" OR vaccinated OR covidvaccine OR #vaccine OR vaccination OR Pfizer OR BioNTech OR Moderna OR \"Johnson & Johnson\" OR AstraZeneca OR Novavax"
# arKeywords="لقاح OR \"لقاح كوفيد\" OR \"لقاح كوفيد-19\" OR \"لقاح كوفيد19\" OR ملقح OR لقاح كورونا OR #لقاح OR التطعيم OR فايزر OR بايوتنك OR موديرنا OR \"جونسون& جونسون\" OR استرازينكا OR نوفافاكس"
# df=get_tweets(arKeywords, "2021-02-28", "2022-02-28",140000,"ar",False,"twint")
# stop=timeit.default_timer()
# print(df.head())
# printTime(start,stop,"COLLICTION TIME")

'''Data Preprocessing Code'''
# start=timeit.default_timer()
# df= pd.read_csv(r"C:\PythonProjects\MLSA-on-Reviews-of-COVID19-vaccines\tweets\3k_labeld_withVADER.csv")
# df = pd.DataFrame({'tweet':['i won\'t take the vaccine it\'s cuteee gratting']})
# print(df.head())
# df= pre_processing(df)
# stop=timeit.default_timer()
# print(df.head())
# printTime(start,stop,"PREPROCESSING TIME")

'''Label the sentiment using VADER Code'''
# df= pd.read_csv(r"C:\PythonProjects\MLSA-on-Reviews-of-COVID19-vaccines\170000twts_From2021-02-28_to_2022-02-27.csv")
# start=timeit.default_timer()
# df= labelWith_VADER(df)
# stop=timeit.default_timer()
# save_DF(df, "170k_AR_labeld_withVADER.csv")
# print(df.head())
# printTime(start,stop,"LABLING TIME")

'''Build Model and predict the dataset'''
# df=pd.read_csv(r'C:\PythonProjects\TwitterS\80k_labeld_withVADER.csv')

# # #BUILD SVM MODEL
# SVM_Model= MLmodel("SVM","TFIDF", df)
# start=timeit.default_timer()
# SVM_Model.build_model()
# stop=timeit.default_timer()
# printTime(start,stop,"TRAINING TIME")
# #save SVM model and vectroizer
# SVM_Model.saveModel("80K_MySVM_model.pkl")
# SVM_Model.saveVectorizer("80K_MySVM_Vectorizer.pkl")
# #Predict SVM MODEL
# start=timeit.default_timer()
# prediction=SVM_Model.predict()
# stop=timeit.default_timer()
# printTime(start,stop,"PREDCTING TIME")
# SVM_Model.accuracy_score()
# SVM_Model.f1_score()

# #BUILD RF MODEL
# RF_Model= MLmodel("RF","TFIDF", df)
# start=timeit.default_timer()
# RF_Model.build_model()
# stop=timeit.default_timer()
# printTime(start,stop,"TRAINING TIME")
# #save RF model and vectroizer
# # RF_Model.saveModel("180K_RF_Model.pkl")
# # RF_Model.saveVectorizer("180K_RF_Model_Vectorizer.pkl")
# #Predict RF Model MODEL
# start=timeit.default_timer()
# prediction=RF_Model.predict()
# stop=timeit.default_timer()
# printTime(start,stop,"PREDCTING TIME")
# RF_Model.accuracy_score()
# RF_Model.f1_score()

'''Read MODEL'''
# df=pd.read_csv(r'C:\PythonProjects\TwitterS\3k_labeld_withVADER.csv')
# testDF=pd.DataFrame({'tweet':["When the tone of the threat changes, this indicates weakness and that they have exhausted all possible ways to persuade people to take those poisons, so whoever finds harm from the first or second dose should not be tempted by their statements.","i will take the vaccine.", "Ain't no way I'm taking that vaccine.","I am lost for words with reports that people in the eu are refusing the vaccine.","i will not take the vaccine", "In testing, the vaccine was 100 percent effective at preventing severe cases of COVID-19"],'label':[-1,1,-1,-1,-1,1]})

# SVM_Model=MLmodel("SVM","TFIDF", testDF)
# SVM_Model.loadModel(r"C:\PythonProjects\TwitterS\180k_BIGRAM_MySVM_model.pkl")
# SVM_Model.loadVectorizer(r"C:\PythonProjects\TwitterS\180K_BIGRAM_MySVM_Vectorizer.pkl")

# prediction=SVM_Model.predict()
# print(prediction)
# SVM_Model.tweets_df['prdict']=prediction
# print(SVM_Model.tweets_df)
# SVM_Model.accuracy_score()


'''Most words Visualization'''
tweets_df=pd.read_csv(r"C:\PythonProjects\MLSA-on-Reviews-of-COVID19-vaccines\src\5twts_From2020-11-01_to_2020-11-05.csv")
# df= pre_processing(df)
# def words_extract(x): 
#   words = [] 
#   for i in x:
#       i=i.split(" ")
#       for x in i:
#          words.append(x) 
#   return words

# #Choose which sentiment words you want
# words_pos = words_extract(df['tweet'][df['label'] ==-1])
# print(len(words_pos))
# a = nltk.FreqDist(words_pos) 
# d = pd.DataFrame({'word': list(a.keys()), 'Count': list(a.values())})
# d = d.nlargest(columns="Count", n = 20)
# plt.figure(figsize=(20,5))
# ax = sns.barplot(data=d, x= "word", y = "Count") 
# ax.set(ylabel = 'Count') 
# plt.show()



num_allTweets=len(tweets_df.index)
num_posTweets=len(tweets_df[tweets_df['label']==1].index)
num_negTweets=len(tweets_df[tweets_df['label']==-1].index)
num_natTweets=len(tweets_df[tweets_df['label']==0].index)

perc_posTweets=(num_posTweets/num_allTweets)*100
perc_negTweets=(num_negTweets/num_allTweets)*100
perc_natTweets=(num_natTweets/num_allTweets)*100

tweets_df=PreProcessing.pre_processing(tweets_df)
def to_dict(words):
    list_most=[]
    for word in words:
        dict={'x':word[0],'value':word[1]}
        list_most.append(dict)
    return list_most
most_posTweets=to_dict(Counter(" ".join(tweets_df['tweet'][tweets_df['label']==1]).split()).most_common(100))
most_natTweets=to_dict(Counter(" ".join(tweets_df['tweet'][tweets_df['label']==0]).split()).most_common(100))
most_negTweets=to_dict(Counter(" ".join(tweets_df['tweet'][tweets_df['label']==-1]).split()).most_common(100))


top_posDF=tweets_df.loc[tweets_df['label']==1]
top_posDF=top_posDF.loc[(top_posDF['nreplies'].nlargest(10).index)]
top_natDF=tweets_df.loc[tweets_df['label']==0]
top_natDF=top_natDF.loc[(top_natDF['nreplies'].nlargest(10).index)]
top_negDF=tweets_df.loc[tweets_df['label']==-1]
top_negDF=top_negDF.loc[(top_negDF['nreplies'].nlargest(10).index)]

tweets_nums={
'tweets_df':tweets_df,

'num_allTweets':num_allTweets,
'num_posTweets':num_posTweets,
'num_negTweets':num_negTweets,
'num_natTweets':num_natTweets,

'perc_posTweets':perc_posTweets,
'perc_negTweets':perc_negTweets,
'perc_natTweets':perc_natTweets,

'most_posTweets':most_posTweets,
'most_negTweets':most_negTweets,
'most_natTweets':most_natTweets,

'top_posDF':top_posDF,
'top_natDF':top_natDF,
'top_negDF':top_negDF,
}

print(tweets_nums['most_negTweets'])
print(num_allTweets,num_negTweets, num_natTweets, num_posTweets,perc_posTweets,perc_negTweets,perc_natTweets)

print(tweets_nums['top_natDF'][['tweet','nretweets','label']])


for index,row in tweets_df.iterrows():
    print("THE TWEET:"+row['tweet']+".  THE LABEL: "+str(row['label']))

