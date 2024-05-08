from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions
import math
import time
import replicate
from PIL import Image
from io import BytesIO
import requests
import os
os.environ["REPLICATE_API_TOKEN"] = "r8_ZyYveKUp6ihp2v1gnxxsFCv4MfIl1eF1RXRW4"

# Initialize the WebDriver using WebDriverManager for Chrome
def clickOnCoordinateInUrl(url, originalSize, coordinatesToClick):
    driver = webdriver.Firefox()
    driver.get(url)
    body=driver.find_element(By.TAG_NAME,'body')
    body_size=body.size
    body_center=(body_size['width']/2, body_size['height']/2)#width, height
    xProp=body_size['width']/originalSize[0] 
    yProp=body_size['height']/originalSize[1]
    #Resize to body
    resizedXCoordianate=math.floor((coordinatesToClick[0]*xProp)-body_center[0]) if math.floor((coordinatesToClick[0]*xProp)-body_center[0])>0 else math.ceil((coordinatesToClick[0]*xProp)-body_center[0])
    resizedYCoordinate=math.floor((coordinatesToClick[1]*yProp)-body_center[1]) if math.floor((coordinatesToClick[1]*yProp)-body_center[1])>0 else math.ceil((coordinatesToClick[1]*yProp)-body_center[1])
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(body, resizedXCoordianate, resizedYCoordinate) #x and then y?
    action.click()
    action.perform()

def exploreAction(url, actionName, originalSize, coordinatesToClick):
    """
    #Example call: url, original screen size,coordinate to click
    exploreAction("http://www.google.com", "Click Searchbar", (1920,1162), (878,483))
    """
    # opts = FirefoxOptions()
    # opts.add_argument("--headless")
    # driver = webdriver.Firefox(options=opts)
    driver = webdriver.Firefox()

    driver.get(url)
    body=driver.find_element(By.TAG_NAME,'body')
    body_size=body.size
    body_center=(body_size['width']/2, body_size['height']/2)#width, height
    xProp=body_size['width']/originalSize[0]
    yProp=body_size['height']/originalSize[1]
    #Resize to body
    resizedXCoordianate=math.floor((coordinatesToClick[0]*xProp)-body_center[0]) if math.floor((coordinatesToClick[0]*xProp)-body_center[0])>0 else math.ceil((coordinatesToClick[0]*xProp)-body_center[0])
    resizedYCoordinate=math.floor((coordinatesToClick[1]*yProp)-body_center[1]) if math.floor((coordinatesToClick[1]*yProp)-body_center[1])>0 else math.ceil((coordinatesToClick[1]*yProp)-body_center[1])
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(body, resizedXCoordianate, resizedYCoordinate) #x and then y?
    action.click()
    action.perform()
    imageName=url.replace("https://www.","").replace("http://www.","").replace("www.","").replace(".","_")
    imageName=f'{imageName}[{actionName}].png'
    time.sleep(2)
    driver.save_screenshot(imageName)
    img = open(imageName, "rb")
    output = replicate.run(
        "pablodawson/segment-anything-automatic:14fbb04535964b3d0c7fad03bb4ed272130f15b956cbedb7b2f20b5b8a2dbaa0",
        input={
            "image": img,
            "resize_width": 400,
            "crop_n_layers": 0,
            "box_nms_thresh": 0.7,
            "crop_nms_thresh": 0.7,
            "points_per_side": 32,
            "pred_iou_thresh": 0.88,
            "crop_overlap_ratio": 0.3413333333333333,
            "min_mask_region_area": 30,
            "stability_score_offset": 1,
            "stability_score_thresh": 0.95,
            "crop_n_points_downscale_factor": 1
        }
    )
    print(output)
    response = requests.get(output)
    img = Image.open(BytesIO(response.content))
    img.show()

    driver.quit()
exploreAction("http://www.google.com", "Click Searchbar", (1920,1162), (878,483))