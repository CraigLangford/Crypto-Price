import difflib
import json
import requests

API_LINK = ("https://min-api.cryptocompare.com"
            "/data/price?fsym={from_symbol}&tsyms={to_symbol}")
USER_LOCATION_LINK = ("https://api.amazonalexa.com/v1/devices/{device_id}"
                      "/settings/address/countryAndPostalCode")
DEFAULT_CRYPTO = 'Bitcoin'
DEFAULT_CURRENCY = 'US Dollars'


def crypto_price_lambda(event, session):
    """
    Takes a request from the Alexa Skill Kit (ASK) as a dictionary (event) and
    returns a dictionary formatted in the ASK format. This is
    done by the following steps:

    1. The intent is collected from the request data in the event. This can be
       the following:
         * Launch Request - When the user first opens Crypto Price
         * Intent Request - When the user wants the price of a cryptocurrency
         * Help Intent - When the user asks for help from the application
         * Cancel Intent / Stop Intent - When the user wants to stop the app
    2. The task is delegated based on the intent to collect the required data
    3. The response is built based on the information from the bespoke task
    4. If the user has not enabled access to their country (for automatic
       currency selection) a request for them to enable their location is added
       to the message
    5. The response is returned to ASK
    """
    request_type = event['request'].get('type')

    if request_type == 'LaunchRequest':
        title = "Crypto Price Trends"
        response_message = ("Welcome to crypto price. Please ask a question "
                            "like: What is the price of bitcoin")
        should_end_session = False
        location_permission = False
    elif request_type == 'IntentRequest':
        request_intent = event['request']['intent']['name']
        if request_intent == 'GetCryptoPriceIntent':
            crypto_details = collect_crypto_price(event, session)
            title, response_message, location_permission = crypto_details
            should_end_session = True
        elif request_intent == 'AMAZON.HelpIntent':
            title = "Crypto Price Help"
            response_message = ("Crypto price returns the price of the "
                                "leading cryptocurrencies. You can ask "
                                "questions like: What is the price of "
                                "bitcoin, tell me the current price of monero "
                                "in US dollars, and, what is the price of "
                                "litecoin in pounds. Please ask a question.")
            should_end_session = False
            location_permission = True
        elif request_intent in ['AMAZON.StopIntent', 'AMAZON.CancelIntent']:
            title = "Crypto Price Cancel"
            response_message = ("Thanks for using crypto price. See you at "
                                "the moon.")
            should_end_session = True
            location_permission = True
    return build_response(card_title=title,
                          card_content=response_message,
                          output_speech=response_message,
                          should_end_session=should_end_session,
                          location_permission=location_permission)


def collect_crypto_price(event, session):
    """
    Extracts the cryptocurrency, finds the nearest match, and returns
    its price. If the financial currency is supplied the amount returned
    is in that currency. Otherwise the price is returned based on where
    the user is asking from.
    """
    location_permission = True
    slots = event['request']['intent']['slots']
    crypto_currency = slots['cryptocurrency'].get('value', DEFAULT_CRYPTO)
    currency = slots['Currency'].get('value', None)
    if not currency:
        currency = DEFAULT_CURRENCY
        permissions = event['context']['System']['user']['permissions']
        if permissions == {}:
            location_permission = False
        else:
            device_id = event['context']['System']['device']['deviceId']
            consent_token = "Bearer " + permissions['consentToken']
            headers = {'Authorization': consent_token}
            location_api_link = USER_LOCATION_LINK.format(device_id=device_id)
            response = requests.get(location_api_link, headers=headers)
            country_code = response.json().get('countryCode', DEFAULT_CURRENCY)
            with open('data/country_to_currency.json', 'r') as c2c_file:
                COUNTRIES_TO_CURRENCIES = json.load(c2c_file)
            currency = COUNTRIES_TO_CURRENCIES[country_code]

    with open('data/cryptocurrencies.json', 'r') as cryptocurrency_file:
        SUPPORTED_COINS = json.load(cryptocurrency_file)
    from_currency, from_symbol = get_key_and_value_match(crypto_currency,
                                                         SUPPORTED_COINS,
                                                         DEFAULT_CRYPTO)

    with open('data/currencies.json', 'r') as currency_file:
        SUPPORTED_CURRENCIES = json.load(currency_file)
    if currency:
        to_currency, to_symbol = get_key_and_value_match(currency,
                                                         SUPPORTED_CURRENCIES,
                                                         DEFAULT_CURRENCY)
    else:
        to_currency = DEFAULT_CURRENCY
        to_symbol = SUPPORTED_CURRENCIES[DEFAULT_CURRENCY]

    api_link = API_LINK.format(from_symbol=from_symbol, to_symbol=to_symbol)
    api_response = requests.get(api_link)
    api_price = json.loads(api_response.content).get(to_symbol, 'Unavailable')

    title = "{from_currency} Price in {to_currency}".format(
                from_currency=from_currency,
                to_currency=to_currency
            )
    response_message = ("{from_currency} is currently worth {value}"
                        " {to_currency}")
    response_message = response_message.format(from_currency=from_currency,
                                               value=api_price,
                                               to_currency=to_currency)

    return title, response_message, location_permission


def get_key_and_value_match(key_word, dictionary, default_key_word):
    """
    Takes a key word and finds the key or value inside the dictionary which
    matches it and returns the corresponding key and value pair. If there is
    no direct match, the nearest key or value is then found.
    Dictionary is expected to be with lower case keys and upper case values.
    """
    reverse_dictionary = {dictionary[k]: k for k in dictionary}
    if key_word in dictionary:
        key = key_word
        value = dictionary[key_word]
    elif key_word in reverse_dictionary:
        key = reverse_dictionary[key_word]
        value = key_word
    else:
        all_names = {k.lower(): k for k in dictionary.keys()}
        all_names.update({v.lower(): v for v in dictionary.values()})
        closest_guesses = difflib.get_close_matches(key_word.lower(),
                                                    all_names)
        if len(closest_guesses) > 0:
            closest_guess = all_names[closest_guesses[0]]
            if closest_guess in dictionary.keys():
                key = closest_guess
                value = dictionary[closest_guess]
            elif closest_guess in reverse_dictionary.keys():
                key = reverse_dictionary[closest_guess]
                value = closest_guess
        else:
            key = default_key_word
            value = dictionary[default_key_word]

    return key, value


def build_response(
        card_title="Crypto Price",
        card_content="Returns price of a cryptocurrency",
        output_speech="Welcome to cryptoprice",
        should_end_session=True,
        location_permission=True):
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
    if not location_permission:
        ask_response = add_permission_request(ask_response, output_speech)
    return ask_response


def add_permission_request(response, original_message):
    """
    Changes the response card to ask for location permissions and adds to the
    output speech to alert user to enable location settings for app.
    """
    permission_card = {
        "type": "AskForPermissionsConsent",
        "permissions": [
            "read::alexa:device:all:address:country_and_postal_code"
        ]
    }
    permission_message = ("To get your country's currency automatically, "
                          "please enable location permissions for crypto "
                          "price in your alexa app")

    response['response']['card'] = permission_card
    new_message = '. '.join([original_message, permission_message])
    response['response']['outputSpeech']['text'] = new_message

    return response