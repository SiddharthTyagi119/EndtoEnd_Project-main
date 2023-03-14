Step 1- Upload row column data to mongo db database.
Step 2- Create a template by script file i.e. template.py.
Step 3- Create Setup.py-
In python, setup.py is a module used to build and  distribute python packages it typically contains information about the package,such as it name,
version and dependencies, as well as instruction for building and installing the package.We can build and distribute python package so that other
can use it. It is responsible in creating ml application as a package.Build app as a package to import/use it.
Step 4- Create logger file-
logger file is used so that we can esily find out error in our project. it store the errors.
Step 5- Create exception file-
In this we are creating function to get the error message and details
Step 6- Mention Logger and exception function in main.py file to test logger and exception.
Step 7- Create utils.py file.
Inside this we will create a df to read data in local from db.
Step 8- .env- creating a fn. just to load the mongo db environment
Step 9- Insde __init__, we are defining a dotenv package which help us to load any env. in local. 
Step 10- Create a config file- create a class to define mongo url and client.
Step 11- Inside main.py , just passing/calling the function, which is present in utils file to extract the data.
Step 12- create artifact folder and two files->artifact.py and config.py
Artifact generates an output and save it inside the artifact folder
config- creating the function to perform valiation(just creating dir and files to store) and other things
artifact- defining config file functions
Step 13- Data Ingestion
reading the data from db and from main csv file it is splitting the data- and storing them all under artifact
Step 14- Data validation
check dtype , find and remove unwanted data  and data cleaning. and also check our main data is equal to our
split data or not. 
Step 15- Data transformation
missing value impute,outliers,imbalanced data
Step 16- Model trainer-
