
# Alexa App Part 2 - AWS Lambda Function

Having set up an Alexa Skill Kit application in the last section of this blog series [here](LINK TO OTHER POST) we can now start handling the logic to actually handle the request. This is handled by an AWS Lambda function which simply takes a json file and returns a json response which will be passed on to the user. This json interface allows any software language to be used for the Lambda function, and in this case we will be using Python.

## Creating the Response

From the documentation the incoming information is separated into the current event as well as the session information. Therfore we'll create our lambda app, cryptoprice.py and put our lambda function in it. Luckily for us the event and response can be passed as dictionary items so we don't have to worry about loading/dumping the json data.

*cryptoprice.py*


```python
def crypto_price_lambda(event, session):
    response = {}
    return response
```

Obviously this response gives the Alexa Skill Kit no information in how to respond to the user and it will raise an error if attempted. Let's look into the type of response the Alexa Skill Kit will accept. Here is a typical response from the documentation.

*Alexa Skill Kit Request Format*
```
{
    "version": "1.0",
    "response": {
        "card": {
            "type": "Simple",
            "title": "Title in App",
            "content": "This will be the message in the app.",
        },
        "outputSpeech": {
            "type": "PlainText",
            "text": "This is the response the user will hear. Hello!"
        },
        "shouldEndSession": True
    }
}
```

The core response can be seen to contain the version and the response. Further the response is composed of the card, which is the card the user would see in their Alexa App, the output speech, which is what the user will hear, and whether to end the session or not. Now that we have this we can create a simple function which generates the boilerplate around our desired response.

*Lambda Function Plus Alexa Skill Kit Response Building Function*


```python
def crypto_price_lambda(event, session):
    response = build_response()
    return response

def build_response(
        card_title="Crypto Price",
        card_content="Returns price of a cryptocurrency",
        output_speech="Welcome to cryptoprice",
        should_end_session=True):
    """
    Builds a valid ASK response based on the incoming attributes.
    """
    ask_response = {
        "version": "1.0",
        "response": {
            "card": {
                "type": "Simple",
                "title": card_title,
                "content": card_content,
            },
            "outputSpeech": {
                "type": "PlainText",
                "text": output_speech
            },
            "shouldEndSession": should_end_session
        }
    }
    return ask_response

```

Great! Now we should have Alexa respond to any request and say "welcome to cryptoprice" to the user, however, this has no functionality based on the type of request the user makes. From [Alexa App Part 1 - Alexa Skills Kit Application](LINK) we found that all Alexa Skills Kit applications ship with four main request types, namely, the LaunchRequest, HelpIntent, StopIntent and CancelIntent. Furthermore, we added a new intent for our application, the CryptoPriceIntent which is where the core functionality of our application is launched.

## Interpreting the Request

To understand what request the user has been created we must look into the structure of the request being passed to our Lambda function. From the documentation it looks something like below.

*Example Request Format*
```
{
    "version": "1.0",
    "session": {
        "sessionId": "SessionId.7k8jtwl-i43fakadph98-x524-2c33b72ec820",
        "application": {
            "applicationId": "amzn1.ask.skill.eibuosp910poix"
        },
        "attributes": {},
        "user": {"userId": "31849190191"},
        "new": True
    },
    "request": {
        "type": "IntentRequest",
        "requestId": "EdwRequestId.7829c7cd1-f281-48oq-891e-839271a9p19nd",
        "locale": "en-US",
        "timestamp": "2017-04-26T00:41:00Z",
        "intent": {
            "name": "GetCryptoPriceIntent",
            "slots": {
                "Currency": {
                    "name": "Currency"
                    "value": "US dollars"
                },
                "cryptocurrency": {
                    "name": "cryptocurrency",
                    "value": "bitcoin"
                }
            }
        }
    },
    "context": {
        "System": {
            "application": {
                "applicationId": "string"
            },
            "user": {
                "userId": "string",
                "permissions": {
                },
                "accessToken": "string"
            },
            "device": {
                "deviceId": "string",
                "supportedInterfaces": {
                    "AudioPlayer": {}
                }
            },
            "apiEndpoint": "string"
        }
    }
}

```

