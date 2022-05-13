# MLSA-on-Reviews-of-COVID19-vaccines
 We are a group of computer science students who have been studying together for the last five years. We would like to present our project to you. We have built a sentiment analyzer website that can analyze the sentiment of any given text that is related to covid-19 vaccines in a short period of time. 
> Live demo [_here_](http://MLSA.cloud/). 

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [File Dictonary](#file-dictonary)
* [Setup](#setup)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)


## General Information
Our website allows the user to analyze sentiment by filling a form of his specific preferences. Time of analysis depending on number of tweets and the interval of time the user chose. Accuracy of analysis is: %81.8341. The result will be saved automatically in "My Result" page if the user is logged in.


## Technologies Used
- Python - version 3.10
- Django - version 4.04
- Pandas - version 1.4.2
- nltk - version 3.7
- scikit-learn - version 1.0.2
- twint - version 2.1.21
- AnyChart - version 8.11.0
- ChartJS - version 2.5.0


## Features
Our website has the following features:
- Analyze all or specific COVID-19 vaccine on any certain date from 2020-1 to NOW with limit of tweets number of 3500
- Send an email when analysis is done 
- Display result with three, charts PIE chart, WordCloud Chart and LineChart and list of top4 positive/negative tweets
- Save a summary of result as an pdf if the user is logged in
- See all analyzed tweets with orignal link
- Access to previous results
- Update personal user information

## Screenshots
![screenshot1](https://drive.google.com/uc?export=view&id=1-sg0NljpdzfIPRzkell8B-JCZAltPKJX)


## File Dictonary

 * [src](./src)
   * [enSentiment](./src/enSentiment)
       * [static](./src/enSentiment/static)
       * [templates](./src/enSentiment/templates)
       * [urls.py](./src/enSentiment/urls.py)
       * [views.py](./src/enSentiment/views.py)
       * [models.py](./src/enSentiment/models.py)
       * [DataCollection.py](./src/enSentiment/DataCollection.py)
       * [PreProcessing.py](./src/enSentiment/PreProcessing.py)
       * [MLmodel.py](./src/enSentiment/MLmodel.py)

   * [MachineLearning_models](./src/MachineLearning_models)
        * [180k_MySVM_Vectorizer.pkl](./src/MachineLearning_models/180k_MySVM_Vectorizer.pkl)        
        * [180k_MySVM_model.pkl](./src/MachineLearning_models/180k_MySVM_model.pkl)
       
   * [mainsite](./src/mainsite)
        * [urls.py](./src/mainsite/urls.py)
        * [settings.py](./src/mainsite/settings.py)
        
   * [manage.py](./src/manage.py)
   
 * [env](./env)
   * [nltk_data](./env/nltk_data)
   * [Lib](./env/Lib)
   
   
 * [README.md](./README.md)
 * [requirements.txt](./requirements.txt)
 
## Setup
in this section will explain how to install the appliction in your local machine

### Prerequisites
You have to install:
```
Python 3.10
mySQL 
Good internet connection : For retrieving data from twint
``` 
### Download
Download our projcet to your computer intenal path in from our repository as zip or clone it 

### Installing
1) After download the whole project open the Command Prompt on cloned project path and running the next command:

```
python3 -m venv env 
```
The last command building virtual environment.

2) Then you need to activate this environment by running the next command .

```
env\Scripts\activate 
```
Then the word env will appear in parentheses to the left of current path.

3) To install project dependencies in project environment run the next command: 
```
pip install -r requirements.txt
```

4) You have to create a MySQL database with same name "mlsa_on_covid_reviews" and run mySQL database. If you want to change database access settings go to src/mainstie/settings.py then go to line 85 "Databases" and change it to your personal preferences.
  

5) You need to migrate the database by running the next command:
```
1- cd src/
2- python manage.py migrate
```

6) Now you can run the Djanog server by running the next command:
```
python manage.py runserver 
```

7)Now click on the localhost url that will be shown in Command Prompt, the website should be running now :)

## Room for Improvement
This is not end off the road we have some future improvments.
Such as:
- Add new langauge for the frontend with new model for arabic tweets
- Imporve the accuracy of current SVM model


## Acknowledgements
First, we thank Allah Almighty for enabling us to complete our project’s  main objectives and goals of our graduation project, praise be to him. Also, we would  like to express our thanks to Graduation Projects Committee who cooperated with us, we would like to thank our families for their wise advices and friendly support.
![image](https://user-images.githubusercontent.com/55384777/167719591-08bcc1df-232c-434b-9738-830c16d48372.png)


## Contact
Via college emails: 
smsbinonayq@sm.imamu.edu.sa
fkfalotaibe@sm.imamu.edu.sa

Github repository: https://github.com/Saad-BinMansour/MLSA-on-Reviews-of-COVID19-vaccines.git
