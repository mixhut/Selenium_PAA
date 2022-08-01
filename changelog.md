---
# Selenium PAA
---
## Selenium Firefox Webdriver & PAA Script
---

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
