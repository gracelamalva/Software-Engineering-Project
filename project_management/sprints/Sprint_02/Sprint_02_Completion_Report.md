| Use Case | Description | Completion Status | Problems | Additional Tasks | What else did you do? | Team Member |
|---|---|---|---|---|---|---|
| Account | View Account Info (information you registered account with and displays the date you joined), update account info such as the username and email and have a password reset. | Completed | Could not create avatar, API was difficult to work with | Adding a confirmation email link and avatar/profile picture | Helped create and implement the register and login and helped with the creation of the affirmation use case | Sabrina |

 | Patient Sub User | User is given option to become a patient; create database, populate database, create routes, and web page. | Complete -User is able to convert to a patient account, revert back to a generic account, and gain access to patient features such as finding a therapist. Patient is also able to access all generic user features such as journal. All database tables, routes, and webpages are functional.| datetime.datetime has no attribute — not a syntax error, must be some other error | Had to integrate with Account to give new features depending on type of account | Integrated and final merged all the features together, delegated tasks to team members | Grace |

| User Logins|Users and patients can create an account and log into the website|CompletedAdd the feature of user register, login/out, reset info and remember me. The user's information is able to be stored into database using Flask forms and user can only access the other features when the user is authenticated.
A pop-up message will display when the user is successfully logged in/registered, an error message will be displayed if the username and password do not match. User's info and status will also show up and functional on the navigation bar. User is able to check their information and alter them after login. 
 |-The model.py, config.py, init.py need to be modified in order to make the app fully functional with the login.
-create app() statement in different .py files cause errors.(fixed)
|-Making the remember me functional on the database.|--- |Yin|

|-Search Method | Users can search their journal entries by entry date. | Completed
Users can search for journal entries by date. The search uses a query to retrieve all the entries for that specific date. |datetime.strptime has no attribute. Managed to fix it but error repeats on others machines even though the code is the same |Fixing datetime module error. |---| Karan |

|Daily Affirmations | User can set and view reminders for words of motivation. Daily affirmations are uplifting statements and quotes to prompt positive changes and attitude.|User can set and view reminders for words of motivation. The user inputs a positive message to oneself; all messages are displayed.|(sqlite3.OperationalError) no such table:” “. Changes were not being saved into the database. However, it is resolved now.|Create a delete button. |---|Dilpreet|