import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

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

def tag_email(text, model):
    '''
    Clean the text with the clean_text function

    Tokenize the text and pad it

    Use the loaded LSTM model softmax activation to predict the probability of each label
    for the email message being tested

    Return the highest argument as the predicted label
    '''

    text = clean_text(text)

    seq = tokenizer.texts_to_sequences([text])

    padded = pad_sequences(seq, maxlen=5000)

    labels = ['Entertainment', 'Events', 'Finance', 'Other', 'Productivity', 'Shopping', 'Social', 'Travel']

    pred = model.predict(padded)

    return labels[np.argmax(pred)]