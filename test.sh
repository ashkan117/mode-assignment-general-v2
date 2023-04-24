echo General Test One
python main.py 2021-03-04T03:00:00Z 2021-03-08T11:59:59Z > actual.txt
curl 'https://tsserv.tinkermode.dev/hourly?begin=2021-03-04T03:00:00Z&end=2021-03-08T11:59:59Z' > expected.txt
diff --ignore-blank-lines --ignore-all-space actual.txt expected.txt

echo General Test Two
python main.py 2021-03-02T04:00:00Z 2021-03-08T11:59:59Z > actual1.txt
curl 'https://tsserv.tinkermode.dev/hourly?begin=2021-03-02T04:00:00Z&end=2021-03-08T11:59:59Z' > expected1.txt
diff --ignore-blank-lines --ignore-all-space actual1.txt expected1.txt

echo General Test Three
python main.py 2021-03-02T04:00:00Z 2021-03-03T11:59:59Z > actual2.txt
curl 'https://tsserv.tinkermode.dev/hourly?begin=2021-03-02T04:00:00Z&end=2021-03-03T11:59:59Z' > expected2.txt
diff --ignore-blank-lines --ignore-all-space actual2.txt expected2.txt

echo General Test Four
python main.py 2021-03-02T04:00:00Z 2021-03-10T00:00:00Z > actual3.txt
curl 'https://tsserv.tinkermode.dev/hourly?begin=2021-03-02T04:00:00Z&end=2021-03-10T00:00:00Z' > expected3.txt
diff --ignore-blank-lines --ignore-all-space actual3.txt expected3.txt
