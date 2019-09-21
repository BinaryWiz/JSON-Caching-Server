# Caching Server

The Caching Server is meant to alleviate some of the more memory and process expensive tasks, such as web scraping, on a server. As the name suggests, it wil cache the response from a server for a set amount of time in a JSON format, and when it is "expired", it will be deleted. The user can also edit what is in the server via the RESTful-like API.

# Goals
* Track how long each entry in the server has been stored for
* Delete an entry that is longer than a set *x* amount time
  * This means that data will be updated when it most likely has changed/is outdated
* Free up system resources by alleviated stress on the webscraping server

# Requirements
* Flask server for handling GET, PUT and DELETE requests and serving as the backbone of the project
* LevelDB for storing the keys and values

# Updates
* Added uWSGI support and set up the files to be easily used with an NGINX or Apache server
