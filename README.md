**Basic**

Application provides simple API for fetching data from CSV file. 
Url can be configured in `storage.settings` module.
Application loading faster as it checks corrections of image only by demand.

CSV file must have a follow columns:

 - title
 - description
 - image


This implementation includes:

 - Checking `image` field has correct data(load it and checks 
 is it image or not)
 
 **Configuration**
 
 Project wrote and has been tested on `Python 3.5+`.
 By default application runs on development configuration. 
 For adjusting configuration need to setup environment variable 
 `DJANGO_SETTINGS_MODULE` to any configurations provided in 
 `grams100.settings` module. 


**Basic usage**

Resources available through REST API.

Methods:

 - `/api/storage/` returns list of rows imported from CSV 
 - `/api/storage/{index}/` returns row by `index`
 
Limitations:

 - Not thread safety
 - Need to add tests