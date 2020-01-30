# CurrencyXchange - Currency Conversion & Wallet Services

A simple Django application with integrated Django Rest Framework.

Tech used: Python, Django, Django Rest Framework, SQLite, Bootstrap and third-party libraries.

Back-end is exposed as a Rest API. Front-end is made fully responsive, powered by Bootstrap. 

Token authentication has been implemented. The Rest API endpoints can be found in the Postman collections file in the root. 

While making requests from the browser to the API, the Token is stored in the Local Storage of the browser.

### Features:

*   Users can sign up/sign in
*   Users can create/add money in wallet
*   Users can check/convert currency prices in different currencies
*   Users can upload profile picture

### Run:

*   `git clone https://github.com/PraneethKarnena/CurrencyXchange.git`
*   `cd CurrencyXchange-master`
*   Add environment variables in `ENV_VARS.sh`
*   `bash ENV_VARS.sh` (valid for *nix environments)
*   `pip install -r requirements.txt`
*   `python manage.py runserver`
