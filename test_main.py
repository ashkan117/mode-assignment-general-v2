from datetime import datetime
time_format = "%Y-%m-%dT%H:%M:%SZ"
from main import convert_datetime_to_string, main, digest_request
import requests

def runner(start, end, expected):
    start_datetime = datetime.strptime(start,time_format)
    end_datetime = datetime.strptime(end,time_format)

    assert main(start_datetime, end_datetime) == expected

# def test_one():
#     start = datetime(2021, 3, 4, 4)
#     end = datetime(2021, 3, 4, 11, 59, 59)
#
#     actual = main(start, end)
#     output_response = requests.get(f'https://tsserv.tinkermode.dev/hourly?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
#     output = digest_request(output_response.text)
#     assert actual == output
#
# def test_two():
#     start = datetime(2021, 3, 2, 4)
#     end = datetime(2021, 3, 8, 11, 59, 59)
#     actual = main(start, end)
#     with open('actual.txt', 'w') as file:
#         for time, average in actual:
#             file.write(f'{time} {float(average)}\n')
#
#
#     output_response = requests.get(f'https://tsserv.tinkermode.dev/hourly?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
#     output = digest_request(output_response.text)
#     with open('expected.txt', 'w') as file:
#         for time, average in output:
#             file.write(f'{time} {average}\n')
#     print(len(actual))
#     print(len(output))
#     print(actual)
#     print(output)
#     assert actual == output
#
# def test_three():
#     start = datetime(2021, 3, 2, 4)
#     end = datetime(2021, 3, 3, 11, 59, 59)
#
#     actual = main(start, end)
#     with open('actual.txt', 'w') as file:
#         for time, average in actual:
#             file.write(f'{time} {float(average)}\n')
#
#
#     output_response = requests.get(f'https://tsserv.tinkermode.dev/hourly?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
#     output = digest_request(output_response.text)
#     with open('expected.txt', 'w') as file:
#         for time, average in output:
#             file.write(f'{time} {average}\n')
#     print(len(actual))
#     print(len(output))
#     print(actual)
#     print(output)
#     assert actual == output

def test_four():
    start = datetime(2021, 3, 2, 4)
    end = datetime(2021, 3, 10) 

    actual = main(start, end)
    with open('actual.txt', 'w') as file:
        for time, average in actual:
            file.write(f'{time} {float(average)}\n')


    output_response = requests.get(f'https://tsserv.tinkermode.dev/hourly?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
    output = digest_request(output_response.text)
    with open('expected.txt', 'w') as file:
        for time, average in output:
            file.write(f'{time} {average}\n')
    print(len(actual))
    print(len(output))
    print(actual)
    print(output)
    assert actual == output

# def test_long():
#     start = datetime(2021, 3, 2, 4)
#     end = datetime(2021, 12, 3, 11, 59, 59)
#
#     actual = main(start, end)
#     with open('actual.txt', 'w') as file:
#         for time, average in actual:
#             file.write(f'{time} {float(average)}\n')
#
#
#     output_response = requests.get(f'https://tsserv.tinkermode.dev/hourly?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
#     output = digest_request(output_response.text)
#     with open('expected.txt', 'w') as file:
#         for time, average in output:
#             file.write(f'{time} {average}\n')
#     print(len(actual))
#     print(len(output))
#     print(actual)
#     print(output)
#     assert actual == output
