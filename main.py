from time import sleep
from typing import Tuple, List
import decimal
import typer
import requests
from datetime import datetime, timedelta


# decimal.getcontext().rounding = decimal.ROUND_CEILING
# decimal.getcontext().rounding = decimal.ROUND_DOWN
# decimal.getcontext().rounding = decimal.ROUND_FLOOR
# decimal.getcontext().rounding = decimal.ROUND_HALF_DOWN
# decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN
# decimal.getcontext().rounding = decimal.ROUND_HALF_UP
# decimal.getcontext().rounding = decimal.ROUND_UP
# decimal.getcontext().rounding = decimal.ROUND_05UP
# decimal.getcontext().prec = 7
time_format = "%Y-%m-%dT%H:%M:%SZ"
SECONDS_IN_DAY = 86400

def convert_datetime_to_string(dt: datetime):
    return datetime.strftime(dt, time_format)

def main(
    start: datetime = typer.Argument( ..., formats=[time_format]),
    end: datetime = typer.Argument( ..., formats=[time_format]),
):
    # Accepts two timestamps (in RFC3339 format) as command-line arguments. 
    # Each timestamp represents a particular hour. That is, the "minute" and "second" fields should be zero. 
    # For example, 2021-05-12T19:00:00Z.

    # response = requests.get('https://tsserv.tinkermode.dev/data?begin=2021-03-04T03:00:00Z&end=2021-03-04T11:59:59Z')
    
    # response = requests.get(f'https://tsserv.tinkermode.dev/data?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
    '''
    We will split up the times into 14 hour chunks. The reasoning behind this is that there are 50K seconds in 14 hours. So to make sure that there aren't 
    too many elements being processed.
    '''
    current_day: datetime = start
    total_difference = end - current_day
    items: List[Tuple[str, float]]  = []
    print(start, end, total_difference)
    while total_difference.total_seconds() > SECONDS_IN_DAY:
        print("Starting with ")
        current_day_end = datetime(current_day.year, current_day.month, current_day.day, 23,59,59)
        print("Current day, end, total_difference")
        print(current_day, current_day_end, current_day_end - current_day)
        response = requests.get(f'https://tsserv.tinkermode.dev/data?begin={convert_datetime_to_string(current_day)}&end={convert_datetime_to_string(current_day_end)}')
        output = process_data(response)
        items.extend(output)
        diff = current_day_end - current_day + timedelta(seconds=1)
        current_day += diff
        print(f'next day would be {current_day}')
        # diff = next_day - current_day_end 
        # current_day = current_day + timedelta(0,diff.total_seconds())
        total_difference = end - current_day
        sleep(1)

    if total_difference.total_seconds() >= 0:
        print("The total difference is now one day but not zero")
        print("Current day, end, total_difference")
        print(current_day, end, total_difference)
        response = requests.get(f'https://tsserv.tinkermode.dev/data?begin={convert_datetime_to_string(current_day)}&end={convert_datetime_to_string(end)}')
        output = process_data(response)
        print(output)
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
        help = decimal.Decimal(total / count)
        # print(help)
        results.append((hour, float(round(help, 4))))
        print(f'rounding {total/count} resulted in {round(total / count, 4)} and the decimal version is {round(help, 4)}')
    
    print(f'Processed {len(results)} items')
    return results

def digest_request(text: str) -> List[Tuple[str, float]]:
    time_values = text.split('\n')[:-1]
    results : List[Tuple[str, float]] = []
    for time_value in time_values:
        # 2021-03-04 03:45:14 110.8634
        words = time_value.split(' ')
        if len(words) > 2:
            time, value = words[0], words[2]
        else: 
            time, value = words
        results.append((time, float(value)))
    return results


if __name__ == "__main__":
    typer.run(main)
    # 2021-03-04T03:00:00Z 2021-03-04T11:59:59Z')
