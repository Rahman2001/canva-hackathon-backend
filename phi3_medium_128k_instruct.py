import requests
import json
import os
import ssl
from dotenv import load_dotenv


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


allowSelfSignedHttps(True)  # this line is needed if you use self-signed certificate in your scoring service.


def __get_key__(key_name):
    url = os.getenv('phi3-medium-128k-instruct-url')
    api_key = os.getenv('phi3-medium-128k-instruct-key')
    if key_name == 'url':
        return url
    elif key_name == 'api_key':
        return api_key
    return None


def make_inference_request(request):
    load_dotenv()
    medium_model_data_json = open('ms-phi3-medium-128k-model-prompt-train.json', encoding='utf8')

    print(f'This is request: {request}')
    data = json.load(medium_model_data_json)
    data['messages'][-1]['content'] = request['content']
    url = __get_key__('url')
    api_key = __get_key__('api_key')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.post(url, headers=headers, json=data)
    print(response)
    return response.json()
