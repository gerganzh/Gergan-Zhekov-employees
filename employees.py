"""This code returns the pair of employees that have the longest common
working time across different projects. Pandas is used to read the .txt file
and format it. It is then exported to a .CSV file (which is better for data
management). After that with the use of default dictionaries the needed data is
obtained and printed as a result.
"""

import csv
import pandas as pd
import operator

from collections import defaultdict
from itertools import combinations
from datetime import datetime

# global variables, using default dicts rather than normal dictionaries
d = defaultdict(list)
pairs = defaultdict(list)

df = pd.read_csv('data.txt')  # reading the text data file with pandas

# replacing NULL with the value of today
df['DateTo'] = df['DateTo'].fillna(datetime.today().strftime('%Y-%m-%d'))

# sorting by EmpID, because it will be easier to calculate the output
df = df.sort_values(by=['EmpID'])

df.set_index("EmpID", inplace=True)  # creating EmpID as the index
df.to_csv('new_data.csv')  # exporting to a new .CSV file


with open("new_data.csv") as f:
    next(f)  # skip header
    r = csv.reader(f)
    # unpack, use projectID as key and  append empID, start_date, finish_date
    for EmpID, ProjectID, FromDate, ToDate in r:
        d[int(ProjectID)].append((EmpID, FromDate, ToDate))


for project, aref in d.items():
    # only projects with 2 or more assigned employees
    if len(aref) >= 2:
        for ref in combinations(aref, 2):
            # using lambda operator to create an in-line function
            # mapping start and finish dates with the iterable
            start_date = max(map(lambda x: x[1], ref))
            finish_date = min(map(lambda x: x[2], ref))
            # finding the duration of a project in days
            delta = datetime.strptime(finish_date, '%Y-%m-%d') \
                - datetime.strptime(start_date, '%Y-%m-%d')
            dd = delta.days
            if dd > 0:
                # appending to the dictionary pairs as keys with the working
                # times from different projects as values
                pairs[ref[0][0] + ' and ' + ref[1][0]].append(dd)
                # adding the working times from different projects for all
                # the possible pairs
                new_dict = {k: sum(v) for k, v in pairs.items()}
                # and finding key with highest value
                longest_working_pair = max(new_dict.items(),
                                           key=operator.itemgetter(1))[0]
                # highest value from the dictionary, which is the total days
                # for a single pair of employees
                max_value = max(new_dict.values())

print("Employees that have the longest working time together are employees "
      "with ID: " + str(longest_working_pair) + ". The total working time"
      " of them across different projects is " + str(max_value) + " days")


