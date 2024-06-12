# WEATHER MAN


1. To get the highest temperature, lowest temperature and humidity for a given year, run:
```weatherman.py dir/path/for/files/extraction -e 2006```

2. To get the average highest temperature​, average lowest temperature​,​ average mean humidity​ for a month, run:
```weatherman.py dir/path/for/files/extraction -a 2006/5```

3. To draw horizontal bar charts on the console for highest and lowest temperature on each day, run:
```weatherman.py dir/path/for/files/extraction -c 2006/5```

4. Multiple reports can be generated by passing multiple arguments, like:
```weatherman.py dir/path/for/files/extraction -c 2011/03 -a 2011/3 -e 2011```

5. For a given month, to get one horizontal bar chart per day, add --inline flag to the command:
```weatherman.py dir/path/for/files/extraction -c 2011/3 --inline```