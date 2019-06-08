"""Pandas is used to open the data text file and read it as a CSV (a plain
text format used for data management,which uses comma as a separator between
the different values). The data is exported to a pandas DataFrame, the dates
are properly formatted from the reader and the NULL value is automatically
replace with the current date in the same format. The new table is then
outputted to a new CSV file, and is opened and read by Python. A defaultdict
is used instead of a normal dictionary, and ProjectID serves as a key.
Another empty dictionary is created that is going to be filled with the
results from the loop and contain a pair of employees as a key, and the days
worked as a value. In the final print statement the code will return the
pair with the max value.
"""

import csv
import pandas as pd
import operator

from collections import defaultdict
from itertools import combinations
from datetime import datetime

# global variables
d = defaultdict(list)
t = defaultdict(list)

list_projects = [] # a list that will keep track of days worked on a project

df = pd.read_csv('data.txt')  # reading the text data file with pandas

# replacing NULL with the value of today
df['DateTo'] = df['DateTo'].fillna(datetime.today().strftime('%Y-%m-%d'))
df = df.sort_values(by=['EmpID'])# sorting to EmpID, because it will come to
#  use later
df.set_index("EmpID", inplace=True)  # creating EmpID as the index
df.to_csv('new_data.csv')  # exporting to a new text file


with open("new_data.csv") as f:
    next(f)  # skip header
    r = csv.reader(f)
    # unpack, use projectID as key and  append empID, start_date, finish_date
    for EmpID, ProjectID, FromDate, ToDate in r:
        d[int(ProjectID)].append((EmpID, FromDate, ToDate))


for project, aref in d.items():
    # finding which projects had two or more employees assigned
    if len(aref) >= 2:
        #using combinations package to iterate
        for ref in combinations(aref, 2):
            #using lambda as a function
            #mapping start and finish dates with the iterable
            start_date = max(map(lambda x: x[1], ref))
            finish_date = min(map(lambda x: x[2], ref))
            #calculating the days using the datetime package
            delta = datetime.strptime(finish_date, '%Y-%m-%d') \
                - datetime.strptime(start_date, '%Y-%m-%d')
            dd = delta.days
            if dd > 0:
                list_projects.append(dd)
                #appending to the dictionary for the output
                t[ref[0][0] + ' and ' + ref[1][0]].append(dd)
                new_dict = {k: sum(v) for k, v in t.items()}


print("Employees that have the longest working time together are employees "
      "with ID: " +
      str(max(new_dict.items(), key=operator.itemgetter(1))[0]))


