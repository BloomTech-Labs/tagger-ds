import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences


with open('final_tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

def clean_text(text):
    # Perform a few cleaning steps to remove non-alphabetic characters
    
    text = text.replace("\n", " ").replace("\r", " ")
    text = text.strip(" ")
    
    punc_list = '!@#$%^&*()+?-_=:.<>[]{}/\~",©' + '1234567890'
    t = str.maketrans(dict.fromkeys(punc_list, " "))
    text = text.translate(t)
    
    return text

def format_inputs(text, maxlength):
    text = clean_text(text)
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=maxlength)
    
    return padded

def get_tags(text, loaded_model):
    labels = ['Entertainment', 'Events', 'Finance', 'Other', 'Productivity', 'Shopping', 'Social', 'Travel']
    padded = text
    pred = loaded_model.predict(padded)
    if (np.argmax(pred)) >= .90:
        best = np.argmax(pred)
        prediction = labels[best]
        return [prediction]
    else:
        best = np.argmax(pred)
        best_pred = labels[best]
        print(pred)
        pred = np.where(pred == pred.max(), 0, pred)
        print(pred)
        second = np.argmax(pred)
        second_pred = labels[second]
        return [best_pred, second_pred]