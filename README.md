# Reddit OpenAI Bot

A Reddit bot that uses the text-davinci-003 model from the OpenAI API to respond to posts.

## Install Requirements
```
pip3 install -r requirements.txt 
```
## Environment Vars
Store all required environment variables in the ```.env``` file.
## Prompt
Update prompt in ```prompts.txt``` to tailor responses.

## Run
```
nohup python3 -u app.py &
```