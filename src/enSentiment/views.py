from ast import keyword
from django.shortcuts import redirect, render 
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
import timeit
import pandas as pd
#Import our python files
from .DataCollection import get_tweets
from .PreProcessing import pre_processing
from .MLmodel import MLmodel
from django.contrib.auth.models import User, auth
from .models import Results,Tweets
from collections import Counter
from django.conf import settings


#That is home page function
def home (request):
    return render(request,'enSentiment\home.html') 


def login(request):
    if request.method == 'POST':
        #Get user inputs in local varibales 
        username=request.POST['login_username']
        password=request.POST['login_password']
        #check if his info in database
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            #Because user is find in DB we give him session by login and redirect to home
            auth.login(request, user)
            message= f'Welcome again, {user.username}'
            messages.success(request, message)
            return redirect('enSentiment:home')
        else:
            #If can't find in DB maybe user info is worng and let him to know there is a wrong
            messages.error(request, "PLEASE CHECK YOUR USERNAME OR PASSWORD!")
            return redirect('enSentiment:home')
    else:
        return render(request,'enSentiment\home.html') 

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout done')
    return redirect('./')


def register(request):
    if request.method == 'POST' and request.POST.get('register_username'):
        #Get user inputs in local varibales
        username=request.POST.get('register_username')
        firstname=request.POST.get('register_firstname')
        lastname=request.POST.get('register_lastname')
        email=request.POST.get('register_email')
        password=request.POST.get('register_password')
        conf_password=request.POST.get('register_confpassowrd')
        print(password)
        print(conf_password)
        if password==conf_password:
            #Check in database if user inputs exist already or not 
            if User.objects.filter(username=username).exists():
                messages.error(request, 'USER NAME EXISTS!')
                return redirect('enSentiment:home') 
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'EMAIL EXIST!')
                return redirect('enSentiment:home') 
            else:
                #If user input is correct, that will create a row in database with his info 
                user = User.objects.create(username=username,first_name=firstname,last_name=lastname,email=email)
                user.set_password(password)
                user.save()

                #and we give him session by login and redirect to home
                auth.login(request, user)
                successMSG="Welcome ("+firstname+") To our site."
                messages.success(request, successMSG)
                return redirect('enSentiment:home')

        messages.error(request, "PASSWORDS DOESN'T MATHC!!")
        return redirect('enSentiment:home') 

    else:
        return render(request,'enSentiment\home.html') 

def aboutus(request):
    return render(request, 'aboutus.html')


def result(request,id=None):

    if id:
        #Get Result ID as an Object
        result=Results.objects.get(id=id)
        
        #Fetch tweets from database to Dataframe
        tweets_df = pd.DataFrame.from_records(
            Tweets.objects.filter(result=result).values_list('tweetlID','tweetDate', 'tweetNickname','tweetUsername', 'tweetText', 'tweetLikes', 'tweetRetweets', 'tweetReplies',  'tweetLocation','tweetLink','tweetLabel')
        ,columns=["id", "date", "name", "username", "tweet", "nlikes", "nretweets","nreplies", "place", "link","label"])
        
        #Save tweet to orginal tweets before pre processing the tweets 
        tweets_df['orginalTweet']=tweets_df['tweet']
        try:
            tweets_df['date']=tweets_df['date'].dt.strftime('%Y-%m-%d %H:%M:%S') 
        except:
            tweets_df['date']=tweets_df['date']
        tweets_df=pre_processing(tweets_df)

        #Get tweets information to display it in result page 
        tweets_info=get_tweets_info(tweets_df,result.FromDate,result.ToDate,result.Keyword)

        check_session = check_sessions(request)
        if not check_session:
            create = make_sessions(request,tweets_info)
            if not create :
                print("Error")
        else:
            del request.session['tweets_info']
            create = make_sessions(request,tweets_info)
            if not create :
                print("Error")

        return render(request,'result.html',tweets_info)
    else:
        check_session = check_sessions(request)
        if check_session:
            return render(request,'result.html',check_session)
    return render(request,'result.html')

def allTweets(request):
    check_session = check_sessions(request)
    if check_session:
        return render(request,'allTweets.html',check_session)
    return redirect('enSentiment:result')

def profile(request):
    if request.user.is_authenticated :
        if request.method =='GET':
            username=request.user.username
            firstname=request.user.first_name
            lastname=request.user.last_name
            email=request.user.email
            context={
                'firstname':firstname,
                'lastname':lastname,
                'username':username,
                'email':email,
            }
            return render(request,'profile.html',context)
        if request.method =='POST':
            if request.POST['firstname']:
                request.user.first_name=request.POST['firstname']
                request.user.save()
            
            if request.POST['lastname']:
                request.user.last_name=request.POST['lastname']
                request.user.save()

            if request.POST['email']:
                request.user.email=request.POST['email']
                request.user.save()
            
            if request.POST['password']:
                request.user.set_password(request.POST['password'])
                request.user.save()
                
            if request.POST['username']:
                request.user.username=request.POST['username']
                request.user.save()

            username=request.user.username
            firstname=request.user.first_name
            lastname=request.user.last_name
            email=request.user.email
            context={
                'firstname':firstname,
                'lastname':lastname,
                'username':username,
                'email':email,
            }

            message= f'{request.user.username}, Your information has been updated successfully.'
            messages.success(request, message)
            
            return render(request,'profile.html',context)


        
    return render(request,'profile.html')

