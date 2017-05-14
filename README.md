
# Crypto Price - Alexa Skills Kit Application

Crypto Price is an Amazon Web Services (AWS) Lambda Function that pairs with the Alexa Skills Kit (ASK) to respond to an Amazon Echo user's request for the current price of any leading cryptocurrency (such as Bitcoin, Ethereum, Monero, Litecoin, etc.) in any world currency. By default the function will return the price in US Dollars, however, if a user specifies a currency it will return the price in that currency. Furthermore, if the user enables the app location permissions on their Alexa App it will return the price in the currency of their current country. Some typical questions and responses are as follows:

---

> **User**: Alexa, tell me the price of Bitcoin from Crypto Price. *(location disabled by the user)*
>
> **Alexa**: The current price of Bitcoin is 1,487.91 US dollars.

---

> **User**: Alexa, open Crypto Price and tell me the price of Ethereum. *(location enabled by the user and they live in the United Kingdom)*
> 
> **Alexa**: The current price of Ethereum is 53.72 pounds.

---

> **User**: Alexa, load Crypto Price.
> 
> **Alexa**: Welcome to Crypto Price. Please ask a question like: What is the price of Bitcoin?
>
> **User**: Give me the price of Monero in yen.
>
> **Alexa**: The current price of Monero is 3,070.75 yen.

---

> **User**: Alexa, get help from Crypto Price.
>
> **Alexa**: Crypto Price returns the price of the leading cryptocurrencies in any country's currency. You can ask questions like...

---

## Getting Started

These instructions will you get a copy of the project up and running on your local machine for deployment and testing purpose. Please checkout the [blogpost](docs/blogpost.md) for full deployment details and how to integrate the app with the Alexa Skill Kit.

### Prerequisites

This app runs using Python 3.6.1. Please checkout [www.python.org](https://www.python.org) to install it on your own system. It is recommended to build the project in a contained virtual environment. This can be achieved with a combination of [Virtualenv](https://virtualenv.pypa.io/en/stable/) and the [Virtualenv Wrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) which allows you to create and delete Virtualenvs easily. 

### Installing

The first step to installing the app is to clone the git repository:

```bash
$ git clone https://github.com/CraigLangford/Crypto-Price.git
```

If you have virtualenv and virtualenvwrapper installed (See [Prerequisites](#prerequisites)), create your Python 3.6 environment.

```bash
$ mkvirtualenv --python=python3.6 cryptoprice
```

You can set the root directory of the project as well so whenever you run `workon cryptoprice` you'll be in your virtualenv in your root folder immediately.

```bash
$ setvirtualenvproject
```

You should now be in the root directory with Python 3.6.x as your Python version.

```bash
$ ls
cryptoprice.py  data  docs  LICENSE  README.md  requirements.txt  setup.py  test_cryptoprice.py
$ python --version
Python 3.6.1
```

For API requests the project uses [requests](http://docs.python-requests.org/en/master/) and for testing it uses [Pytest](https://docs.pytest.org/en/latest/). To install these simply install via the requirements file.

```bash
$ pip install --requirement requirements.txt
```

That's it! You're now set up to work locally. You can build some tests in test_cryptoprice.py to test locally (see [Running the Tests](#running-the-tests)) or checkout the steps from [Deployment](#deployment) to set up the project as an Amazon Lambda function and integrate it with your own Alexa Skills Kit App!

## Running the Tests

Pytest is used for testing the application, and is included in the requirements.txt file. If you already followed the steps in [Installing](#installing) and you're good to go! Just run the following on the root directory of the project to run the tests for the project. *Note: You must have an internet connection as the app will gather the prices from [www.cryptocompare.com](www.cryptocompare.com)*

```bash
$ py.test
```

## Deployment

To deploy the system as an Amazon Lambda function you must create a zip composed of the core cryptoprice.py file, the data directory and the third party requests module. This is handled by the setup.py script which can be run in the root directory as below.

```bash
$ python setup.py
```

This will generate a cryptoprice.zip file which can be uploaded as your lambda function to AWS Lambda.

## Contributing

## Authors

* **Craig Langford** - *Initial Work* - https://github.com/CraigLangford

Please feel free to contribute to be added to the project!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* Hats off to to [www.cryptocompare.com](https://www.cryptocompare.com) for their easy to use and extensive [API](https://www.cryptocompare.com/api)
