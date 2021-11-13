import urllib.request
from bs4 import BeautifulSoup
import requests
import csv
import io
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

url = "https://en.wikipedia.org/wiki/50_Greatest_Players_in_NBA_History"
html_content = requests.get(url).text

soup = BeautifulSoup(html_content, "lxml")

data = {}

for all_table in soup.find_all('table', class_='wikitable sortable', limit=2):
    all_table_data = all_table.tbody.find_all("tr") 
    
headings = []

for th in all_table_data[0].find_all('th'):
    head = th.text.replace('\n', '').strip()
    headings.append(head)

                    
for table in all_table_data:
    for heading in  headings:
    
        table_data = []
        for tr in all_table.find_all("tr"): 
            t_row = {}
      
            for td, th in zip(tr.find_all("td"), headings): 
          
                t_row[th] = td.text.replace('\n', '').strip()
            table_data.append(t_row)
      
        data[heading] = table_data[1:]
        df = pd.DataFrame(data[heading])

df.to_csv("50_Greatest_Players_in_NBA_History.csv", index=False)
print("50 Greatest of Players in NBA History:\n")
df
#  Plotting Data from DataFram
#csv_path = 'C:\\.....\\50_Greatest_Players_in_NBA_History.csv'
#df = pd.read_csv(csv_path)
df = df.head(10)
display(df)
dfAll =df[df['Championships won[b]'] != "None"]
dfChamp = dfAll.apply(lambda row:  str(row["Championships won[b]"][0]), axis = 1)
dfChamp = dfChamp.astype(int)

dfName = dfAll['Name'] 
y_posName = range(len(dfName))

plt.bar(y_posName, dfChamp, color = "blue", width = 0.2)
plt.xticks(y_posName, dfName, rotation=90)
plt.xlabel('Name')
plt.ylabel('Championships won')
plt.title('Championships won')
plt.show()



dfAllMVP =df[df['MVP won'] != "None"]
dfMVP = dfAllMVP.apply(lambda row:  str(row["MVP won"][0]), axis = 1)
dfMVP = dfMVP.astype(int)

dfYear = np.array(dfAllMVP['Year'] )

dfName2 = dfAllMVP['Name'] 
y_posName2 = range(len(dfName2))
plt.xticks(y_posName2, dfName2, rotation=90)

plt.plot(y_posName, dfChamp, label='Championships won')
plt.plot(y_posName2,dfMVP,label='MVP won')
plt.xlabel('Name')
plt.ylabel('Championships and MVP')
plt.title('Championships won and MVP won')
plt.legend()

plt.show()
