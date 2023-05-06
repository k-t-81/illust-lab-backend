main stack
-----
- runtime
  - python 3.10.9
- server
  - fast-api
  - unicorn
- graphql
  - strawberry-graphql
- database
  - mysql 8.0.32
  - sqlalchemy
  - aiomysql
  - migration
    - alembic
    - pymysql
- storage
  - aws-s3

start server
------------
`docker-compose up -d`  
`source venv/bin/activate`  
`python main.py`

migration
---------
`alembic upgrade head`

create migration file
----------------
`alembic revision --autogenerate"`  

export requirements.txt
-----------------------
`pip freeze > requirements.txt`

export graph schema
-------------------
`python export_schema.py`  
  
install python 3.10.9
---------------------
`pyenv install 3.10.9`  
`pyenv global 3.10.9`  
`python -m venv venv`  
`source venv/bin/activate`  

install packages
----------------
`source venv/bin/activate`  
`pip install -r requirements.txt`

s3
--
bucket name: `stable-diffusion-v2.1`  

more info
---------
- fast-api: https://fastapi.tiangolo.com/ja/  
- strawberry-graphql: https://strawberry.rocks/docs/integrations/fastapi  
- sqlalchemy: https://www.sqlalchemy.org/  
- alembic: https://alembic.sqlalchemy.org/en/latest/tutorial.html