Here we can see that again there is the version number and the request at the base level, however, the context is passed as well. This will come in useful later when we want to gather the user's country information to decide which currency to respond in. As there are two main request types, the LaunchRequest (when the app is launched) and IntentRequest (for the HelpIntent, CancelIntent, StopIntent and GetCryptoPriceIntent). We will update our lambda function to delegate based on this. For many of the responses we can simply respond with a message, once this is done our only task left is to handle the GetCryptoPriceIntent.

Below it can be seen that depending on the case the title, response message and should end session information is updated. To keep things simple notice that the card message as well as the speech output are the same.

*Delegating the Request Types*


```python
def crypto_price_lambda(event, session):
    request_type = event['request'].get('type')

    if request_type == 'LaunchRequest':
        title = "Crypto Price Trends"
        response_message = ("Please ask a question like: What is the price of"
                            " bitcoin")
        should_end_session = False
    elif request_type == 'IntentRequest':
        request_intent = event['request']['intent']['name']
        if request_intent == 'GetCryptoPriceIntent':
            # TODO: Delegate logic to collect cryptoprice details
            pass
        elif request_intent == 'AMAZON.HelpIntent':
            title = "Crypto Price Help"
            response_message = ("Crypto Price returns the price of the "
                                "leading cryptocurrencies. You can ask "
                                "questions like: What is the price of "
                                "bitcoin, tell me the current price of monero "
                                "in US dollars, and, what is the price of "
                                "litecoin in pounds. Please ask a question.")
            should_end_session = False
        elif request_intent in ['AMAZON.StopIntent', 'AMAZON.CancelIntent']:
            title = "Crypto Price Cancel"
            response_message = ("Thanks for using crypto price. See you at "
                                "the moon.")
            should_end_session = True
    return build_response(card_title=title,
                          card_content=response_message,
                          output_speech=response_message,
                          should_end_session=should_end_session,
                          location_permission=location_permission)
```

## Handling the logic to gather the cryptoprice

Our app can now respond nearly every type of response, except for the one we actually built the app for! This function will be taking the desired cryptocurrency, and if the user specified, the cryptocurrency and look up the price. Looking around http://cryptocompare.com/api it seems we can convert any cryptoprice to any world currency. This can be achieved by making a request to https://min-api.cryptocompare.com/data/price?fsym={from_symbol}&tsyms={to_symbol} and subbing in the 3 letter symbol of the cryptocurrency (BTC for Bitcoin) for the from_symbol and the 3 letter symbol of the world currency (USD for US dollars) to the to_symbol. [Here's the link](https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD) for USD to BTC as an example. The trick here, of course will be converting the users request to the correct three letter symbol. Let's create a function which takes the event and returns the title for the response card and the message to be said and shown. This will use additional json dictionaries based on the cryptocurrencies and currencies the API supports.

*Handling the Cryptocurrency Logic*


```python
API_LINK = ("https://min-api.cryptocompare.com"
            "/data/price?fsym={from_symbol}&tsyms={to_symbol}")

def collect_crypto_price(event):
    slots = event['request']['intent']['slots']
    crypto_currency = slots['cryptocurrency'].get('value')
    currency = slots['currency'].get('value')

    SUPPORTED_COINS = json_to_dictionary('data/cryptocurrencies.json')
    from_symbol = SUPPORTED_COINS.get(crypto_currency)

    SUPPORTED_CURRENCIES = json_to_dictionary('data/currencies.json')
    to_symbol = SUPPORTED_CURRENCIES.get(currency)

    api_link = API_LINK.format(from_symbol=from_symbol, to_symbol=to_symbol)
    api_response = requests.get(api_link)
    api_price = api_response.json().get(to_symbol, 'Unavailable')

    title = "{from_currency} Price in {to_currency}".format(
                from_currency=crypto_currency,
                to_currency=currency
            )
    response_message = ("{from_currency} is currently worth {value}"
                        " {to_currency}")
    response_message = response_message.format(from_currency=crypto_currency,
                                               value=api_price,
                                               to_currency=currency)

    return title, response_message
```

