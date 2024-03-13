# Database Performance Test
## Developers
 
* Casaburi, Nicolas
* Casco, Julio

## Institution

* Universidad Nacional de La Plata

### Steps to run this performance test:
1. Cloning this repo
```
git clone https://github.com/ncasaburi/Databases_Performance_Test.git
```
2. Move into the repo
```
cd Databases_Performance_Test/
```
3. Start Mongo and PostgreSQL containers
```
docker-compose up
```
4. Create environment and install the requirements
```
python3 -m venv .venv; . .venv/bin/activate; pip install -r requirements.txt
```
5. Generate new SQL files (optional)
```
python3 Queries/PostgreSQL/SQLGenerator.py 
```
6. Run performance test
```
python3 __main__.py
```