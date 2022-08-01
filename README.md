---
# Selenium PAA
---
## Selenium Firefox Webdriver & PAA Script

### Description:
- Combines Selenium engine with the people_also_ask project based on bs4.
- Built with Firefox Webdriver
- Removed requests modules / replaced with Selenium

## Changelog (v1.7):
- Added function to remove duplicate keys from JSON file
- Fixed append_json function - now outputs valid JSON
- Minor updates to constants.py

## Changelog (v1.6):
- Added the PAA level depth back into the GSearch.search function
- Added pickle_it function to tools + added pickle2json conversion
- Added clearing data on every loop for testing (stability/performance)
- Added project_root etc to constants.py
- Added functions for checkpoint to tools.py
- Removed checkpoint folder, changed to .save file in output dir

## Changelog (v1.5):
- Added some functions into a class 'GSearch' (needs refined)
- Fixed RAM issues with webdriver not exiting properly (__init__, __del__)
- Removed selenium-wire integration (throwing HTTPS errors with new FF profile)
- Removed interceptor (selenium-wire)
- Adjusted default PAA scrape level to 7
- Tweak directory structure


### To-Do:
- [x] Add pickle to JSON converter to end of script
- [x] Look into RAM handling/cleaning for performance
- [x] Create function that outputs a valid JSON file
- [ ] Remove pickling and output direct to JSON
- [ ] Make clearer functions and better naming system
- [ ] Consolidate testing scripts into functions + streamline 
- [ ] Change bloated constants naming system for files | e.g. > line.split/join()
- [ ] Create function for taking SERP KWs > PAAs, and function for PAAs > Pickle/JSON
- [ ] Convert bash cleaning scripts to python and add to tools.py
- [ ] Future: Use Click or similar module to allow running from the CLI
- [ ] Add command line arguments - e.g. for project_name, etc
- [ ] Add naming stages to json files for processing
- [ ] Remove debug comments



### Requirements:
- requirements.txt
- Geckodriver =>0.31.0 https://github.com/mozilla/geckodriver/releases 
- Fill in local variables in constants.py file
- Filenames/structure work in progress - name files in input/output as per script
