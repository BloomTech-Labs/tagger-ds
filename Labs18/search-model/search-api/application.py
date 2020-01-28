import gensim.downloader as api
import en_core_web_sm
from flask import Flask, request, jsonify


application = Flask(__name__)
model = api.load('glove-wiki-gigaword-50')
nlp = en_core_web_sm.load()


def get_similar_words(search):
    results = [search.lemma_]
    try:
        matches = model.most_similar(str(search).lower())
    except:
        return results

    for match in matches:
        if len(results) < 3:
            doc = nlp(match[0])
            for token in doc:
                if token.lemma_ not in results:
                    results.append(token.lemma_)
        else:
            continue

    return results


@application.route('/', methods=['POST'])
def home():
    data = request.get_json()
    queries = {'search1': data["query"]}
    doc = nlp(queries['search1'])
    parts_of_speech = ['NOUN', 'VERB']
    tokens = [token for token in doc if token.is_stop == False and token.pos_ in parts_of_speech]
    if len(tokens) < 1:
        tokens = [token for token in doc]
    keyword = tokens[0]
    
    matches = get_similar_words(keyword)
    if len(matches) > 1:
        for i, match in enumerate(matches[1:]):
            queries[f'search{i+2}'] = queries['search1'].replace(str(keyword), str(match))

    return jsonify(queries)


if __name__ == '__main__':
    application.run()
