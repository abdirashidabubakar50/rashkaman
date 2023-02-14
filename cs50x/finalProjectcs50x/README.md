# TODO'S
#### Video Demo:  https://youtu.be/dzs2ZEzgrRY
#### Description:

This is my project, which is a tool for doing something useful. I created this project because I saw a need for a tool like this in my work or personal life, and I wanted to fill that need.

In this project, I have included the following files:

- app.py: This is the main script for the project. It contains the main functions and routes which are /signup, /index, /login, logout/, /addtask, /tasks.

- project.db This file contains the database for my application .

- static/: This directory contains styles.css file for my css codes for the application and also an image file which I used for logo.

- templates/: This directory contains html files the main script. In the templates directory there are the following files:
- 1. layout.html: THis file contains the overall layout html for the web application
- 2. signup.html: This file contains the html file for signup function. It posts a form where the user can signup
- 3. login.html: This file contains the html for login function.
- 4. index.html: This is the  html file for homepage
- 5. tasks.html: This file contains the html file for the tasks page which allows the user to add, update and delete tasks

#### /signup:
This is a route which uses both "GET" and "POST" methods.It confirms that the user has typed in all the inputs(username, email, password, confirmation).If the username typed in is already in the database it prompts an error("username has already been used"), also it checks the valididty of the email and if it is invalid it again prompts an error saying the email provided is invalid.The function also checks if the password enterd is atleast 8 characters, has an uppercase letter ,a lower case letter ,a special character and one number.if either of the above is missing it will prompt an error.It also confirms the password and checks if it matches with the one entered in the confirmation input,and if it does not match it will prompt an error respectively.The function goes on checking if the email entered has already been signed up with  before and if so it will prompt an error.
If the user succeeds and surpasses all the above the and clicks the signup button, the user's data will be inserted into the database and an email will be sent to the user saying ("You've successfully signed up for your account feel free to plan for your day"), then it redirects the user to a login page where the user is able to login.


#### /login:
In this route the function checks that if the username password and email entered correspond with the ones in the database it redirects the user to another page called tasks where the user is able to add tasks, update and also delete

#### /logout:
This route allows users who are already logged in to be able to logout

#### /tasks:
This route retrieves all tasks from the database and renders the tasks template, passing the tasks as a parameter


#### /addtask:
Here the function gets the task from the form submission and adds the task and current date to the database and redirects the user to the tasks page

#### /delete:
In this route the function allows the user to delete the tasks. When the user clicks on the delete button in tasks.html it deletes the respective task from the database

#### /update:
When the user clicks on update button in tasks page, the function updates the respective task to completed.


I debated several design choices while working on this project, and ultimately decided to go with the approach that I did because it seemed the most efficient and effective. For example, I considered using SQLAlchemy for storing the data, but ultimately decided to use sqlite3 imported from cs50 library because it was easier to work with.

I hope you find this project useful, and I welcome any feedback or suggestions for improvement.
