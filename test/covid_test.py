import pytest # for pytest.raises (see: https://docs.pytest.org/en/latest/assert.html)

from app.covid import get_data, string_validation, data_validation, average_deaths, average_cases, deaths_change, cases_change

CI_ENV = os.environ.get("CI") == "true" # expect default environment variable setting of "CI=true" on Travis CI, see: https://docs.travis-ci.com/user/environment-variables/#default-environment-variables

@pytest.mark.skipif(CI_ENV==True, reason="to avoid configuring credentials on, and issuing requests from, the CI server")

def test_get_data():
    # test to ensure data is getting written to local CSV sheet and file_name is a string
    
    assert get_data() == "nytdata.csv"

    with open(get_data(), 'r') as file:
        csv_file_reader = csv.DictReader(file)
        assert isinstance(csv_file_reader, dict)

def test_string_validation():
    # test to ensure state and county inputs are strings, not integers
    state_input 

def test_data_validation():

def test_average_deaths():

def test_average_cases():

def test_deaths_change():

def test_cases_change():

def test_to_usd():
    # it should apply USD formatting
    assert to_usd(4.50) == "$4.50"