def myresults(request):
    if request.user.is_authenticated :
        user=request.user
        result=Results.objects.filter(userID_id=user)
        return render(request,'myresults.html',{'results':result})
    return render(request,'myresults.html')

def del_result(request,id):
    Results.objects.filter(id=id).delete()
    return redirect('enSentiment:myresults')

def getAnalysis(request):

    keyword=str(request.POST['SelectKeyWord'])
    fromDate=str(request.POST['FromData'])
    toDate=str(request.POST['ToDate'])
    tweetsNum=int(request.POST['tweetsNum'])

    #Check if user is member or anonymously
    username=None
    if request.user.is_authenticated :
        username= request.user.username 
    tweets_df =analyze(keyword, fromDate, toDate, tweetsNum,"en", username=username)  
    if(tweets_df.empty):
        return JsonResponse({'state':False},status=200)
    tweets_info=get_tweets_info(tweets_df,fromDate,toDate,keyword)

    check_session = check_sessions(request)
    if not check_session:
        create = make_sessions(request,tweets_info)
        if not create :
            print("Error")
    else:
        del request.session['tweets_info']
        create = make_sessions(request,tweets_info)
        if not create :
            print("Error")

    if request.POST.get('sendEmail'):
            context={'user':request.user,'num_allTweets':tweets_info['num_allTweets']}
            html_body = render_to_string("Email.html",context)
            msg = EmailMultiAlternatives(subject='Your Analysis of '+str(tweets_info['num_allTweets'])+' Tweets is ready', from_email=settings.EMAIL_HOST_USER,
                        to=[request.user.email], body='text_body')
            msg.attach_alternative(html_body, "text/html")
            msg.send()
    return JsonResponse({'state':True},status=200)




'''Here is backend and analysis funcitons'''

#this is main function to analyze user options and insert it to database
def analyze(keyword_uChoice, uStartDate, uEndDate, uLimit, uLang, username):
    inDatabase=False
    resultID=None
    #if user member will collect the data with his account if not the data will be save temp in memoroy 
    if username:
        #1st Create result row in Result tabel
        result=Results.objects.create(userID=User.objects.get(username=username),Keyword=keyword_uChoice,NumberOftweets=uLimit, FromDate=uStartDate, ToDate=uEndDate)
        resultID=result
        inDatabase=True

   #2nd Check and create best keyword
    keywords=None
    match keyword_uChoice:
        case "All vaccines":
            keywords="vaccine OR \"covid vaccine\" OR \"COVID-19 vaccine\" OR \"COVID19 vaccine\" OR vaccinated OR covidvaccine OR #vaccine OR vaccination OR Pfizer OR BioNTech OR Moderna OR \"Johnson & Johnson\" OR AstraZeneca OR Novavax"
        case "Pfizer-BioNTech":
            keywords="pfizer OR BioNTech"
        case "Moderna":
            keywords="Moderna"
        case "Johnson & Johnson’s Janssen":
            keywords=" \"Johnson & Johnson’s Janssen\" "
        case "Oxford-AstraZeneca":
            keywords=" \"Oxford AstraZeneca\" OR AstraZeneca"
        case "Novavax":
            keywords="Novavax"

    #3rd Search on user analysis options and insert it to DB with None in label
    '''Data Collection Code'''
    df=get_tweets(keywords, uStartDate, uEndDate, uLimit, uLang,inDatabase,"twint", resultID)
    
    if(df.empty):
        return None

    #4th Create Machine learing object and clean data to predict ONLY
    '''Read MODEL'''
    SVM_Model=MLmodel("SVM","TFIDF", df)
    SVM_Model.loadModel(str(settings.BASE_DIR) +'\\MachineLearning_models\\180k_MySVM_model.pkl')
    SVM_Model.loadVectorizer(str(settings.BASE_DIR) +'\\MachineLearning_models\\180k_MySVM_vectorizer.pkl')
    SVM_Model.predict(insert_toLabel=True)
    #this "df" now is labeld with Machine learning model 
    df = SVM_Model.tweets_df

    if username:
        #5th Insert label column in "df" var to label column in DB. by select same tweet id from df
        for row in df.itertuples():
            Tweets.objects.filter(result=result,tweetlID=row.id).update(tweetLabel=row.label)

    return df

