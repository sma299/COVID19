# COVID19
This application tracks COVID-19 data by US county over time and emails the user a summary of the statistics.

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
Run the python script locally

Example
```sh
python -m app.covid
```
Run it using Heroku - first, you must login using your own account
```sh
heroku login
```

Set up the server on Heroku
```sh
heroku create covid-tracker-your-name
```

Configure your environment variable using Heroku interface OR from the command line
```sh
heroku config
heroku config:set APP_ENV="production"
heroku config:set SENDGRID_API_KEY="insertAPIkey"
heroku config:set MY_EMAIL_ADDRESS="insert@email.com"
heroku config:set MY_NAME="Mr.Krabs"
heroku config:set STATE="California"
heroku config:set COUNTY="Orange"
heroku config:set PLOTLY_USER_NAME = "plotly"
heroku config:set PLOTLY_API_KEY = "insertAPIkey"
```

To make sure everything is up-to-date on the Heroku server
```sh
git push heroku master
```

Finally, run the app on the Heroku server
```sh
heroku run bash
python -m app.covid
```

## Testing

Run the package using this command
```sh
pytest
```