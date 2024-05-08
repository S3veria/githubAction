from selenium import webdriver
import requests
import base64
from base64 import b64encode
from imgurpython import ImgurClient

# # Initialize the WebDriver using WebDriverManager for Chrome
# driver = webdriver.Firefox()

# # URL of the webpage you want to screenshot
# url = 'https://google.com'

# # Open the webpage
# driver.get(url)

# # Take a screenshot and save it to a file
# driver.save_screenshot('screenshot.png')

# # Close the WebDriver
# driver.quit()


client_id = "6b64323e061f52b"
client_secret = "280dd7ab9026793f38eb7c909b847b15d4a471b5"

client = ImgurClient(client_id, client_secret)

imgur_data=client.upload_from_path("screenshot.png")
imgur_link=imgur_data['link']
imgur_imageid=imgur_data['id']
print(imgur_data)

#Connect to SAM (Segment Anything Model)
def toB64(imgUrl):
    return str(b64encode(requests.get(imgUrl).content))[2:-1]

def localFileToBase64(file_path):
    with open(file_path, "rb") as file:
        image_content = file.read()
        base64_encoded = b64encode(image_content).decode('utf-8')[2:-1]
    return base64_encoded

def imageToBase64(imageName):
    # with open(imageName, 'rb') as file:
    #     base64_image =  str(b64encode(file.read()))[2:-1]
    base64_string = localFileToBase64(imageName)
    return base64_string

api_key = "SG_51a5bc43438ec7d0"
url = "https://api.segmind.com/v1/sam-img2img"

print(requests.get("https://i.imgur.com/nxheF7J.png"))
# Request payload
data = {
  "image": toB64('https://i.imgur.com/nxheF7J.png')
}

# data2={
#     "image":localFileToBase64("screenshot.png")
# }


# response = requests.post(url, json=data, headers={'x-api-key': api_key})
# print(response)
#print(response.json())