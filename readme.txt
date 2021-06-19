Hi, the german app is a desktop app with the objective of practicing german vocabulary.

It has an executable, which sadly only runs if you have PostgreSQL installed.

Also a brief explanation of the components:
    -german.py: Is the main file in wich we have the Kivy code and the german vocabulary.
    -german.kv: It has many of the kivy instruction write in Kivy Language.
    -database.py: It has the PostgreSQL instruction to create database, create tables, extract information,etc. 
                All this done from the german.py script.

Features of the APP:
    -Create Account User
    -Login User
    -Select the lesson to study german
    -Lessons from german, in which it is possible to evaluate if the results are good, or to show the correct answers.
    -It has a configuration screen where an user can see their information regarding the results of their lessons and the option to log out.