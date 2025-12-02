
## This is the health and fitness club management system. I've included here a basic overview, how to launch and test this program, and the link to the youtube video.
Student name: Rayan Hassan  Student ID: 101310730
Operations chosen:
    Member:
        User registeration
        Profile Management
        Health history
        Group class registeration 

    Trainer:
        Member lookup
        Schedule View

    Admin:
        Class managment
        Room booking

Prerequisites: 
    Python 3
    Postgres
    pip


Setup
    Because we're working with psychopg2, we'll need virtual environemnt (venv)
    In terminal, in project root enter: 
    python3 -m venv .venv
    source .venv/bin/activate

    Then run: pip install psychopg2-binary

Create and Populate db: createdb gym_management

    Then run the DDl: psql -d gym_management -f sql/DDL.sql
    Then run the DML: psql -d gym_management -f sql/DML.sql

To launch: 
    Type in terminal: python app/app.py

From here you will see a simple CLI with options. Choose option you want, and follow steps. You can test all opeartions from there. 

Youtube link Video: https://youtu.be/4YRx0NwwPxU