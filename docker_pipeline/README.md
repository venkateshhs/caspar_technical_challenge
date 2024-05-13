# ELT Pipeline using docker
This is an ELT pipeline build using Python, Git, Docker and Postgres DB. csv files present under 
data folder gets read and written to postgres database using python and docker. We can query the tables using pgadmin 
or though http://localhost:8080. 
    
    
Prerequisites
    1. Docker (https://www.docker.com/products/docker-desktop/) and git should be installed in host machine.

## Step1: 
    run the docker desktop.
    Clone repository : https://github.com/venkateshhs/caspar_technical_challenge.git
    Move to directory docker_pipeline using command: cd docker_pipeline in CLI.
    run command: docker-compose up --build as shown in figure in CLI.

## Step2:
    Database gets created and csv's are written into respective table as shown in figure.

## Step3:
    Open any browser and run : http://localhost:8080 as shown in figure.
    Input admin@admin.com and admin as username and password -> press Login

## Step4:
    pgadmin gets loaded.
    right click on Server -> Register -> Server
    Register server dialog gets opened.

## Step5:
    Go to Connection tab.
    Input :
            Host name / Address: postgres
            Port: 5432
            Maintainance databse : docker_hospital_databse
            Username: postgres
            Password: root
    Click save.

## Step6: 
    pgadmin gets opened.
    Click Server -> postgres -> Database -> docker_hospital_database
    Right click on docker_hospital_database and select Query Tool.
    Copy and Paste query from query.sql

## Step7:
    Run each query one by one (By selecting the entire query) using Windows+F5 key.
    Results gets displayed.

## Step8:
    Go to CLI where docker commands are running. Press CTRL+C.
    Run command: Docker-compose down.


    
    
