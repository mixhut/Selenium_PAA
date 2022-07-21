
## Selenium_PAA
``` v1.3
- Combines Selenium(-wire) engine with the people_also_ask project based on bs4.
- Based on the Firefox Webdriver
- Removes requests modules and replaced with selenium
- Housekeeping: some functions into their own folder
- Test of selenium-wire to block image requests

```
### To-Do:
- Make clearer functions and better naming system
- Create function for taking SERP KWs > PAAs, and function for PAAs > Pickle/JSON
- Convert bash cleaning scripts to python and add to tools.py
- Look into RAM handling/cleaning for performance (meantime pause/restart every 200 PAAs)
- Future: Use Click or similar module to allow running from the CLI 
- 


### REQUIREMENTS:
- requirements.txt
- Geckodriver =>0.31.0 https://github.com/mozilla/geckodriver/releases 
- Fill in local variables in constants.py file
- Filenames/structure work in progress - name files in input/output as per script