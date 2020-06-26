# Tagger Mail Data Science Road Map

[![Maintainability](https://api.codeclimate.com/v1/badges/04429dcdec013a7b9175/maintainability)](https://codeclimate.com/github/Lambda-School-Labs/tagger-ds/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/04429dcdec013a7b9175/test_coverage)](https://codeclimate.com/github/Lambda-School-Labs/tagger-ds/test_coverage) ![MIT](https://img.shields.io/packagist/l/doctrine/orm.svg) [![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

Lambda Labs 24 - M. Bustamante, J. Lindberg, B. Mulas, C. Filkins
>>
The Tagger Data Science team put together 2 API points: one which resides in the cloud on a flask application within Amazon Web Services and the other, which lies internally within a stand-alone desktop Electron application. The Tagger cloud-based API pulls emails from the Google API. Our API then cleans these emails and runs them through an NLP pipeline using a latent Dirichlet allocation to derive a topic set. Those topics are then weighted by frequency and paired with concurrent VADER Sentiment Analysis. All of this is packaged up in JSON for retrieval by the desktop application. The data science API for the desktop application, in turn, receives search requests from the end-user and searches the database of email "smart tags" to find a list of relevant email IDs, which are then output to the desktop application for presentation at the user level.
>>

## Current Architecture
Currently, the application tagging engine produces a 49% tagging accuracy for the end-user. Analysis [insert link]

Go here to see a breakdown of current build architecture.

## Methods for improved tagging model accuracy:

- Spacy “Named Entity Recognition” [Docs](https://spacy.io/usage/linguistic-features#named-entities) 

- Spacy “Part of Speech” [Docs](https://spacy.io/usage/linguistic-features#pos-tagging)

- Spacy “Dependency Parsing” [Docs](https://spacy.io/usage/linguistic-features#dependency-parse)

## Methods for improved search speed:

- Elasticsearch [Docs](https://elasticsearch-py.readthedocs.io/en/master/index.html)

## Methods for improved search model relevancy:

- K Nearest Neighbors [Docs](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html), or KMeans [Docs](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html) on "search phrase" using tagging dictionary (This is the model that Labs24 was building towards. You can see such work in the [colab notebooks](https://github.com/Lambda-School-Labs/tagger-ds/tree/master/notebooks).) Predictors should be a list of emails based on search phrases.

- - Issues include:
- - - Requires managing size of tagging dictionary for KNN
- - - Requires frequency of building tagging dictionary for KNN

- Using an RNN such a Self Organizing Map [Pypi](https://pypi.org/project/MiniSom/) to "compete" with the KNN model. Develop signaling within the search to pass priority to the RNN when it's accuracy overtakes the KNN model.

- - Issues include:
- - - Requires long training time over large data sets of emails
- - - Requires application to cede function from one model to another without user intervention

- User-generated tagging as addition and augmentation to existing ML tagging API
- - Current BE DB has a table for user-generated tags, called “User Tags” by BE engineers. This is the extent of the implementation at this time.

- - The ultimate goal is to allow users to add (per individual email) their own tags, remove existing tags and apply Active Learning techniques towards more relevant results for the end-user [Docs](https://modal-python.readthedocs.io/en/latest/)

- - - Issues include:
- - - - Returning the current state of the tags back to the web-based API
- - - - Effecting the tagging model by the results of the user tag editing
This ability for the end-user to edit the tag dictionary by either adding or deleting tags will be useful in user-based labeling for training the RNN

- Sentiment analysis/warning at the search result UX



## Addtional ML Concepts / Views
The following are ways to further use machine learning to improve the Tagger Mail experience.

- Toggle machine-written (spam) email versus personal email 
- Clustering folders
- Auto-correct
- Clustering on relationships
- Best time of day to send emails/when your colleagues/friends send emails is probably a good time to send them as well
- Analytics across all user functions
- Collect contact information for sender during a search
- Products/media your contacts refer to in messages
- Trips/vacations your contacts refer to in messages
- Email deferral tracking
- Commitment detection
- Smart reply
- Contact view sorted by recency

[Additional Documentation]()

