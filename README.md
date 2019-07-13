# Price Assist Caching Server

The Price Assist Caching Server is meant to alleviate some of the more I/O bound and memory expensive tasks on the web scraping part of the server. As the name suggests, it wil cache the response from the server for a set amount of time, which will allow other users to use the same data.

# Goals
* Be able to set up an efficient way of storing item models associated with the retaialer information (a JSON)
* Track how long each entry in the server has been stored for
* Delete an entry that is longer than a set *x* amount time
  * This means that data will be updated when it most likely has changed/is outdated
* Free up system resources by alleviated stress on the webscraping server

# Requirements
* Flask server for handling GET, PUT, POST, and DELETE requests and serving as the backbone of the project
* JSON for storing the data
