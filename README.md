#Web API Project
A  Udacity project to develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

# Getting Started
You can access the files of this project from [ this Github link](https://github.com/rawatankit90/item_catalog)

## Prerequistes
In order to view these files you must have a

1) A Web broswer(like IE or Chrome) installed on your computer.
2) A working internet connection.
3) A Virtual Machine and Vagrant setup to run
4) Python 2.7 with SQLAlchemy and flask framework setup

## With the above steps done
1) You can access the files from [ this Github link ] (https://github.com/rawatankit90/item_catalog) by clicking the green download button on the right.
2) Unzip the downloaded file.
3) Place the above files in Vagrant directory
4) From Vagrant, SSH to VM [Virtual Machine]  and navigate to the folder "item_catalog" under vagrant folder
5) Create the database ''''  shoplocal.db ''' using following command ''' python model.py '''
6) Populate the database using following command ''' python populate_db.py '''
5) Run the project.py file using command python project.py
6) Go to your favorite browser and type http://localhost:5000
7) You will be directed to home page where user can login or Register himself or User can browse the categories without login
8) User has option to login with Google

## Built With love from udacity learner
1) HTML5
2) CSS3
3) Bootstrap 3
4) Python 2.7
5) SQLAlchemy
6) flask templates
