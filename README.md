# COVID
This application tracks COVID-19 statistics by US County over time and makes recommendations about potentially reopening the economy.

## Instructions for the Project:
https://github.com/prof-rossetti/intro-to-python/tree/master/projects/freestyle

## Install on Local Device
Fork it, clone it, navigate from the command line

Example
```sh
cd ~/Documents/GitHub/COVID19
```

## Setup
Create an anaconda virtual environment
Example
```sh
conda activate covid-env
```
 
Install necessary packages
```sh
pip install -r requirements.txt
```

## Usage
Run the python script

Example
```sh
python app/covid.py
python -m app.covid
```
Run it using Heroku
```sh
heroku login
```

## Testing
Install the pytest package within a virtual environment using pip
```sh
pip install pytest
```

Run the package using this command
```sh
pytest
```