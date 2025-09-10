import pytest
from datetime import datetime
from tasks.converters import DateConverter

@pytest.fixture
def date_converter():
    return DateConverter()

def test_to_python(date_converter):
    # Test conversion from string to datetime
    assert date_converter.to_python("2025-09-10") == datetime(2025, 9, 10)

def test_to_url(date_converter):
    # Test conversion from datetime to string
    date_obj = datetime(2025, 9, 10)
    assert date_converter.to_url(date_obj) == "2025-09-10"