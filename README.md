# Database Performance Tester
## Developers
 
* Casaburi, Nicolas
* Casco, Julio

## Institution

* Universidad Nacional de La Plata

## Description

This tool was developed with the purpose of testing the performance of Postgres and Mongo databases. While the tool supports custom models and databases, it provides two built-in databases (PostgreSQL and MongoDB) housed in Docker containers. There is already a default database model that simulates a hospital database with four tables and their relationships. The Database Performance Tester can generate a large amount of data to populate and stress the hospital tables. Additionally, this tool supports inserts, queries, deletes, index creation, and more. Measurements such as time, disk space, and memory consumption (the latter only available for MongoDB) are displayed in the logs generated on each tool execution. Finally, to enhance the user experience, an interactive menu has been developed, which can be viewed in the picture below.

![Main Menu](/images/Main_menu.png "Main Menu")

## Steps to run the tool:
> [!NOTE]
> This software requires Python version 3.10 or newer.
1. Clone the repository
```
git clone https://github.com/ncasaburi/Database_Performance_Tester.git
```
2. Move into the repository
```
cd Databases_Performance_Test/
```
3. Start Mongo and PostgreSQL containers
```
docker-compose up -d
```
4. Create environment and install the requirements
```
python3 -m venv .venv; . .venv/bin/activate; pip install -r requirements.txt
```
5. Run performance tests
```
python3 __main__.py
```
## Dataset generation:
Database Performance Tester comes with a dataset of 500000 registers (250000 rows for PostgreSQL and 250000 documents for MongoDB). However, the tool also includes a feature called Data Generator under the Miscellaneous option (from the main menu), which can generate millons and millons of data to populate the default hospital database. The dataset can be divided into different zipped files in order to decrease their size.

Example of generating 25.000.000 registers for both PostgreSQL and MongoDB

![DataGenerator](/images/DataGenerator_1.png "DataGenerator")

![DataGenerator](/images/DataGenerator_2.png "DataGenerator")