# Executing code
python main.py 2021-03-04T03:00:00Z 2021-03-08T11:59:59Z

I included a requirements.txt if required but it may not be complete
pip install -requirement requirements.txt

I also included a mini test bash script to go over the test cases I used. However if you jump to the #d44b9f3cfba2e495bc2bd70238075f8a4be3856d commit 
you can use a pytest that I included since at that time I was storing the combined data in a list
pytest -vv

# Proccessing the Data
If you view the get request from the *data* endpoint as a tuple of datetime to float you can then use a hashmap that maps 
'year:month:day:hour' as a key and the value is a pair (total , count). This way we can keep a running sum of our average.
Once we have all the totals and counts then we can properly calculate the averages per key and output them

# Handling large data loads
In order to avoid processing all the data at once I used a hueristic. If we only process one day at a time we can ensure that 
the list that helps with the processing never grows to a value large enough to cause problems. There are 86400 seconds in a day
which is not an unusually high amount. Based off some test cases it appears that the data is fairly sparse relative to the seconds 
so it is actually much less than the 86400 number.

Furthermore, this hueristic allows us to clear the hashmap safely since we are sure that there will be no hash conflicts between days

# Oddities
## Rounding Error
I ran into a strange rounding error in my testing. One of the averages has a value of 107.0418 according to the hourly endpoint
whereas my script reports back 107.0417. After investigating this different I believe it is due to some peculirarity in significant digits and 
rounding.

Assuming the code written by Mode was either in Go or JavaScript I would still assume that the rounding would support my 107.0417 value.

![image](https://user-images.githubusercontent.com/30095041/233899118-f8fb07ab-d4a1-49d7-bcc3-12b1f5326ddd.png)
![image](https://user-images.githubusercontent.com/30095041/233899131-59e30c4e-743d-4132-8c3d-de618b477219.png)

I have also tried experiment with the rounding modes found in the [https://docs.python.org/3/library/decimal.html#rounding-modes](decimal) module.

## Faulty Input?
I believe I also found a case where the expected results do not make sense.
If you look at the following url https://tsserv.tinkermode.dev/data?begin=2021-03-02T04:00:00Z&end=2021-03-10T00:00:00Z you would see that 
no data exists with datetime hour 2021-03-10T00:00:00Z however in the hourly endpoint (https://tsserv.tinkermode.dev/hourly?begin=2021-03-02T04:00:00Z&end=2021-03-10T00:00:00Z) there is an average that exists
