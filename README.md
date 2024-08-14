# Canva Apps SDK backend
This repository serves as a backend for [canva-apps-sdk-frontend](https://github.com/Rahman2001/canva-apps-sdk.git) repository. 

## Description
The backend utilizes Microsoft's two AI models from a family of <strong>Phi3</strong>, such as `medium-128k-instruct` and `vision-128k-instruct`.

| Paramaters                                    | Types                       |
|-----------------------------------------------|-----------------------------|
| Input                                         | text, image                 |
| Output                                        | text                        |
| Model (text-to-text)                          | Phi3-medium-128K-instruct   |
| Model (image-to-text)                         | Phi3-vision-128K-instruct   |
| Hosting Server                                | Microsoft Azure             |
| Max Input Token                               | 50K tokens                  |
| Average Output Token (for 2 Canva pages)      | 1200 - 2000 tokens          |
| `Phi3-medium-128K-instruct` model host server | Microsoft Azure AI Services |
| `Phi3-vision-128K-instruct` model host server | NVIDIA Cloud                |

## Requirements
In order to run this application, you need to fill in `.env` file with required values. 

### Phi3-medium-128K-instruct model
This model is hosted on <strong>Microsoft Azure AI Services</strong> platform. User needs to get subscription and deploy the model.
After successful deployment, you get url and API key for accessing a model with REST API. </br>
In my case, I chose `East US2` location for deployment of the model and got URL `https://Phi-3-medium-128k-instruct-hnett.eastus2.models.ai.azure.com/v1/chat/completions`


### Phi3-vision-128K-instruct model
This model is hosted on <strong>NVIDIA Cloud</strong> which can be accessible for free with <strong>NVIDIA Developer Program</strong> subscription.
NVIDIA offers free 1000 credits for usage of REST API. User needs to obtain API key in <strong>NVIDIA NGC</strong>. The URL should look like `https://ai.api.nvidia.com/v1/vlm/microsoft/phi-3-vision-128k-instruct`.

### Other requirements
Other requirements can be seen in `requirements.txt` file which can be executed with command:

```bash
pip install -r requirements.txt
```

## Flow Diagram
![Backend flow diagram](https://github.com/Rahman2001/canva-hackathon-backend/blob/master/canva%20ai%20hackthon%20backend%20diagram.drawio.png)

## Demo Video on YouTube
[Watch my demo on YouTube](https://youtu.be/4LA7YT-4vLU?si=Jyv_UQzl-fFJrdQc)