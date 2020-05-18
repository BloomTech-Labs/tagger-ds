# Tagger - Smarter Email

[![Maintainability](https://api.codeclimate.com/v1/badges/04429dcdec013a7b9175/maintainability)](https://codeclimate.com/github/Lambda-School-Labs/tagger-ds/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/04429dcdec013a7b9175/test_coverage)](https://codeclimate.com/github/Lambda-School-Labs/tagger-ds/test_coverage) ![MIT](https://img.shields.io/packagist/l/doctrine/orm.svg)
![Typescript](https://img.shields.io/npm/types/typescript.svg?style=flat)
![Netlify Status](https://api.netlify.com/api/v1/badges/b5c4db1c-b10d-42c3-b157-3746edd9e81d/deploy-status)
![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)

You can find the project at `TBD`.

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



🚫 more info on using badges [here](https://github.com/badges/shields)

## Project Overview

[Trello Board](https://trello.com/b/39GG7MwY/tagger-smarter-email)

[Product Canvas](https://www.notion.so/Tagger-Smarter-Email-01673a2ed9e54cb8834b959ad39f7de2)

The idea of this project was to develop an email app similar to Gmail, Edison mail, Yahoo mail, etc. but with better organization to help you find emails easier. For the DS, we built an API that generates tags for all emails so they can be put into folders by the BE.

[Tagger - Smarter Email](https://taggerhq.com/)

### Tech Stack

 -   Languages: JSON, Python
 -   Libraries: Pandas, Scikit-Learn, Pickle, NLTK, and Flask
 -   Services: Flask and AWS EB

### Predictions

The DS API takes in a JSON object of an email, generates a tag, and spits out a JSON object with the previous email information + tag. The current API is using TfidfVectorizer, NLTK wordnet Lemmatizer, regexp_tokenize, and a Random Forest Classifier model.

### Explanatory Variables

-   Text of the emails 

### Data Sources

-   Private E-mails

### Python Notebooks

[Functions for gathering the emails](https://github.com/Lambda-School-Labs/tagger-ds/blob/master/Jay/email_functions.ipynb)

[Model Hyperparameter Optimization and Training](https://github.com/Lambda-School-Labs/tagger-ds/blob/sam-branch/labs_sam(3).ipynb)

[Flask API](https://github.com/Lambda-School-Labs/tagger-ds/blob/sam-branch/API/application.py)


### How to connect to the data API

Send a POST request to http://tags2.us-east-2.elasticbeanstalk.com/api/tags with the arguments {'id', 'sender', 'subject', 'message'}

## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a [code of conduct](./code_of_conduct.md.md). Please follow it in all your interactions with the project.

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

## Accessing the API Endpoints

### /train_model
Input:
```
{   
    "address": <email user>,
    "emails": [
        {
            "uid": <id>,
            "from": <email sender>,
            "subject": <email subject>,
            "msg": <email body text>
            "content_type": <unused, keep as blank string>
        },
        ...
    ]
}

```
Output:
```
"Trained a model!"
```

### /predict
Input:
```
{   
    "address": <email user>,
    "emails": [
        {
            "uid": <email uid (optional)>,
            "from": <email sender>,
            "subject": <email subject>,
            "msg": <email body text>
            "content_type": <unused, keep as blank string>
        } 
    ]
}
```
- "emails" array can have a length > 0, but only the first entry will be taken.
- This endpoint can also be used for predicting what real emails are closest to a hypothetical email.

Output:
```
Array of 5 email UID's closest in content to the selected email 
or "No model in database for this address..."
```

## Launching on EC2 guide

### Creating instance:
1. Go to AWS and look for EC2 service
2. Click on launch Instance
3. Look for the AMI that has the name Ubuntu LTS (latest) with a free tier eligible.
    - For the purpose of this API we do not need a more powerful machine since it is using a pre-trained model.
4. Click next on the bottom right until "Configure Security Group"
    - SSH will be the default first type, look to source, and in the pull down select "My IP" for security reasons.
    - Then "Add Rule", select Type "HTTP" from the dropdown and click "Review and Launch"
5. Click "Launch" and select an existing key pair if you have one; if not go ahead and choose "Create a new key pair" and assign it a name.
    - Once the name is assigned you can "Download Key Pair"
    - Take note of where the .pem key gets downloaded.
6. Accept the agreement and "Launch Instance"
7. Lastly "View Instance"
    - The instance will take a few seconds launching. Once ready right click on the newly launched instance and select "connect"
8. Take a moment to read ssh instructions.
    - The most straightforward way to ssh is through the command line; copy what follows "Example:" into a command line that contains the .pem key.
    - Using an SSH client like "PuTTY" uses GUI and saves the key for future use, follow the guide to use this way of ssh.
### Getting the container up and running:
1. ```wget https://raw.githubusercontent.com/Lambda-School-Labs/tagger-ds/JFDeployedbranch/bootstrap.sh``` in the command line inside the ssh.
    - This step will download "bootstrap.sh"; it has the commands to get docker installed and in theory fully running.
    - Read the bootstrap.sh for more information on what each line is doing.
2. ```sudo sh bootstrap.sh``` will run the shell commands and return an error once it gets to the last line.
    - The error is due to the lack of a ".env" file. Look at "exampleenv" for reference on what the ".env" should look like.
3. ```cd tagger-ds/``` to go change into the directory we cloned with the shell file, that contains "docker-compose.yml
4. ```sudo vim .env``` to open a command line editor(replace `vim` for `nano` for a different command line editor)
    - copy the contents of "https://raw.githubusercontent.com/Lambda-School-Labs/tagger-ds/JFDeployedbranch/exampleenv" into this file.
    - Once inside vim type the letter "a" to transition into `--insert--` mode then press the "esc" key once finished editing.
    - change "BASILICA_KEY=SLOW_DEMO_KEY" for "BASILICA_KEY=[personalkey]"
      ```DATABASE_URL=postgres://test:testp@postgres:5432/testu```
      ```POSTGRES_USER=test```
      ```POSTGRES_PASSWORD=testp```
      ```POSTGRES_DB=testu```
    - change the variables here for more secure credentials for security.
    - exit vim by typing ":wq" This command will write then quit the command line editor.
5. Lastly run ```docker-compose up --build```
    - if running this command returns an error run ```sudo docker-compose up --build``` instead.
### Initialize the database through the cli
##### This API uses the package "click" to securely initialize the database, this command only needs to be run once or any time resetting the database is necessary.
1. Open another ssh client by following the instructions layed out in "Creating instance:# step #8.
    - Able to have multiple command lines connected to the same computer through ssh. Leave the container created in "Getting the container up and running:" up. 
    - The following instructions depend on the container being started to correctly run.
2. ```cd tagger-ds/``` to change into the directory that contains "docker-compose.yml
3. ```docker-compose exec flask tagger db reset``` to get the database initialized with the schemas we made in "db.py"
    - This command will not return any errors if run correctly. It won't return anything in fact.
### The api link:
To find the website that contains this api go back to the EC2 and copy the "Public DNS (IPv4)" that belongs to the instance created for this example.