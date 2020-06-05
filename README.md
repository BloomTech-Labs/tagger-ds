# Tagger - Smarter Email

[![Maintainability](https://api.codeclimate.com/v1/badges/04429dcdec013a7b9175/maintainability)](https://codeclimate.com/github/Lambda-School-Labs/tagger-ds/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/04429dcdec013a7b9175/test_coverage)](https://codeclimate.com/github/Lambda-School-Labs/tagger-ds/test_coverage) ![MIT](https://img.shields.io/packagist/l/doctrine/orm.svg) [![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)


You can find the data science API project at ``.

## Labs 24 Contributors
|[Brandon Mulas](https://github.com/bmulas1535)|[Monica Bustamante](https://github.com/Moly-malibu)|
|:---:|:---:|
|[<img src="https://avatars3.githubusercontent.com/u/54636579?s=460&u=d00932d4a8f2179dd262f9e934d125adda505d2c&v=4" width="200">](https://github.com/bmulas1535)|[<img src="https://avatars0.githubusercontent.com/u/58006376?s=460&u=8382c603014ddf685cf7886ecc1f62e6429b9626&v=4" width="200">](https://github.com/Moly-malibu)|
|[Chris Filkins](https://github.com/filchyboy)|[Jack Lindberg](https://github.com/Jllin50)|
[<img src="https://avatars3.githubusercontent.com/u/55597792?s=460&u=6b0d46f250e1e450c25cc32d692601d591f2b267&v=4" width="200">]()|[<img src="https://avatars1.githubusercontent.com/u/31583768?s=460&u=5d5f73d4382a2d9e54b78b97fa0b71e3621510fc&v=4" width="200">](https://github.com/Jllin50)|

## Labs 20 Contributors 
|[Rosie Lasota](https://github.com/apathyhill)|[Jean Fraga](https://github.com/JeanFraga)|  
|:---:|:---:|
|[<img src="https://avatars3.githubusercontent.com/u/14889913?s=460&v=4" width="200" />](https://github.com/apathyhill)|[<img src="https://avatars3.githubusercontent.com/u/12549527?s=460&v=4" width="200" />](https://github.com/JeanFraga)|

## Labs 18 Contributors 
|[Avraham Jacobsohn](https://github.com/noreallyimfine)|[John Morrison](https://github.com/JohnMorrisonn)|[Samuel Hepner](https://github.com/SamH3pn3r)|
|:---:|:---:|:---:|
|[<img src="https://ca.slack-edge.com/T4JUEB3ME-UJJJCQN4R-3d9845ab1b54-512" width="200" />](https://github.com/noreallyimfine)|[<img src="https://ca.slack-edge.com/T4JUEB3ME-UL5V3G7A9-f4a14f4623d7-512" width="200" />](https://github.com/JohnMorrisonn)|[<img src="https://ca.slack-edge.com/T4JUEB3ME-UJ5GAHMS7-abc28b1e9d94-512" width="200" />](https://github.com/SamH3pn3r)|


## Project Overview

The idea of this project was to develop an email app similar to Gmail, Edison mail, Yahoo mail, etc. but with better organization to help you find emails easier. For the DS, we built an API that generates tags for all emails so they can be put into folders by the BE.

[Trello Board](https://trello.com/b/39GG7MwY/tagger-smarter-email)

[Product Canvas](https://www.notion.so/Tagger-Smarter-Email-01673a2ed9e54cb8834b959ad39f7de2)

[Tagger - Smarter Email](https://taggerhq.com/)

### Tech Stack

 -   Language: [Python](https://docs.python.org/)
 -   Libraries: [Pandas](https://pandas.pydata.org/docs/), [Gensim](https://radimrehurek.com/gensim/), [GoogleAPI](https://developers.google.com/docs/api), [NLTK](https://www.nltk.org/), [Spacy](https://spacy.io/api/doc), [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), and [Flask](https://flask.palletsprojects.com/en/1.1.x/)
 -   Services: [AWS Elastic Beanstalk](https://docs.aws.amazon.com/elastic-beanstalk/index.html)

 

### Predictions

Our production topic model uses a Spacy pipeline with a Gensim LDAMulticore modeler and an NLTK tokenizer. The output from this model is run through multiple iterations, the results are weighted for frequency, and a descending sort is applied. The final output is a clean sorted list of smart tags that apply per email. This list of tags is packaged in a JSON object delivered to the electron application on the user's desktop.

### Data Sources

-   Private User E-mails

### Explanatory Variables

-   Text of the emails 

### Python Notebooks

[Smart Tag Model Hyperparameter Optimization and Training](https://github.com/Lambda-School-Labs/tagger-ds/blob/master/SmartEmailTags.ipynb)

This notebook contains 3 working models for producing smart tags. This work was done by Monica Bustamante.


### How to connect to the data API

Send a POST request to http://tags2.us-east-2.elasticbeanstalk.com/api/tags with the arguments {'id', 'sender', 'subject', 'message'}

## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a [code of conduct](./code_of_conduct.md). Please follow it in all your interactions with the project.

### Issue/Bug Request

 **If you are having an issue with the existing project code, please submit a bug report under the following guidelines:**
 - Check first to see if your issue has already been reported.
 - Check to see if the issue has recently been fixed by attempting to reproduce the issue using the latest master branch in the repository.
 - Create a live example of the problem.
 - Submit a detailed bug report including your environment & browser, steps to reproduce the issue, actual and expected outcomes,  where you believe the issue is originating from, and any potential solutions you have considered.

### Feature Requests

We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

### Pull Requests

If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

#### Pull Request Guidelines

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the README.md with details of changes to the interface, including new plist variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Include the relevant issue number, if applicable.
- You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

### Attribution

These contribution guidelines have been adapted from [this good-Contributing.md-template](https://gist.github.com/PurpleBooth/b24679402957c63ec426).

## Documentation

See [Backend Documentation](https://github.com/Lambda-School-Labs/tagger-be) for details on the backend of our project.

See [Front End Documentation](https://github.com/Lambda-School-Labs/tagger-fe) for details on the front end of our project.

## Additional Notes:
More info on using badges [here](https://github.com/badges/shields)