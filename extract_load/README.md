# Simple ELT pipeline
This pipeline is built using Python, Git, SQl and pgadmin.

Prerequisites:
Git, Python and pgadmin should be installed.
Also, install all the packages in requirements.txt

## Create environmental Variables:
    After cloning the repo: https://github.com/venkateshhs/caspar_technical_challenge.git
    Go to folder -> extract_load using cd extract_load in CLI
    create folder "env" and then a file called ".env"
    Paste the following in .env file after putting correct credentials:
        DB_HOST=localhost
        DB_NAME=*input your db name*
        DB_USER=*input your user name*
        DB_PASSWORD=*input your password*
        DB_PORT=5432

## Pipeline explanation:
    1. Given csv files are present under the folder data.
    2. env folder containes a file called .env which contains database credentials. This is not commited to git owing to security reasons.
    3. common_methods.py contains common methods such as test_connection, setup_logging and get_credentials.    
    4. logs folder contains logs of each run as a textfile referenced using timestamp of each run.
    5. To insert data into database, run read_csv_write_to_db.py using the command: python read_csv_write_to_db.py in CLI.
    6. Data is inserted into db. 
    7. Open pgadmin, create server and check output.   
    
