import argparse
import re

import pandas as pd
from tabulate import tabulate
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="A tool to compile and analyze multiple Quizizz reports to get statistics and rankings of KITS students.")
    parser.add_argument("-f","--files",nargs='+',help="List of Quizizz report files to process (required)")
    parser.add_argument("-o","--output",action="store",help="Save output into a .xlsx file")
    parser.add_argument("-a","--all",action="store_const",const=True,help="Show/print all data (default option shows top 10 rankers)")
    parser.add_argument("-v","--verbose",action="store_const",const=True,help="Activate verbose output")
    args = parser.parse_args()

    drop_cols = ["First Name","Last Name","Attempt #","Correct","Incorrect","Info","Started At","Total Time Taken","Unattempted","Rank"]
    df_list   = []

    pattern   = re.compile(r'([UuPp][RrLl][Kk][12][0129])[a-zA-Z][a-zA-Z]\d\d\d\d')

    reg_func = lambda x : None if not pattern.search(x) else pattern.search(x)[0].upper()
    tim_func = lambda x : x.hour * 3600 + x.minute * 60 + x.second

    qprint = lambda msg: None
    if args.verbose:
        qprint = lambda msg: print(msg)

    if(not args.files):
        parser.print_help()
        return False
    
    for file in args.files:
        qprint(f"Reading file ({file})")
        df = None
        try:
            df = pd.read_excel(file,1)
        except FileNotFoundError:
            qprint(f"File not found ({file})")
        
        df["Reg No"]  = df["First Name"] + df["Last Name"]
        df["Reg No"]  = df["Reg No"].apply(reg_func)
        df["Seconds"] = df["Total Time Taken"].apply(tim_func)

        df.drop(drop_cols,axis=1,inplace=True)
        df.dropna(inplace=True)

        df_list.append(df)
    
    master_df = pd.concat(df_list)
    master_df.reset_index(inplace=True)

    master_df = master_df.groupby("Reg No").sum(numeric_only=True)
    master_df.sort_values(["Score","Seconds"],ascending=[False,True],inplace=True)
    master_df.reset_index(inplace=True)
    master_df.index = master_df.index + 1 
    master_df.drop(["index"],axis=1,inplace=True)
    
    if args.output:
        if(Path(args.output).suffix in [".xlsx"]):
            master_df.to_excel(args.output)
            return True
        else:
            qprint(f"Unable to open ({args.output})")
            return False

    if args.all:
        print("\n - TOP Scores - \n")
        print(tabulate(master_df.iloc[:,], headers='keys', tablefmt='psql'))
    else:
        print("\n - TOP 10 Scores - \n")
        print(tabulate(master_df.head(10).iloc[:,], headers='keys', tablefmt='psql'))
