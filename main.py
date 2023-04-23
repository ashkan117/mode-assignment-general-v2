from typing import Tuple, List
import decimal
import typer
import requests
from datetime import datetime


decimal.getcontext().rounding = decimal.ROUND_CEILING
time_format = "%Y-%m-%dT%H:%M:%SZ"

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
    response = requests.get(f'https://tsserv.tinkermode.dev/data?begin={convert_datetime_to_string(start)}&end={convert_datetime_to_string(end)}')
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
        rounded_value = round(float(help), 4)
        # if str(total / count)[-1] == "5":
        #     rounded_value += .0001
        #     rounded_value = round(rounded_value, 4)
        results.append((hour, rounded_value))
        print(f'rounding {total/count} resulted in {round(total / count, 4)} and the decimal version is {round(help, 4)}')

    return results

    
    # response = requests.get('https://tsserv.tinkermode.dev/data?begin=2021-03-04T03:00:00Z&end=2021-03-04T11:59:59Z')

def digest_request(text: str) -> List[Tuple[str, float]]:
    time_values = text.split('\n')[:-1]
    # times: List[str] = []
    # values: List[float] = []
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
