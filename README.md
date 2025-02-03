# CS348-Project

Repository for a CS 348 Introduction to Database Systems group project.

## Installation

To start, you will need Python 3.X installed.

### MacOS

```txt
git clone https://github.com/DarkHawk727/CS348-Project.git
python -m virtualenv venv
source .\venv\bin\activate
pip install -r requirements.txt
```

### Windows

```txt
git clone https://github.com/DarkHawk727/CS348-Project.git
python -m virtualenv venv
.\venv\bin\activate.ps1
pip install -r requirements.txt
```

## Verification (Hello World Application)

To verify that you have correctly installed everything correctly, please run `test.py`. This will create the table schema, fill the data, and then verify that there are 1000 rows

## Sources

- https://github.com/ofenloch/mysql-sakila/blob/master/sakila-data.sql
- https://dev.mysql.com/doc/sakila/en/sakila-preface.html
