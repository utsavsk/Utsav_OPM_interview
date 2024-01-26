# Stock Charts - Readme File
There are two sets of related files in the project. 
* 1. 'importnasdaq.py' file along with all the text files in 'NASDAQData' folder
* 2. 'main.py' file and associated files and folders that are part of the flask app that will crate a very simple yet powerful dashboard that can quickly data table with thousands of rows and produce stock market chart and calculate prediction when clicked. 


_Opensource Technologies used:_
Besides python libraries, I am using the following freely usable libraries:
* Bootstrap
* simple-datatables
* fontawesome
* jquery
* ajax
* chart.js



### Step 0. Create and run a virtual environment

Copy and paste the following codes to create a new vitual environment and run it. If a virtual environment is already present simply activate it. I also suggest updating pip just incase. 

```sh
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
```

### Step 1. Install dependencies

Since this code has multiple dependencies, I have included a *requirements.txt* file. Please the following script to install all the required dependencies at once.
```sh
pip install -r requirements.txt
```


### Step 2. Run 'importnasdaq.py' 

This file loads all the data from NASDAQData folder, runs a simple linear regression to predict a day ahead stock closing price, and saves the output in Predict_NASDAQ.csv flat file. 
There are over 4000 stock symbols so this will take a couple of minutes to run. 

```sh
python importnasdaq.py
```

### Step 3. Run 'main.py' 

Main.py is a flask app that will initialize __init__.py which will inturn initialize views.py. Since this is a flask app, it will run a sever on the local machine. 

```sh
python main.py

# copy and paste the following to view website
http://127.0.0.1:5000/
```


Copyright (c)  Utsav Kattel
