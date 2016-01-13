# Project: Tournament Database  - jennifer lyden

## Synopsis
Sets up a system (with a Python module and PSQL database) to run a tournament.

## Required Libraries and Dependencies
* You will need PostgreSQL, Python v2.*, and Python module psycopg2 to run this project.
* If you don't already have PSQL or python on your machine, you could run the system on a Vagrant Virtual Machine. Udacity's instructions for VM installation are here: https://www.udacity.com/wiki/ud197/install-vagrant

## Installation

### To Install
Download the zip file and extract the "tournament" folder inside.

### To Run
Start up your VM and navigate to the "tournament" folder you extracted.

### To Setup the Database:
Type `psql` to get into PostgreSQL.

#### In PostgreSQL:
* Type `create database tournament;`
* If you don't see the message "CREATE DATABASE", you probably left out the semicolon (;). Type it now and hit enter.
* Type `\c tournament`.
* You should see the message "You are now connected to database "tournament""
* Type `\i tournament.sql`. This imports the file into PSQL and sets up your tables and views.
* To verify that the empty tables exist, type `select * from users;` or `select * from matches;`. Don't forget semicolons!
* Type `\q` to exit PSQL.

### To Test Program
At command line (NOT in PSQL) type `python tournament_test.py`.

## Extra Credit Description
- In ec_tournament.py, I have modified the grouping function and swissPairings to prevent rematches. 
- I recognize this rematch-check-code is repetitive and limited - it works, but only if count(players) % 4 = 0. Once I refactored my original code (in response to previous submission feedback) to add a helper function and remove database calls from my Swiss Pairings loop, I wanted to attempt EC again. But now I'm moving on to the next project.
- You can see a test of ec_tournament.py by running `python ec_tournament_test.py`
- I realize I could improve basic code further by adapting helper functions to take additional parameters (so I could use it for "registerPlayer", for example), and to return values (so I could use it for "playerStandings"). But as I mentioned above, I'm eager to continue with next project. I'll try to incorporate helper functions as appropriate in future code.