# Interactive Pokedex
This is a small WIP project to gain some familiarity with Flask. At the moment, it is a web app that allows the user to obtain information about Pokemon from a database locally hosted with Microsoft SQL Server Express. Below is a clip of the web app.

https://github.com/user-attachments/assets/9eaf8850-0a6c-42aa-bd94-88c974ef9c13

Pokemon.csv is the dataset used, bulk inserted into the database. In the assets folder, there is a CSS file that makes the dropdown menus match the page's dark mode. The main file runs the app and passes the user input to connect_to_database, which passes the user parameters to the SQL server as a query.
