**Basic**

Application provide simple API for fetching data from CSV file. 
Url can be configured in _storage.settings_ file.
Application has a long time to loading, cause it fetch data from CSV and 
checks some data in it.

CSV file must have a follow columns:

 - title
 - description
 - image


This implementation includes:

 - Checking `image` field has correct data(load it and checks 
 is it image or not)


**Basic usage**

Resources available through REST API.

Methods:

 - _/api/storage/_ returns list of rows imported from CSV 
 - _/api/storage/{index}/_ returns row by `index`
 
Limitations:

 - Not thread safety
 - Application have a long time of loading
 - Need to add tests