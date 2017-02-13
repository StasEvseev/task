The Setting

You need to develop a RESTful API to return a simple data set. The data consists of:

	•	Image;
	•	Title;
	•	Description (optional).

The data set is hosted on Google Docs: https://docs.google.com/spreadsheets/d/1SYNFV6IGYOme9smQKVBFBPnOQvJa3MUi9QKGo2rFa94/pubhtml

The spreadsheet is accessible as a CSV file through the following link: https://docs.google.com/spreadsheets/d/1SYNFV6IGYOme9smQKVBFBPnOQvJa3MUi9QKGo2rFa94/pub?gid=0&single=true&output=csv

The datasheet consists of user collaborated data with very little validation checks. You should make no assumptions about the correctness of the data. For example, the size of the images is not guaranteed to be optimised for use in a mobile application.

The Task

Because the CSV is an external resource with no guarantees of direct availability, an API should be implemented in between. Build a RESTful JSON API in Python/Django that will load the contents of the CSV and provide a JSON API for web app and mobile app clients.

Things you have to take into consideration:

	•	Cold-boot times;
	•	Performance;
	•	Image cache;
	•	Exception handling;
	•	Supporting multiple working environments(development/staging/production).

Optional Components:

	•	Response cache;
	•	Scalability, when the application should be served from multiple servers.

Remarks

You can build everything yourself or use existing library components.
Try to make error handling as graceful as possible. The user should not be bugged with error messages.