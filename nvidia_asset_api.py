import os
from dotenv import load_dotenv
import requests

load_dotenv()


def __get_key__(key_name):
    nvidia_ngc_key = os.getenv('nvidia-ngc-key')
    asset_create_url = os.getenv('nvidia-cloud-asset-create-url')
    asset_delete_url = os.getenv('nvidia-cloud-asset-delete-url')
    asset_list_url = os.getenv('nvidia-cloud-asset-list-url')
    if key_name:
        if key_name == 'nvidia_ngc_key':
            return nvidia_ngc_key
        elif key_name == 'asset_create_url':
            return asset_create_url
        elif key_name == 'asset_delete_url':
            return asset_delete_url
        elif key_name == 'asset_list_url':
            return asset_list_url
        else:
            return None
    return None


def create_asset(asset_name):
    headers = {
        "Authorization": f'Bearer {__get_key__("nvidia_ngc_key")}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        "contentType": "image/png",
        "description": f'{asset_name}'
    }
    response = requests.post(__get_key__('asset_create_url'), headers=headers, json=payload)
    return response


def upload_asset(upload_url, asset_name, file_path):
    headers = {
        'Content-Type': 'image/png',
        'x-amz-meta-nvcf-asset-description': f'{asset_name}'
    }
    payload = open(file_path, 'rb')
    response = requests.put(upload_url, headers=headers, data=payload)
    return response


def delete_asset(asset_id):
    delete_url = __get_key__('asset_delete_url').replace('{asset_id}', asset_id)
    headers = {
        "Authorization": f'Bearer {__get_key__("nvidia_ngc_key")}'
    }
    response = requests.delete(delete_url, headers=headers)
    return response


def list_assets():
    headers = {
        'Authorization': f'Bearer {__get_key__("nvidia-ngc-key")}',
    }
    response = requests.get(__get_key__("nvidia-cloud-asset-list-url"), headers=headers)
    return response