def get_tweets_info(tweets_df,fromDate,toDate,keyword):
    #get the number of tweest in every class
    num_allTweets=len(tweets_df.index)
    num_posTweets=len(tweets_df[tweets_df['label']==1].index)
    num_negTweets=len(tweets_df[tweets_df['label']==-1].index)
    num_natTweets=len(tweets_df[tweets_df['label']==0].index)
    num_ofTweets=[{'x':'positive','value':num_posTweets, 'fill':'#CEDB84'},{'x':'natural','value':num_natTweets, 'fill':'#5895DB'},{'x':'negative','value':num_negTweets, 'fill':'#DB766D'}]


    #this function to convert the word list to dictonary 
    def to_dict(words):
        list_most=[]
        for word in words:
            dict={'x':word[0],'value':word[1]}
            list_most.append(dict)
        return list_most
    #Get the most 100 common word in every class in put it in dictonary    
    most_posTweets=to_dict(Counter(" ".join(tweets_df['tweet'][tweets_df['label']==1]).split()).most_common(100))
    most_natTweets=to_dict(Counter(" ".join(tweets_df['tweet'][tweets_df['label']==0]).split()).most_common(100))
    most_negTweets=to_dict(Counter(" ".join(tweets_df['tweet'][tweets_df['label']==-1]).split()).most_common(100))

    #Get the most 4 intreactive tweets by number of replies and put in dataframe
    top_posDF=tweets_df.loc[tweets_df['label']==1]
    top_posDF=top_posDF.loc[(top_posDF['nreplies'].nlargest(4).index)]
    top_natDF=tweets_df.loc[tweets_df['label']==0]
    top_natDF=top_natDF.loc[(top_natDF['nreplies'].nlargest(4).index)]
    top_negDF=tweets_df.loc[tweets_df['label']==-1]
    top_negDF=top_negDF.loc[(top_negDF['nreplies'].nlargest(4).index)]

    #All Postive and Negtiave tweets in spreate Dataframe
    posDF=tweets_df.loc[tweets_df['label']==1]
    negDF=tweets_df.loc[tweets_df['label']==-1]

    #Add numbers of tweest based date in list to diplay it as an Axis chart
    #make copy of orginal DF to another to change the date type
    tweets_df_dates=tweets_df.copy()
    tweets_df_dates['date']= pd.to_datetime(tweets_df['date'])
    tweets_df_dates['date']= tweets_df_dates['date'].dt.strftime('%Y-%m-%d')

    #Add all search dates to list 
    datesLabel=[]
    datesLabel.append(tweets_df_dates.loc[0,'date'])
    for i in range(1,len(tweets_df_dates)):
        if tweets_df_dates.loc[i,'date']!=tweets_df_dates.loc[i-1,'date']:
            datesLabel.append(tweets_df_dates.loc[i,'date'])

    #Function to convert polarity DF to list with numbers of tweets in same data 
    def to_list(date_df,datesLabel):
        list=[]
        counter=0
        for i in range(len(datesLabel)):
            for j in range(len(date_df)):
                if datesLabel[i]==date_df.loc[j,'date']:
                    counter=counter+1
            list.append(counter)
            counter=0
        return list

    #Apply the function to conver to list
    num_posDate=to_list(tweets_df_dates.loc[tweets_df_dates['label']==1].reset_index(),datesLabel)
    num_natDate=to_list(tweets_df_dates.loc[tweets_df_dates['label']==0].reset_index(),datesLabel)
    num_negDate=to_list(tweets_df_dates.loc[tweets_df_dates['label']==-1].reset_index(),datesLabel)

    #Graping all above data to dictonary object
    tweets_infos={
    'FromDate':fromDate,
    'ToDate':toDate ,
    'keyword': keyword,

    'tweets_df':tweets_df.to_dict('records'),

    'num_ofTweets':num_ofTweets,   
    'num_allTweets':num_allTweets,
    'num_posTweets':num_posTweets,
    'num_negTweets':num_negTweets,
    'num_natTweets':num_natTweets,

    'most_posTweets':most_posTweets,
    'most_negTweets':most_negTweets,
    'most_natTweets':most_natTweets,

    'top_posDF':top_posDF.to_dict('records'),
    'top_natDF':top_natDF.to_dict('records'),
    'top_negDF':top_negDF.to_dict('records'),

    'posDF':posDF.to_dict('records'),
    'negDF':negDF.to_dict('records'),

    'datesLabel':datesLabel,
    'num_posDate':num_posDate,
    'num_natDate':num_natDate,
    'num_negDate':num_negDate,
    }
    return tweets_infos

#Check if tweets info is in user session if yes return the tweets info
def check_sessions(request):

    if request.session.has_key('tweets_info'):

        return request.session.get('tweets_info')
    else:
        return 

#Create key in user session with tweets info              
def make_sessions(request,data):

    if not request.session.has_key('tweets_info'):
        request.session["tweets_info"] = data
        request.session.modified = True
        return True
    else:
        return 