# Caching Server

The Caching Server is meant to alleviate some of the more memory and process expensive tasks, such as web scraping, on a server. As the name suggests, it wil cache the JSON response from a server for a set amount of time in a LevelDB database, and when it is "expired", it will be deleted.

# Goals
* Cache items from a server quickly
* Track how long each entry in the server has been stored for
* Delete an entry that is longer than a set *x* amount time
  * This means that data will be updated when it most likely has changed/is outdated

# Requirements
* Flask server for handling GET, PUT and DELETE requests and serving as the backbone of the project
* LevelDB for storing the JSON response from a server

# How to Use

This application has two parts: 
* The Flask server that handles requests to PUT and GET requests for the LevelDB 

[Set up the uWSGI server with `cache_manager.py` is you want to use this in a production environment.](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04)

* A seperate process handles the deletion of items after a set amount of time (default is 30 minutes)

The seperate process uses Systemd to enable it on startup and for more organization (status, start, stop, restart, etc.). Here is how you set it up:
* *Make sure you have Python 3 with `apscheduler` installed
* Edit the `run.sh` to have your directory in it
* *Make sure that the `run.sh` is executable by running `chmod +x run.sh`
* Create a file called a `.service` in `/lib/systemd/system` file and add put in it:
```
[Unit]
Description=Time updater for LevelDB Caching Server

[Service]
User=your-user-name
ExecStart=/path-to-directory/run.sh
WorkingDirectory=/path-to-directory

[Install]
WantedBy=multi-user.target
```
* Use `sudo systemctl start name-of-.service-file` to start the process
* Run `sudo systemctl status name-of-.service-file` to check everything is working fine
