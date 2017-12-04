import sys
import time
import json
import requests

seen_photos = {}

def recursive_download(url, count=0):

    if url in seen_photos:
        return
    seen_photos[url] = True

    page = requests.get(url)
    photo_json = page.json()

    print(photo_json)
    yield photo_json

    next_url = 'https://earthview.withgoogle.com' + photo_json['nextApi']
    id_url = photo_json['id'] + '.jpg'
    download_url = photo_json['photoUrl']

    with open(id_url, 'wb') as handle:
        response = requests.get(download_url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

    timing(60)

    for photo_json in recursive_download(next_url, count + 1):
        yield photo_json

def timing(secs):

    time.sleep(secs)

if __name__ == "__main__":


    # Extract image json from web souce
    r = requests.get('https://earthview.withgoogle.com')
    s1 = r.text
    s2 = s1.replace(s1[:s1.find('/_api')],'')
    s3 = s2.replace(s2[:s2.find('.json')],'')
    photo_latest_earth = 'https://earthview.withgoogle.com' + s2.replace(s3,'') + '.json'

    photos_json = json.dumps(list(recursive_download(photo_latest_earth)))
