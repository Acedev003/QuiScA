import sys
import re
import pandas as pd

files       = sys.argv[1:]
master_df   = None
indiv_data  = []
total_score = {}

drop_cols = ["First Name","Last Name","Attempt #","Correct","Incorrect","Info","Started At","Total Time Taken","Unattempted","Rank"]

pattern = re.compile(r'([UuPp][Rr][Kk][12][0129])[a-zA-Z][a-zA-Z]\d\d\d\d')

reg_func = lambda x : None if not pattern.search(x) else pattern.search(x)[0].upper()
tim_func = lambda x : x.hour * 3600 + x.minute * 60 + x.second

for file in files:
    df          = pd.read_excel(file,1)

    df["regno"]   = df["First Name"] + df["Last Name"]
    df["regno"]   = df["regno"].apply(reg_func)
    df["seconds"] = df["Total Time Taken"].apply(tim_func)
    
    df.drop(drop_cols,axis=1,inplace=True)
    df.dropna(inplace=True)
    
    indiv_data.append(df)
    df = None

master_df = pd.concat(indiv_data)
master_df.reset_index(inplace=True)

master_df = master_df.groupby("regno").sum(numeric_only=True)

master_df.sort_values(["Score","seconds"],ascending=[False,True],inplace=True)
master_df.reset_index(inplace=True)
master_df.drop(["index"],axis=1,inplace=True)

print(master_df.head().iloc[:,])