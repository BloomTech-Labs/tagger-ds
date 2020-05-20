from gensim.corpora import Dictionary
from gensim.models.ldamulticore import LdaMulticore
from gensim.models.coherencemodel import CoherenceModel
import spacy
import nltk
import string
from spacy.lang.en.stop_words import STOP_WORDS
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('stopwords')


def main():
    # Stop words
    stop = stopwords.words('english')
    sno = SnowballStemmer('english')

    # Load spacy model
    nlp = spacy.load('en_core_web_lg')

    # Shape text & tokenize
    df['email_body'] = text

    tokens = []
    for doc in nlp.pipe(df['email_body'], batch_size=500):
        doc_tokens = []
        for token in doc:
            if (token.is_stop is False) & (token.is_punct is False):
                doc_tokens.append(token.lemma_.lower())
        tokens.append(doc_tokens)
    df['tokens'] = tokens

    id2word = Dictionary(df['tokens'])
    id2word.filter_extremes(no_below=5, no_above=.98)

    corpus = [id2word.doc2bow(d) for d in df['tokens']]

    model = LdaMulticore(corpus=corpus,
                         id2word=id2word,
                         random_state=42,
                         num_topics=15,
                         passes=10,
                         workers=12)

    words = [re.findall(r'"([^"]*)"', t[1]) for t in model.print_topics()]

    topics = [' '.join(t[0:5]) for t in words]

    for id, t in enumerate(topics):
        print(f"------ Topic {id} ------")
        print(t, end="\n")

if __name__ == '__main__':
    main()
