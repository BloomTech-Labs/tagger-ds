import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

with open('tokenizer.pickle', 'rb') as handle:
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

def get_tags(text, model):
    labels = ['Entertainment', 'Events', 'Finance', 'Other', 'Productivity', 'Shopping', 'Social', 'Travel']
    padded = text
    pred = model.predict(padded)

    if (np.argmax(pred)) >= .90:
        best = np.argmax(pred)
        prediction = labels[best]
        return prediction
    else:
        best = np.argmax(pred)
        best_pred = labels[best]
        pred = np.where(pred == np.argmax(pred), 0, pred)
        second = np.argmax(pred)
        second_pred = labels[second]
        return best_pred, second_pred

def getTags(preds_proba, encoder):
    classes = encoder.classes_
    if preds_proba.max() >= .75:
        best = np.where(preds_proba == preds_proba.max())
        prediction = classes[best]
        return [prediction[0]]
    else:
        best = np.where(preds_proba == preds_proba.max())
        best_pred = classes[best]
        preds_proba = np.where(preds_proba==preds_proba.max(), 0, preds_proba)
        second = np.where(preds_proba== preds_proba.max())
        second_pred = classes[second]
        return [best_pred[0], second_pred[0]]