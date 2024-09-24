import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import sys

# Fetch XML data from Last.fm API using environment variables for security
api_key = os.getenv('LASTFM_API_KEY')   #put your lastfm api key in your github secrets
user = os.getenv('LASTFM_USERNAME')   #put your lastfm username in your github secrets
limit = 10   #how many tracks should it grab, if left blank the default is 50
url = f'https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&limit={limit}&api_key={api_key}'

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    xml_data = response.content

    # Parse the XML data
    root = ET.fromstring(xml_data)

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from Last.fm API: {e}")
    sys.exit(1)  # Exit the script with a non-zero status to indicate failure

# Extract track information
tracks = []
for track in root.find('recenttracks').findall('track'):
    artist = track.find('artist').text if track.find('artist') is not None else ""
    name = track.find('name').text if track.find('name') is not None else ""
    album = track.find('album').text if track.find('album') is not None else ""
    url = track.find('url').text if track.find('url') is not None else ""
    image_url = track.find("image[@size='large']").text if track.find("image[@size='large']") is not None else ""
    date_listened_full = track.find('date').text if track.find('date') is not None else ""

    # Extract only the date part (first part before comma) and ignore time part
    date_listened_date_only = date_listened_full.split(',')[0] if date_listened_full else ""

    tracks.append({
        'artist': artist,
        'name': name,
        'album': album,
        'url': url,
        'image_url': image_url,
        'date_listened': date_listened_full
    })

# Get current date and time in ISO 8601 format with timezone offset
current_datetime = datetime.now().astimezone().isoformat()

# Generate Markdown content with Hugo front matter and embedded HTML for styling
markdown_content=f'''---
title: "Music"
date: "{current_datetime}"
#YOUR FRONTPLATE INFO GOES HERE
#I included how it changes the date to the current one every time it runs with {current_datetime}
#If you prefer to use the lastupdated option instead go for it
---

## Last Ten Tracks Listened To From Last.fm

{{{{< rawhtml >}}}}

<ul class="track-list">
'''

for t in tracks :
   markdown_content+= f'''
<li class="track-item">
<div class="track-image"><img src="{t['image_url']}" alt="{t['name']}"></div>
<div class="track-details">
<h3><a href="{t['url']}" target="_blank">{t['name']}</a></h3>
<p><strong>Artist:</strong> {t['artist']}<br>
<strong>Album:</strong> {t['album']}<br>
<strong>Date Listened To:</strong> {t['date_listened']}</p>
</div>
</li>'''

markdown_content += '''
</ul >
{{< /rawhtml >}}
'''

# Write to a markdown file- Change to whatever folder or filename you want the results placed in. 
with open("content/music.md", "w") as f:
     f.write(markdown_content)

