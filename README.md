# PhillyBot
A Telegram bot that gives you the latest news and scores on your favorite Philadelphia sports teams.

Add the bot here: telegram.me/Phillybot

## Deployment Instructions
* Create virtualenv venv (make sure it's python 2.7)
* pip install -r requirements.txt
* create a Python AWS Lambda function
* Copy venv/lib/python2.7/site-packages to root directory
* Zip up everything in the root directory except for the virtual environment
* Upload to AWS as the lambda function
* Create endpoint in AWS API Gateway
* Add POST method to API gateway and have it route to the Lambda function
* Create stage in API gateway and deploy API
* Copy URL from the API Gateway
* Set the bot's webhook by curling the telegram API setWebHook method
* Start chatting w/ bot!!