from .cryptoprice import (
    crypto_price_lambda, collect_crypto_price, get_key_and_value_match
)

EXAMPLE_INTENT_REQUEST = {
    "session": {
        "sessionId": "SessionId.6beee92e-e49fakjdsh73-b514-3c03b7eec660",
        "application": {
            "applicationId": "amzn1.ask.skill.fasjdofsad998fasdj"
        },
        "attributes": {},
        "user": {"userId": "21376468928"},
        "new": True
    },
    "request": {
        "type": "IntentRequest",
        "requestId": "EdwRequestId.768c7cd1-b270-47ab-810e-80208e7e16ed",
        "locale": "en-US",
        "timestamp": "2017-04-26T00:41:00Z",
        "intent": {
            "name": "GetCryptoPriceIntent",
            "slots": {
                "Currency": {"name": "Currency"},
                "cryptocurrency": {
                    "name": "cryptocurrency",
                    "value": "Bitcoin"
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
                    "consentToken": "string"
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
    },
    "version": "1.0"
}


def test_get_key_and_value_match():
    """
    Tests the get_key_and_value_match with various keys and values.
    """
    test_dict = {"Apple": "APC", "Banana": "BNC", "Carrot and Potato": "CAP"}
    args = ("carrot and potato", test_dict, "default")
    assert "Apple", "APC" == get_key_and_value_match(*args)
    args = ("carrot and potato", test_dict, "default")
    assert "Banana", "BNC" == get_key_and_value_match(*args)
    args = ("carrot and potato", test_dict, "default")
    assert "Carrot and Potato", "CAP" == get_key_and_value_match(*args)
    args = ("appl", test_dict, "default")
    assert "Apple", "APC" == get_key_and_value_match(*args)
    args = ("fdsaoijpjo", test_dict, "Apple")
    assert "Apple", "APC" == get_key_and_value_match(*args)


def test_collect_crypto_price_for_various_cryptocurrencies():
    crypto_details = collect_crypto_price(EXAMPLE_INTENT_REQUEST, {})
    title, response_message, location_enabled = crypto_details
    assert title == "Bitcoin Price in US Dollars"
    assert response_message.startswith("Bitcoin is currently worth")
    assert response_message.endswith("US Dollars")

    EXAMPLE_INTENT_REQUEST['request'][
        'intent']['slots']['cryptocurrency']['value'] = "ethereum"
    crypto_details = collect_crypto_price(EXAMPLE_INTENT_REQUEST, {})
    title, response_message, location_enabled = crypto_details
    assert title == "Ethereum Price in US Dollars"
    assert response_message.startswith("Ethereum is currently worth")
    assert response_message.endswith("US Dollars")

    EXAMPLE_INTENT_REQUEST['request'][
        'intent']['slots']['cryptocurrency']['value'] = "doge coin"
    crypto_details = collect_crypto_price(EXAMPLE_INTENT_REQUEST, {})
    title, response_message, location_enabled = crypto_details
    assert title == "Dogecoin Price in US Dollars"
    assert response_message.startswith("Dogecoin is currently worth")
    assert response_message.endswith("US Dollars")

    EXAMPLE_INTENT_REQUEST['request'][
        'intent']['slots']['cryptocurrency']['value'] = "XMR"
    crypto_details = collect_crypto_price(EXAMPLE_INTENT_REQUEST, {})
    title, response_message, location_enabled = crypto_details
    assert title == "Monero Price in US Dollars"
    assert response_message.startswith("Monero is currently worth")
    assert response_message.endswith("US Dollars")


def test_collect_crypto_price_for_nearest_values():
    EXAMPLE_INTENT_REQUEST['request'][
        'intent']['slots']['cryptocurrency']['value'] = "dog coin"
    EXAMPLE_INTENT_REQUEST['request'][
        'intent']['slots']['Currency']['value'] = "camadian dollars"
    crypto_details = collect_crypto_price(EXAMPLE_INTENT_REQUEST, {})
    title, response_message, location_enabled = crypto_details
    assert title == "Dogecoin Price in Canadian Dollars"
    assert response_message.startswith("Dogecoin is currently worth")
    assert response_message.endswith("Canadian Dollars")

    EXAMPLE_INTENT_REQUEST['request'][
        'intent']['slots']['cryptocurrency']['value'] = "XM R"
    crypto_details = collect_crypto_price(EXAMPLE_INTENT_REQUEST, {})
    title, response_message, location_enabled = crypto_details
    assert title == "Monero Price in Canadian Dollars"
    assert response_message.startswith("Monero is currently worth")
    assert response_message.endswith("Canadian Dollars")


def test_crypto_price_lambda_returns_dictionary():
    crypto_price_response = crypto_price_lambda(EXAMPLE_INTENT_REQUEST, {})
    assert type(crypto_price_response) == dict
    assert 'version' in crypto_price_response
    assert 'response' in crypto_price_response


def test_cryptocurrency_returns_correct_format():
    conversion_response = crypto_price_lambda(EXAMPLE_INTENT_REQUEST, {})
    assert 'version' in conversion_response
    assert 'response' in conversion_response
    assert 'card' in conversion_response['response']
    assert 'outputSpeech' in conversion_response['response']
