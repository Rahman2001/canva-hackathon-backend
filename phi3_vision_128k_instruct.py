import requests, base64
import os
import json
from dotenv import load_dotenv

import nvidia_asset_api


def __get_key__(key_name):
    invoke_url = os.getenv('nvidia-phi3-vision-128k-instruct-url')
    api_key = os.getenv('nvidia-phi3-vision-128k-instruct-key')
    if key_name:
        if key_name == 'invoke_url':
            return invoke_url
        elif key_name == 'api_key':
            return api_key
        return None
    return None


def make_inference_request(file_path, stream=False):
    load_dotenv()
    vision_model_data_json = open('nvidia-phi3-vision-128k-model-prompt-train.json', encoding='utf8')

    print(f'\n\nFile path is {file_path}\n')
    with open(f'{file_path}', "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()

    headers = {
        "Authorization": f'Bearer {__get_key__("api_key")}',
        "Accept": "text/event-stream" if stream else "application/json"
    }

    payload = json.load(vision_model_data_json)
    asset_id = ''
    if not len(image_b64) < 180_000:
        response = nvidia_asset_api.create_asset(file_path.replace('/', '-')
                                                 .replace('.png', '').replace('.img', '').replace('.zip', ''))
        print(f'\n\nThis is nvidia create asset response: {response}\n')
        response_json = json.loads(response.text)
        asset_id = response_json['assetId']
        print(f"Asset is created, status code: {response.status_code}, asset_id: {asset_id}")

        response = nvidia_asset_api.upload_asset(response_json['uploadUrl'], response_json['description'], file_path)
        print(f"Asset is uploaded, status code: {response.status_code}")
        print(f'Asset description: {response_json["description"]}')

        payload['messages'][0]['content'] = (payload['messages'][0]['content'].replace('{image_b64}', asset_id)
                                             .replace('base64', 'asset_id'))
        headers['NVCF-INPUT-ASSET-REFERENCES'] = asset_id
    else:
        payload['messages'][0]['content'] = payload['messages'][0]['content'].replace('{image_b64}', image_b64)

    response = requests.post(__get_key__("invoke_url"), headers=headers, json=payload)

    # if stream:
    #     for line in response.iter_lines():
    #         if line:
    #             print(line.decode("utf-8"))
    # else:
    #     print(response.json())

    del_response = nvidia_asset_api.delete_asset(asset_id)
    if del_response.status_code == 204:
        print(f'Asset was deleted, status code: {del_response.status_code}')
    else:
        print("Could not delete asset!")

    os.remove(file_path)
    if not os.listdir(file_path.split('/')[0]):
        os.rmdir(file_path.split('/')[0])

    return response.json()
