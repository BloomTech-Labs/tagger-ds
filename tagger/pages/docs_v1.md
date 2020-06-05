# Taggermail Data Science Documentation <img src="../static/markdown-logo.png" height=20, width=32></img>


## Accessing the API Endpoints

### /api/sync
Input:
```python
{   
    "provider": <email service>,
    "token": [
        {
            "refresh_token": <refresh_token_value>,
            "client_id": <client_id_value>,
            "client_secret": <client_secret_value>,
        },
        ...
    ]
}



```
Output:
```

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