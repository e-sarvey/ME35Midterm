### ELIJAH'S PROGRAM TO UPDATE AIRTABLE WITH COLOR DETECTED ##
# OpenCV program
cv2_image = cv2.cvtColor(np.array(cam.raw_image), cv2.COLOR_RGB2BGR) # take picture and return bgr array format
b,g,r = cv2.split(cv2_image) # get color channels as individual arrays
grey = cv2.cvtColor(cv2_image, cv2.COLOR_BGRA2GRAY) # greyscale of original image

# define a red mask that takes upper and lower threshold values for bgr to define what is "RED"
lower_Red = np.array([0, 0, 80]) # b,g,r
upper_Red = np.array([100, 100, 255])
mask_Red = cv2.inRange(cv2_image, lower_Red, upper_Red)
red = cv2.bitwise_and(cv2_image, cv2_image, mask = mask_Red) # apply mask to image to isolate red
#display(Image.fromarray(mask_Red))
#display(Image.fromarray(cv2.cvtColor(red, cv2.COLOR_BGR2RGB)))

# define a green mask that takes upper and lower threshold values for bgr to define what is "GREEN" as was done with red
lower_Green = np.array([100, 0, 0]) # b,g,r
upper_Green = np.array([175, 255, 100])
mask_Green = cv2.inRange(cv2_image, lower_Green, upper_Green)
Green = cv2.bitwise_and(cv2_image, cv2_image, mask = mask_Green)
#display(Image.fromarray(mask_Green))
#display(Image.fromarray(cv2.cvtColor(Green, cv2.COLOR_BGR2RGB)))

# same as previous but for blue!
lower_Blue = np.array([200, 0, 0]) # b,g,r
upper_Blue = np.array([255, 100, 100])
mask_Blue = cv2.inRange(cv2_image, lower_Blue, upper_Blue)
Blue = cv2.bitwise_and(cv2_image, cv2_image, mask = mask_Blue)
#display(Image.fromarray(mask_Blue))
#display(Image.fromarray(cv2.cvtColor(Blue, cv2.COLOR_BGR2RGB)))

# make a new mask that contains the blue, red, and green masks so we can compare which mask has the most of each color in the threshold range
new_mask = mask_Blue + mask_Red + mask_Green
res = cv2.bitwise_and(cv2_image, cv2_image, mask = new_mask)
display(Image.fromarray(cv2.cvtColor(res, cv2.COLOR_BGR2RGB)))
b,g,r = cv2.split(res) # split by color channels
colors = {"Red":np.sum(r),"Green":np.sum(g),"Blue":np.sum(b)} # sum the color channels
big_color = max(colors, key=lambda color: colors[color]) # identify the color channel with the largest sum which would mean it is the most prominent in the mask added image
print(big_color) # print the result color

# TESTED: THIS CODE SECTION SHARES VARIABLES WITH PREVIOUS BLOCK #
import requests
from mysecrets import ATsecrets

# Initialize Airtable Rest API access
api_key = ATsecrets['token']
base_id = 'appCUx68GT006rHir'
table_name = 'Color Detection History'
url = f'https://api.airtable.com/v0/{base_id}/{table_name}/recDBFD7dJnbrfVHM'

# Function that returns the current color posted to the Airtable "Color Detection History"
def GetCurrentColor():
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        current_color = data.get('fields', {}).get('Color')
        print(current_color)
        return current_color
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        
# Function that updates the value for "Color" field in the first record of the Airtable "Color Detection History"
def UpdateColor(new_color):
    if new_color not in ['Blue', 'Green', 'Red']:
        print('Input Argument Value not in List of Allowed Values')
        return
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    color_post = {'fields': {'Color': new_color}}
    response = requests.patch(url, json=color_post, headers=headers)
    if response.status_code == 200:
        print(f'Updated Color with {new_color}')
    else:
        print(f"Failed to update color. Status code: {response.status_code}")

# main function: checks current cell value and updates it if the new color read is different.
def main(big_color):
    current_color = GetCurrentColor()
    if current_color == big_color:
        print('New Value Matches Current Value')
        return
    elif current_color != big_color:
        UpdateColor(big_color)
    else:
        print('something weird happened...')


# run main
try:
    main(big_color)
except Exception as e:
    print(f'Error: {e}')
finally:
    print('The End!')



#import Serial

#Serial.SerialConsole("console")
