# Database Performance Test
## Developers
 
* Casaburi, Nicolas
* Casco, Julio

## Institution

* Universidad Nacional de La Plata

### Description
This tool was developed with the purpose of testing the performance of Postgres and Mongo databases. While the tool supports custom models and databases, it provides two built-in databases (PostgreSQL and MongoDB) housed in Docker containers. There is already a default database model that simulates a hospital database with four tables and their relationships. The Database Performance Tester can generate a large amount of data to populate and stress the hospital tables. Additionally, this tool supports inserts, queries, deletes, index creation, and more. Measurements such as time, disk space, and memory consumption (the latter only available for MongoDB) are displayed in the logs generated for each tool execution. Finally, to enhance the user experience, an interactive menu has been developed, which can be viewed in the pictures below.

![Main Menu](/images/Main_menu.png "Main Menu")

### Steps to run the performance test:
> [!NOTE]
> This software requires Python version 3.10 or newer.
1. Clone the repository
```
git clone https://github.com/ncasaburi/Databases_Performance_Test.git
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
