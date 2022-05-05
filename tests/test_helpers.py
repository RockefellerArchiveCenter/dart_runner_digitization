import json
from os.path import join

import pytest

from create_bags.helpers import create_tag, format_aspace_date


def test_create_tag():
    created_tag = create_tag("testName", "test value")
    expected_result = {"tagFile": "bag-info.txt",
                       "tagName": "testName", "userValue": "test value"}
    assert created_tag == expected_result


def test_format_aspace_date(ao_date_data):
    dates = format_aspace_date(ao_date_data)
    assert dates[0] == "1950-01-01"
    assert dates[1] == "1969-12-31"


@pytest.fixture
def ao_data():
    path_to_file = join("tests", "data", "ao_data.json")
    with open(path_to_file, "r") as read_file:
        data = json.load(read_file)
    return(data)


@pytest.fixture
def ao_date_data():
    path_to_file = join("tests", "data", "ao_date_data.json")
    with open(path_to_file, "r") as read_file:
        data = json.load(read_file)
    return(data)
