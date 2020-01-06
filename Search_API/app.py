import gensim.downloader as api
import spacy
import en_core_web_lg
from flask import Flask, request, jsonify


app = Flask(__name__)
model = api.load('glove-wiki-gigaword-50')
nlp = en_core_web_lg.load()


def get_similar_words(search: spacy.tokens.token.Token) -> list:
    results = [search.lemma_]

    matches = model.most_similar(str(search))
    
    for match in matches:
        if len(results) < 3:
            doc = nlp(match[0])
            for token in doc:
                if token.lemma_ not in results:
                    results.append(str(token))
        else:
            continue

    return results


@app.route('/', methods=['POST'])
def home():
    data = request.get_json()
    queries = {'search1': data["query"]}
    tokens = [token for token in nlp(queries['search1']) if token.pos_ == 'NOUN']
    keyword = tokens[0]
    matches = get_similar_words(keyword)
    for i, match in enumerate(matches[1:]):
        queries[f'search{i+2}'] = queries['search1'].replace(str(keyword), str(match))

    return jsonify(queries)


if __name__ == '__main__':
    app.run()
