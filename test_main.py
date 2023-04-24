from datetime import datetime
from main import convert_datetime_to_string, main, digest_request
import requests

def test_one():
    start = datetime(2021, 3, 4, 4)
    end = datetime(2021, 3, 4, 11, 59, 59)

    actual = main(start, end)
    output_response = requests.get(f'https://tsserv.tinkermode.dev/hourly?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
    output = digest_request(output_response.text)
    assert actual == output

def test_two():
    start = datetime(2021, 3, 2, 4)
    end = datetime(2021, 3, 8, 11, 59, 59)
    actual = main(start, end)

    output_response = requests.get(f'https://tsserv.tinkermode.dev/hourly?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
    output = digest_request(output_response.text)
    assert actual == output
#
def test_three():
    start = datetime(2021, 3, 2, 4)
    end = datetime(2021, 3, 3, 11, 59, 59)

    actual = main(start, end)
    output_response = requests.get(f'https://tsserv.tinkermode.dev/hourly?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
    output = digest_request(output_response.text)
    assert actual == output

def test_four():
    start = datetime(2021, 3, 2, 4)
    end = datetime(2021, 3, 10) 

    actual = main(start, end)
    output_response = requests.get(f'https://tsserv.tinkermode.dev/hourly?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
    output = digest_request(output_response.text)
    assert actual == output

# commented since it will take some time
# def test_long():
#     start = datetime(2021, 3, 2, 4)
#     end = datetime(2021, 12, 3, 11, 59, 59)
#
#     actual = main(start, end)
#     output_response = requests.get(f'https://tsserv.tinkermode.dev/hourly?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
#     output = digest_request(output_response.text)
#     assert actual == output
