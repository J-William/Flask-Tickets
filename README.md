# Flask-Tickets

A ticket tracking system made with Flask, Bootstrap 4, and Oracle Database 21c XE.


### To run

Clone the repo to your computer
Create and activate a virtual environment for the project
Use PIP to install requirements from the requirements.txt
Set environment variables
    - FLASK_APP=application
    - FLASK_ENV=development
    - DATABASE_USER=<your db user>
    - DATABASE_PASSWORD=<your db password>
    - DATABASE_DSN=<your db dsn like 'localhost:1521/xepdb1'>
Ensure you are connecting to a empty schema for this application
Execute `flask init-db` to initialize the database
Execute `flask load-sample-data` to load the sample data
Execute `flask run`