The above example sufficient in taking a crypto currency and world currency and making a get request through the cryptocompare API to gather the current conversion rate of the two currencies. This should be enough for the extent of this tutorial, giving us a working Lambda function which can return the price of a cryptocurrency when given the name of the cryptocurrency and the world currency. The final file can be seen below.

*Final Lambda Function File*


```python
API_LINK = ("https://min-api.cryptocompare.com"
            "/data/price?fsym={from_symbol}&tsyms={to_symbol}")

def crypto_price_lambda(event, session):
    request_type = event['request'].get('type')

    if request_type == 'LaunchRequest':
        title = "Crypto Price Trends"
        response_message = ("Please ask a question like: What is the price of"
                            " bitcoin")
        should_end_session = False
    elif request_type == 'IntentRequest':
        request_intent = event['request']['intent']['name']
        if request_intent == 'GetCryptoPriceIntent':
            title, response_message = collect_crypto_price(event)
        elif request_intent == 'AMAZON.HelpIntent':
            title = "Crypto Price Help"
            response_message = ("Crypto Price returns the price of the "
                                "leading cryptocurrencies. You can ask "
                                "questions like: What is the price of "
                                "bitcoin, tell me the current price of monero "
                                "in US dollars, and, what is the price of "
                                "litecoin in pounds. Please ask a question.")
            should_end_session = False
        elif request_intent in ['AMAZON.StopIntent', 'AMAZON.CancelIntent']:
            title = "Crypto Price Cancel"
            response_message = ("Thanks for using crypto price. See you at "bbz
                                "the moon.")
            should_end_session = True
    return build_response(card_title=title,
                          card_content=response_message,
                          output_speech=response_message,
                          should_end_session=should_end_session,
                          location_permission=location_permission)


def build_response(
        card_title="Crypto Price",
        card_content="Returns price of a cryptocurrency",
        output_speech="Welcome to cryptoprice",
        should_end_session=True):
    """
    Builds a valid ASK response based on the incoming attributes.
    """
    ask_response = {
        "version": "1.0",
        "response": {
            "card": {
                "type": "Simple",
                "title": card_title,
                "content": card_content,
            },
            "outputSpeech": {
                "type": "PlainText",
                "text": output_speech
            },
            "shouldEndSession": should_end_session
        }
    }
    return ask_response


def collect_crypto_price(event):
    slots = event['request']['intent']['slots']
    crypto_currency = slots['cryptocurrency'].get('value')
    currency = slots['currency'].get('value')

    SUPPORTED_COINS = json_to_dictionary('data/cryptocurrencies.json')
    from_symbol = SUPPORTED_COINS.get(crypto_currency)

    SUPPORTED_CURRENCIES = json_to_dictionary('data/currencies.json')
    to_symbol = SUPPORTED_CURRENCIES.get(currency)

    api_link = API_LINK.format(from_symbol=from_symbol, to_symbol=to_symbol)
    api_response = requests.get(api_link)
    api_price = api_response.json().get(to_symbol, 'Unavailable')

    title = "{from_currency} Price in {to_currency}".format(
                from_currency=crypto_currency,
                to_currency=currency
            )
    response_message = ("{from_currency} is currently worth {value}"
                        " {to_currency}")
    response_message = response_message.format(from_currency=crypto_currency,
                                               value=api_price,
                                               to_currency=currency)

    return title, response_message
```

## Final Thoughts

You can see the full source code on github [here](https://github.com/CraigLangford/Crypto-Price) and see that there has been logic added to the collect_crypto_price function. This is to handle the following edge cases:

* When the world currency isn't supplied - the app defaults to the country where the user is
* When a 3 letter name is specified
* If the Alexa Skill Kit app sends a typo - Python's native difflib.get_close_matches is used to guess the nearest match for the user

That's it! You now have a working Lambda function that you can pair with your Alexa Skills Kit application. See [deployment](https://github.com/CraigLangford/Crypto-Price#deployment) for how to upload your function to AWS and to actually use it!
