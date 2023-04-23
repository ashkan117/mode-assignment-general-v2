from datetime import datetime
time_format = "%Y-%m-%dT%H:%M:%SZ"
from main import convert_datetime_to_string, main, digest_request
import requests

def runner(start, end, expected):
    start_datetime = datetime.strptime(start,time_format)
    end_datetime = datetime.strptime(end,time_format)

    assert main(start_datetime, end_datetime) == expected

def test_one():
    start = datetime(2021, 3, 4, 4)
    end = datetime(2021, 3, 4, 11, 59, 59)

    actual = main(start, end)
    output_response = requests.get(f'https://tsserv.tinkermode.dev/hourly?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
    output = digest_request(output_response.text)
    assert actual == output

# def test_two():
#     start = datetime(2021, 3, 2, 4)
#     end = datetime(2021, 3, 8, 11, 59, 59)
#
#     actual = main(start, end)
#     output_response = requests.get(f'https://tsserv.tinkermode.dev/hourly?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
#     output = digest_request(output_response.text)
#     assert actual == output

def test_three():
    start = datetime(2021, 3, 2, 4)
    end = datetime(2021, 3, 4, 11, 59, 59)

    actual = main(start, end)
    output_response = requests.get(f'https://tsserv.tinkermode.dev/hourly?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
    output = digest_request(output_response.text)
    assert actual == output
    # expected = requests.get('https://tsserv.tinkermode.dev/data?begin=2021-03-04T03:00:00Z&end=2021-03-04T11:59:59Z')
    # expected_response
    # expected_1 = [
    #         ("2021-03-04T03:00:00Z",  113.1652),
    #         ("2021-03-04T04:00:00Z",  105.5466),
    #         ("2021-03-04T05:00:00Z",   99.7907),
    #         ("2021-03-04T06:00:00Z",   94.8736),
    #         ("2021-03-04T07:00:00Z",   89.3490),
    #         ("2021-03-04T08:00:00Z",   81.8498),
    #         ("2021-03-04T09:00:00Z",   71.6812),
    #         ("2021-03-04T10:00:00Z",   59.5748),
    #         ("2021-03-04T11:00:00Z",   47.0522)
    #         ]
    # runner("2021-03-04T03:00:00Z","2021-03-04T11:59:59Z", expected_1)
