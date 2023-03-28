# World Construct

### Welcome

Welcome to the new and improved version of World Construct (previously JDKWorldBuilder). This sytem has been upgraded in numerous ways from the initial design. The key changes are:

1. Shift from encoded .csv file to using a PostgreSQL database for information, making information accessing and changing much easier
2. Establishment of API calls allowing for the information to be accessed by other applications. This allows us to shift away  from each client needing the files and allows for easier updates and changes to data
3. Devlopment of a frontend website. No longer need the client installed on the user's system, which was previously done using JavaFX (work in progress)

### Setup

In order for the system to be able to access and modify the database, first you will need to do a few initial setups.

1. In the config folder, create a db.yml file. Within this file, paste the following lines (setup to reflect the database name and login of your system):

```
host: localhost
database: *Your database name here*
user: *Your username here*
password: *Your password here*
port: 5432
```
2. Run the following command in the command line client:
   `pip install -r requirements.txt`
3. For the initial setup of the database tables, run the test `test_reset_tables`. This will run the function `rebuild_tables()` which is designed to dump the tables if they exist and reinsert them with the proper fields. Do not run this after values are put into it live as it will delete all of the information in the database

### Future Plans
The future plans for this system is to, firstly, finish the design of the frontend website, as well as getting the likes and dislikes system online. After completion, the api calls will be integrated into Sullybot, allowing for the information to be accessed from any Discord server. Following this, I hope to make consistent updates, adding new features, like more component types., as well as possible AI integration, like Midjourney image generation and ChatGTP description generation