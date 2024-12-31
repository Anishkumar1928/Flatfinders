import requests

# Use the Client ID you provided
client_id = 'ab25efbe52ed0a9'

# Image file you want to upload
image_path = 'yoyo.jpeg'

# Open the image in binary mode
with open(image_path, 'rb') as image_file:
    image_data = image_file.read()

# Prepare the headers and data
headers = {
    'Authorization': f'Client-ID {client_id}'
}
data = {
    'image': image_data,
    'type': 'file'
}

# Upload the image to Imgur
response = requests.post('https://api.imgur.com/3/upload', headers=headers, files={'image': image_data}, timeout=10)

# Check if the upload was successful
if response.status_code == 200:
    print('Image uploaded successfully!')
    print('Image URL:', response.json()['data']['link'])
else:
    print('Failed to upload image:', response.json()['data']['error'])
