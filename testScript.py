import requests
from base64 import b64encode

def toB64(imgUrl):
    with open('whatsappImage.jpeg', 'rb') as file:
        file_content = file.read()
    return str(b64encode(file_content))[2:-1]


api_key = "SG_164d0ef213758ed2"
url = "https://api.segmind.com/v1/sam-img2img"

# Request payload
data = {
  "image": toB64('https://segmind.com/kitchen.jpg')
}

response = requests.post(url, json=data, headers={'x-api-key': api_key})
print(response)