# Flask-Tickets

A classic ticket tracking application featuring basic authentication with user accounts and role-based authorization with three privilege classes made with:  
- Python, Flask  
- HTML, CSS, JavaScript, AJAX, Bootstrap 4  
- Oracle Database 21c XE.    
<br>
<br>  

![image](https://user-images.githubusercontent.com/21013517/189447797-618a39f7-3f6d-4203-b8ec-8f306499858f.png)  
![image](https://user-images.githubusercontent.com/21013517/189447837-52b13b2b-c11f-4a39-95de-f6b19b13c741.png)  
![image](https://user-images.githubusercontent.com/21013517/189447889-1fdb68ad-285a-410e-8129-c962430b95cb.png)



### To run

You will need an Oracle Database compatible with 21c XE accessible via user/pass/dsn.

- Clone the repo to your computer  
- Create and activate a virtual environment for the project  
- Use PIP to install requirements from the requirements.txt  
- Set environment variables  
    - FLASK_APP=application  
    - FLASK_ENV=development  
    - DATABASE_USER= your database user
    - DATABASE_PASSWORD= your db password  
    - DATABASE_DSN= your db dsn like 'localhost:1521/xepdb1'  
- Ensure you are connecting to a empty schema for this application to avoid object identifier conflicts   
- Execute `flask init-db` to initialize the database  
- Execute `flask load-sample-data` to load the sample data  
- Execute `flask run`  
