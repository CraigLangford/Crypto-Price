
# Crypto Price - Alexa Skills Kit Application

Crypto Price is an Amazon Web Services (AWS) lambda function which when paired with the Alexa Skills Kit (ASK) can tell an Amazon Echo user the current price of the leading cryptocurrencies (such as Bitcoin, Ethereum, Monero, Litecoin, etc.) in any world currency. By default the function will return the price in US Dollars, however, if a user specifies a currency it will return the price in that currency. Furthermore, if the user enables the app location permissions on their Alexa App it will return the price in the currency of their current country. Some typical questions and responses are as follows:

---

> **User**: Alexa, tell me the price of Bitcoin from Crypto Price. *(location disabled)*

> **Alexa**: The current price of Bitcoin is 1,250 US Dollars.

---

> **User**: Alexa, open Crypto Price and tell me the price of Ethereum. *(location enabled and in the United Kingdom)*

> **Alexa**: The current price of Ethereum is 53.72 pounds.

---

> **User**: Alexa, load Crypto Price.

> **Alexa**: Welcome to Crypto Price. Please ask a question like: What is the price of Bitcoin?

> **User**: Give me the price of Monero in Yen.

> **Alexa**: The current price of Monero is 3,070.75 yen.

---

> **User**: Alexa, get help from Crypto Price.

> **Alexa**: Crypto Price returns the price of the leading cryptocurrencies in any country's currency. You can ask questions like...

---

## Getting Started

These instructions will you get a copy of the project up and running on your local machine for deployment and testing purpose. Please checkout the [blogpost](docs/blogpost.md) for full deployment details and how to integrate the app with the Alexa Skill Kit.

### Prerequisites

This app runs using Python 3.6.1. Please checkout www.python.com to set-up on your own system. It is recommended to build the project in a contained virtual envirnment. You can see more details on the virtualenv project at www.github.com/virtualenv. 

### Installing

The first step to installing the app is to clone the git repository:

```bash
$ git clone https://github.com/CraigLangford/Crypto-Price.git
```

If you have virtualenv and virtualenvwrapper installed (See [Prerequisies](#Prerequisites), create your Python 3.6 environment.

```bash
$ mkvirtualenv --python=python3.6 cryptoprice
```

You can set the root directory of the project as well so whenever you run `workon cryptoprice` you'll be where you need to be immediately.

```bash
$ setvirtualenvproject
```

You should now be in the root directory with Python 3.6 as your Python version.

```bash
$ ls
cryptoprice.py  data  docs  LICENSE  README.md  requirements.txt  setup.py  test_cryptoprice.py
$ python --version
Python 3.6.1
```

For API requests the project uses requests (see www.requests.com) and for testing it uses Pytest. To install these simply install via the requirements file.

```bash
$ pip install --requirement requirements.txt
```

That's it! You're now set up to work locally. You can build some tests in test_cryptoprice.py to test locally (see #Running the Tests) or checkout ##Deployment the project to a Amazon Lambda function to set it up with your own Alexa Skills Kit App!

## Running the Tests

Pytest is used for testing the application, and is included in the requirements.txt file. If you already installed the requirements you're good to go! Just run the following on the root directory of the project.

## Deployment

To deploy the system as an Amazon Lambda function you

## Contributing

## Authors

* **Craig Langford** - *Initial work* - www.github.com/CraigLangford

Please feel free to contribute to be added to the project!

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENCE.md) file for details.

## Acknowledgments

* This project was created using the pricing API 
