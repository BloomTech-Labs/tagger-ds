from nltk.stem import WordNetLemmatizer
from nltk.tokenize.regexp import regexp_tokenize
import numpy as np



# A function that removes all unnecessary puncuation, html code, and/or any apostrophes lying around
def clean_text(text):
    # replace new line and carriage return with space
    text = text.replace("\n", " ").replace("\r", " ")
    
    # replace the numbers and punctuation (exclude single quote) with space
    punc_list = '!"#$%&()*+,-/:;<=>?[\]^_{|}~' + '0123456789'
    t = str.maketrans(dict.fromkeys(punc_list, " "))
    text = text.translate(t)
    
    # replace single quote with empty character
    t = str.maketrans(dict.fromkeys("''", ""))
    text = text.translate(t)
    
    return text

class tokenize:
    def regnltk_tokenize(text):
        lemmatizer = WordNetLemmatizer()
        text_clean = clean_text(text)
        words = regexp_tokenize(text_clean, pattern = '\s+', gaps = True)
        return [lemmatizer.lemmatize(word) for word in words if (len(word) >= 3)]


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