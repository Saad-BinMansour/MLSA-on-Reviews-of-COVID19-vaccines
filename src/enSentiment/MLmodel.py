from . import PreProcessing
import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer 
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import f1_score,accuracy_score, confusion_matrix
import pickle
import timeit


class MLmodel:
    #Constructor method to Create machine learning objects 
    def __init__(self, MLname, VECTname, tweets_df, **kwargs):
        self.MLname = MLname 
        self.VECTname = VECTname
        self.tweets_df =tweets_df
        self.VECTmodel=None
        self.MLmodel=None
        self.X_train=None
        self.Y_train=None
        self.X_test=None
        self.Y_test=None
        self.isLoaded= False
        self.prediction=None       
        
        #Pre preocessing to the tweets by clean data and lemmtz
        tweets_df=PreProcessing.pre_processing(self.tweets_df)
        self.tweets_label= tweets_df['label']

    def build_model(self, **kwargs):

        #Create Vectroizer to self and fit with transform to "trans_vect"
        trans_vect =self.createVectroizer()
        print("====>END VECTROIZING")

        #Split the data 
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(trans_vect,self.tweets_label, random_state=42, test_size=0.2)

        if self.MLname=="SVM":
            self.svm()
            print("====>END (SVM) BULDING MODEL")   
        
        if self.MLname=="RF":
            self.rf()
            print("====>END (RF) BULDING MODEL")
     
    def createVectroizer(self, **kwargs):
        trans_vect=None

        if self.VECTname=="bow":
            trans_vect= self.bow_vectorizer()
        if self.VECTname=="TFIDF":
            trans_vect= self.TFIDF_vectorizer()
        return trans_vect

    def bow_vectorizer(self):
        vectorizer = CountVectorizer(stop_words='english')
        self.VECTmodel = vectorizer
        bow= vectorizer.fit_transform(self.tweets_df['tweet'].apply(lambda x: np.str_(x)))        
        return bow

    def TFIDF_vectorizer(self):
        vectorizer = TfidfVectorizer(ngram_range=(1,3),min_df=5,stop_words='english')
        self.VECTmodel = vectorizer
        bow= vectorizer.fit_transform(self.tweets_df['tweet'].apply(lambda x: np.str_(x)))        
        return bow    

    def svm(self):
        svc = SVC(kernel='linear', probability=True).fit(self.X_train, self.Y_train)
        self.MLmodel = svc

    def rf(self):
        rf= RandomForestRegressor(n_estimators = 100, random_state = 42, n_jobs=-1).fit(self.X_train, self.Y_train)
        self.MLmodel = rf

    def predict(self, insert_toLabel=False):
        start=timeit.default_timer()
        if insert_toLabel==True and self.isLoaded == False:
            self.prediction= np.round(self.MLmodel.predict(self.X_test))            
            self.tweets_df['label']= self.prediction
            PreProcessing.printTime(start,timeit.default_timer(),"PREDICTING IS DONE")       

        elif insert_toLabel==True and self.isLoaded == True:
            trans_vect=self.VECTmodel.transform(self.tweets_df['tweet'].apply(lambda x: np.str_(x)))    
            self.prediction= np.round(self.MLmodel.predict(trans_vect))            
            self.tweets_df['label']= self.prediction        
            PreProcessing.printTime(start,timeit.default_timer(),"PREDICTING IS DONE")
        
        else:    
            if self.isLoaded == False:
                self.prediction= np.round(self.MLmodel.predict(self.X_test))
                PreProcessing.printTime(start,timeit.default_timer(),"PREDICTING IS DONE")
                return self.prediction
            else:
                trans_vect=self.VECTmodel.transform(self.tweets_df['tweet'].apply(lambda x: np.str_(x)))
                PreProcessing.printTime(start,timeit.default_timer(),"VECTORIZING IS DONE") 
                start=timeit.default_timer()                   
                self.prediction = np.round(self.MLmodel.predict(trans_vect))
                PreProcessing.printTime(start,timeit.default_timer(),"PREDICTING IS DONE")
                return self.prediction
    
    def saveModel(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.MLmodel, file)
    
    def loadModel(self, filename):
        with open(filename, 'rb') as file:
            self.MLmodel=pickle.load(file)
        self.isLoaded=True

        
    #Save The current vectroizer with passing file name   
    def saveVectorizer(self, filename):
       with open(filename, 'wb') as file:
            pickle.dump(self.VECTmodel, file)   

    #Load exist vectorizer
    def loadVectorizer(self, filename):
        with open(filename, 'rb') as file:
            self.VECTmodel=pickle.load(file)   


    #To Measure the f1 score
    def f1_score(self):
        if self.isLoaded==True:
            Y_label=self.tweets_label
        else:
            Y_label= self.Y_test 

        if self.prediction is None:
            self.predict()
            
        f1=f1_score(Y_label, self.prediction, average='weighted')*100
        print("\n"+50*"="+f"\nHere is the F1 score of our {self.MLname} model: \n {f1}")
        print("\n"+50*"="+f"\nHere is the Confusion Matrix of our {self.MLname} model: \n {confusion_matrix(Y_label, self.prediction)}")

        return f1

    def accuracy_score(self):
        if self.isLoaded==True:
            Y_label=self.tweets_label
        else:
            Y_label= self.Y_test 

        if self.prediction is None:
            self.predict()

        accuracy= accuracy_score(Y_label, self.prediction)*100
        print("\n"+50*"="+f"\nHere is the testing Accuracy score of our {self.MLname} model: \n {accuracy}")
        return accuracy

