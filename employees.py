from collections import defaultdict
from itertools import combinations
from datetime import datetime
import pandas as pd
import csv

df = pd.read_csv('data.csv') #reading the text data file with pandas
df['DateTo'] = df['DateTo'].fillna(datetime.today().strftime('%Y-%m-%d')) #replacing NULL with the value of Today
df.set_index("EmpID", inplace = True) #creating EmpID as the index, as otherwise there would be problem with the reading of the data
df.to_csv('new_data.csv') #exporting to a new text file

d = defaultdict(list) #

with open("new_data.csv") as f:
    next(f) # skip header
    r = csv.reader(f)
    # unpack use projectID as key and  append empID, start date, finish date
    for EmpID, ProjectID, FromDate, ToDate in r:
        d[int(ProjectID)].append((EmpID, FromDate, ToDate))

list_projects = []
t = defaultdict(list)

for job, aref in d.items():

    if len(aref) >= 2:
        for ref in combinations(aref, 2):

            begin = max(map(lambda x: x[1], ref))
            end = min(map(lambda x: x[2], ref))
            delta = datetime.strptime(end, '%Y-%m-%d') \
                    - datetime.strptime(begin, '%Y-%m-%d')
            dd = delta.days
            if dd > 0:
                list_projects.append(dd)
                t[ref[0][0]+ ' and ' + ref[1][0]].append(dd)
                #print('Employees with EmpID:', ref[0][0], 'and', ref[1][0],
                      #'worked together on a common project (Project ID:', job, ') for a total of', dd, 'days\n')

print('The pair that has worked together the longest according to the data file input are employees with ID ' + str(max(t, key=t.get)) + ' with a working time of ' + str(max(list_projects)) + ' days')
