import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import sys
import json

# Load track data from JSON file instead of fetching it directly from API.
try:
    with open("lastfm_tracks.json", "r") as f:
         response = json.load(f)

except FileNotFoundError as e:
    print(f"Error loading track data file {e}")
    sys.exit(1)  # Exit the script with a non-zero status to indicate failure.

# Extract track information from loaded JSON data.
tracks = []
for track in response['recenttracks']['track']:
    artist = track['artist']['#text'] if 'artist' in track else ""
    name = track['name'] if 'name' in track else ""
    album = track['album']['#text'] if 'album' in track else ""
    url = track['url'] if 'url' in track else ""

    # Correctly extract large image URL
    image_url = next((img['#text'] for img in track.get('image', []) if img.get('size') == 'large'), "")

    date_listened_full = track['date']['#text'] if 'date' in track else ""

    date_listened_date_only = date_listened_full.split(',')[0] if date_listened_full else ""

    tracks.append({
         'artist': artist,
         'name': name,
         'album': album,
         'url': url,
         'image_url': image_url,
         'date_listened': date_listened_date_only,
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

