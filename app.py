import os
import re

import requests

import phi3_vision_128k_instruct
import phi3_medium_128k_instruct
from zipfile import ZipFile
from flask import Flask, request
# from flask_ngrok import run_with_ngrok
from flask_cors import CORS

app = Flask(__name__)
# run_with_ngrok(app)
CORS(app)


@app.route('/canva-design/eval', methods=['POST'])
def main():
    list_json = __get_image_list__(request.get_json())
    file_path = list_json['file_path']
    image_list = list_json['image_list']
    print(f'\n\nTHis is image_list: {image_list}\n')
    aggregated_resp = {"content": ""}
    for image in image_list:
        vision_resp = phi3_vision_128k_instruct.make_inference_request(file_path + "/" + image)
        print(f'This vision response: {vision_resp}')
        if not aggregated_resp['content'] == "":
            vision_resp['choices'][0]['message']['content'] = " \n\n" + vision_resp['choices'][0]['message']['content']
        aggregated_resp['content'] = aggregated_resp['content'] + vision_resp['choices'][0]['message']['content']
    medium_resp = phi3_medium_128k_instruct.make_inference_request(aggregated_resp)
    return medium_resp


def __get_image_list__(canva_request):
    url = canva_request['blob_url']
    file_name = re.search('(\d+-\d+\\.png)|(\d+-\d+\\.img)|(\d+-\d+\\.zip)', url)[0]
    print('File name in Canva: {}'.format(file_name))
    file_stream = requests.get(
        url=url,
        stream=True)

    image_list = []
    file_metadata = file_name.split('.')
    print(f'File metadata: {str(file_metadata)}')
    file_path = file_metadata[0] + "/" + file_name
    os.mkdir(file_metadata[0])  # create a directory with a name of file

    with open(f'{file_path}', 'wb') as file:
        file.write(file_stream.content)

    if file_metadata[1] == 'zip':
        ZipFile(file_path).extractall(file_metadata[0])  # extract from zip file to destination directory
        os.remove(file_path)
        image_list = os.listdir(file_metadata[0])
    else:
        image_list.append(file_name)
    return {'file_path': file_metadata[0], 'image_list': image_list}


if __name__ == '__main__':
    app.run(debug=True)
