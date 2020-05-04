import pytest # for pytest.raises (see: https://docs.pytest.org/en/latest/assert.html)

from app.covid import get_data, string_validation, data_validation, average_deaths, average_cases, deaths_change, cases_change

#CI_ENV = os.environ.get("CI") == "true" 
#@pytest.mark.skipif(CI_ENV==True, reason="to avoid configuring credentials on, and issuing requests from, the CI server")

def test_get_data():
    # test to ensure data is getting written to local CSV sheet and file_name is a string

    # INVOCATION
    assert get_data() == "nytdata.csv"

    with open(get_data(), 'r') as file:
        csv_file_reader = csv.DictReader(file)
        # INVOCATION
        assert isinstance(csv_file_reader, dict)

def test_string_validation():
    # test to ensure state and county inputs are strings, not integers

    state_int = 82882
    county_int = 3939 

    # INVOCATION
    assert string_validation(state_int, county_int) == True

    state = "California"
    county = "Orange"

    # INVOCATION
    assert string_validation(state, county) == False

def test_data_validation():
    # test to ensure state and county combination exists

    states_array = ["California", "New Jersey", "Delaware", "Ohio"]
    counties_array = ["Los Angeles", "Mercer", "Sussex", "Cuyahoga"]

    state1 = "California"
    county1 = "Mercer"
    county2 = "Los Angeles"

    # INVOCATION
    assert data_validation(state1, county1, states_array, counties_array) == False
    assert data_validation(state1, county2, states_array, counties_array) == True

def test_average_deaths():
    # test to ensure deaths are averaged over two weeks

    deaths_array = [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0]
    # INVOCATION
    assert average_deaths(deaths_array) != 4.928
    assert average_deaths(deaths_array) == 5.0

def test_average_cases():
    # test to ensure cases are averaged over two weeks

    cases_array = [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0]
    # INVOCATION
    assert average_cases(cases_array) != 4.928
    assert average_deaths(cases_array) == 5.0

def test_deaths_change():
    # test to ensure percent of deaths increases or decreases by the proper percentage

    result = " "
    average_deaths = 40
    new_deaths = "10"

    # INVOCATION
    result = deaths_change(average_deaths, new_deaths)
    self.assertIn("75.00", result)

def test_cases_change():
    # test to ensure percent of deaths increases or decreases by the proper percentage
    
    result = " "
    average_cases = 40
    new_cases = "10"

    # INVOCATION
    result = cases_change(average_cases, new_cases)
    self.assertIn("75.00", result)