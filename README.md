# Hugo Last.fm Recently Listened To Page Generator

A simple python script and workflow to pull the last 10 tracks scrobbled by your Last.fm account and update a .md page on your hugo website.

---

### Features:
 - Grab up to 50 of your recent tracks from your last.fm account
 - Schedule the workflow to run as often as you'd like (or as much as your github account will allow)
 - Easily change the css of how it's displayed on the page.

### What this version does not do by default:
 - Auto-push to your host (unless it does that automatically with every new build like cloudflare pages)
     - That though can be acomplished by adding another job to the workflow.
---

## Instructions:

 - Put the generate_markdown.py file at the base-level of your hugo site
 - Add your last.fm API key and username to your github secrets
    - Get your Last.FM API key here: - [https://www.last.fm/api/account/create](https://www.last.fm/api/account/create)
    - Give your application whatever name you'd like, you can use localhost as the callback url if you'd like, click submit and you'll see your API key, WRITE IT DOWN SOMEWHERE SAFE!

 - Create a new shortcode to enable rawhtml by adding a new file in layouts/shortcodes/rawhtml.html with the following content:
```
<!-- raw html -->
{{.Inner}}
```
          
```Use it like this -  {{< rawhtml >}} HTML GOES HERE {{< /rawhtml >}}```

 - Edit generate_markdown.py to change the limit (it's currently at 10 but you can go up to 50)
 - Make sure to put in your own frontplate information here:

```
# Generate Markdown content with Hugo front matter and embedded HTML for styling
markdown_content=f'''---
title: "Music"
date: "{current_datetime}"
#YOUR FRONTPLATE INFO GOES HERE
#I included how it changes the date to the current one every time it runs with {current_datetime}
#If you prefer to use the lastupdated option instead go for it
---
``` 

 - Edit the [git workflow](https://docs.github.com/en/actions/writing-workflows/about-workflows) file update_music_page.yml to change the directory/file the script creates as well as the update frequency. Currently it's set to every 4 hours but you can change the cron line to anything. Here's an easy tool to help with cron - [crontab.guru](https://crontab.guru/)
 - Place the update_music_page.yml in the following folder at the base of your site:  .github/workflows/update_music_page.yml
 - Add the code from the style.css file to your style sheet located in the assets/css/common/ folder, it might be different depending on your theme.
 - Now add/commit/push and it should automatically run the python script. You can see if there were any errors with the workflow by clicking on actions (it'll also email you).
 - Update: Changed it so that the workflow grabs the json file from last.fm's API. It saves a copy in your blog's root folder. Now every time it is triggered it will run a check to see if new music tracks have been added to the last.fm json file, if so it will rebuild the music.md page but regardless it will then go and see if there were any changes to the rest of the filesystem. That way you can still process updates even when there's been no changes to the recently listened to music list (before it would not update the rest of the site unless there was an update to the last.fm API feed).
 
A Full blog write-up can be found on my site at [brentter.com](https://brentter.com/blog/Add_An_Auto_Updating_Recently_Played_Music_Page_To_Hugo)
An example of this working in action can be found here [brentter.com/music](https://brentter.com/music)  
