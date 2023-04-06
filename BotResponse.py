import numpy as np
import json
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import warnings
warnings.filterwarnings('ignore')
import random
import os

from keras.models import load_model

# uncomment for first time use only
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

present_working_dir = os.getcwd()

model = load_model(os.path.join(present_working_dir, "static", "model_files", "chatbot_model.h5"))

intents = json.loads(open(os.path.join(present_working_dir, "static", "model_files", "intents.json")).read())

words = pickle.load(open(os.path.join(present_working_dir, "static", "model_files", "words.pkl"),'rb'))

classes = pickle.load(open(os.path.join(present_working_dir, "static", "model_files", "classes.pkl"),'rb'))

def sent_to_bow(sentence):
  sent_words = nltk.word_tokenize(sentence) # tokenize the sentence
  sent_words = [lemmatizer.lemmatize(word.lower()) for word in sent_words] # lemmatize the sentence

  bow = [0]*len(words) # create list of zeros of the size of len of words list

  # converting zeros to one if the word of sentence matchs the word in words
  for sw in sent_words:
    for i, w in enumerate(words):
      if sw == w:
        bow[i] = 1
  
  return np.array(bow)

def predict_output(sentence):
  arr = sent_to_bow(sentence)
  results = model.predict(np.array([arr]), verbose = 0)[0] # [0] because we want single list instead of list of list and verbose = 0 because it do not print the predicting line

  # its used because returned probability must be greater than 0.25 for better prediction
  ERROR_THRESHOLD = 0.25 
  # get highly matched values greater than o.25, with index no. because we want text from classes based on that index
  results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD] 

  results.sort(key= lambda x: x[1], reverse = True) # sorting based on the predicted value rether than index value, reverse is true because we want higher value first

  pred_tag = classes[results[0][0]] # get tag name from index which we already stored in reuslts

  # check which tag matched from predicted tag and store them in ans
  for intent in intents["intents"]:
    if pred_tag == intent["tag"]:
      ans = random.choice(intent["responses"])
      break

  return ans

def check(a):
    if a>=18 and a<=100:
        return "You are 18+ you can vote"
    elif a>=6 and a<18:
        return "Wait about to be 18. You are younger and you cann't vote."
    else:
        return "You are a child, please focus on your groth."
    