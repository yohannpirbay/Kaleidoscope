# Team *Kaleidoscope* Major Group project

## Team members
The members of the team are:
- *Hamnah Rassen*
- *Kai Jones*
- *Muhammad (Ahsan) Mahfuz*
- *Neel Suroop Nair*
- *Rayan Popat*
- *Svilen Dilchev*
- *Yohann Pirbay*
- *Zoya Nasir*

## Project structure
The project is called `Kaleidoscope`. It currently consists of a single app `journal`.


## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```



## Sources
The packages used by this application are specified in `requirements.txt`

## Additional info
We used the scaffolding from the small group project in this major group project (we were authorised to use it by the lecturer).

We have made use of generative AI to enhance our development process and assist us on small code snippets.

The web app is seeded with a significant amount of sample data to allow you to explore fully all the features.

To gain access to the administrative features use these credentials (username: @johndoe password: Password123). All the other users have the same password as well (Password123).

