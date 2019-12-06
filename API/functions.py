from nltk.tokenize.regexp import regexp_tokenize
from nltk.stem import WordNetLemmatizer


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

def regnltk_tokenize(text):
    lemmatizer = WordNetLemmatizer()
    text = clean_text(text)
    words = regexp_tokenize(text, pattern = '\s+', gaps = True)
    return [lemmatizer.lemmatize(word) for word in words if (len(word) >= 3)]