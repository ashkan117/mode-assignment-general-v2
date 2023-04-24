from typing import Tuple, List
import decimal
import typer
import requests
from datetime import datetime, timedelta

TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
SECONDS_IN_DAY = 86400

def convert_datetime_to_string(dt: datetime):
    return datetime.strftime(dt, TIME_FORMAT)

def main(
    start: datetime = typer.Argument( ..., formats=[TIME_FORMAT]),
    end: datetime = typer.Argument( ..., formats=[TIME_FORMAT]),
):
    current_day: datetime = start
    total_difference = end - current_day
    items: List[Tuple[str, float]]  = []
    while total_difference.total_seconds() > SECONDS_IN_DAY:
        current_day_end = datetime(current_day.year, current_day.month, current_day.day, 23,59,59)
        response = requests.get(f'https://tsserv.tinkermode.dev/data?begin={convert_datetime_to_string(current_day)}&end={convert_datetime_to_string(current_day_end)}')
        output = process_data(response)
        items.extend(output)
        diff = current_day_end - current_day + timedelta(seconds=1)
        current_day += diff
        total_difference = end - current_day

    if total_difference.total_seconds() >= 0:
        response = requests.get(f'https://tsserv.tinkermode.dev/data?begin={convert_datetime_to_string(current_day)}&end={convert_datetime_to_string(end)}')
        output = process_data(response)
        items.extend(output)
    response = requests.get(f'https://tsserv.tinkermode.dev/data?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
    output = process_data(response)
    response = requests.get(f'https://tsserv.tinkermode.dev/hourly?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
    output = process_data(response)
    return items

def process_data(response: requests.Response) -> List[Tuple[str, float]]:
    times_values = digest_request(response.text)
    times_values = [(time[:-7], value) for time, value in times_values]
    hourly_buckets = {}
    for time, value in times_values:
        if time in hourly_buckets:
            total, count = hourly_buckets[time]
            total += value
            count += 1
            hourly_buckets[time] = (total, count)
        else:
            hourly_buckets[time] = (value, 1)
    
    results : List[Tuple[str, float]]= []
    for hour, tup in hourly_buckets.items():
        total, count = tup
        hour = hour + ":00:00Z"
        average = decimal.Decimal(total / count)
        rounded_average = float(round(average, 4))
        print(f'{hour} {rounded_average}')
        results.append((hour, rounded_average))
    
    return results

def digest_request(text: str) -> List[Tuple[str, float]]:
    '''
    We are reading the request from the data endpoint and transforming it into a tuple
    '''
    # last element is a new line character
    time_values = text.split('\n')[:-1]
    results : List[Tuple[str, float]] = []
    for time_value in time_values:
        # every row looks like the one below
        # 2021-03-04 03:45:14 110.8634
        words = time_value.split(' ')
        # there are some cases where there is an additional space in the words array
        # [time, ' ', value]
        if len(words) > 2:
            time, value = words[0], words[2]
        else: 
            time, value = words
        results.append((time, float(value)))
    return results


if __name__ == "__main__":
    typer.run(main)
