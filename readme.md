# IMointor
## Create  virtual environment  using below links and activate the env
https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/


### Go to working directory i.e your project folder
```sh
cd cloudautomation
```
### install  project dependencies
```sh 
pip install -r requirement.txt
```
###  apply the migrations:

```sh 
python manage.py migrate
```
###  Run the development server:
#### 0.0.0.0:8000 will your server on local network on port 8000 
```sh 
python manage.py runserver 0.0.0.0:8000
```
### If you want to create super user then run bellow command and input the requested fields:

```sh 
python manage.py createsuperuser

```