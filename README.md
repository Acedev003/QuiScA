# QuiScA - Quizizz Score Aggregator

A tool to compile and analyze multiple Quizizz reports to get statistics and rankings of students.

Features : 
- Merges data from multiple Quizizz reports
- Display all or top 10 scores
- Option to save aggregated data in an Excel file

## Installation

Install it from pypi using : 
```
pip install quisca
```

## Usage

The tool can be run from the command line using the following syntax:

```
quisca -f [file1.xlsx] [file2.xlsx] ... [-a] [-o [output.xlsx]] [-v]
```
- `-f, --files: List of Quizizz report files to process (required)`
- `-a, --all: Show/print all data (default option shows top 10 rankers)`
- `-o, --output: Save output into a .xlsx file`
- `-v, --verbose: Activate verbose output`
- `-h, --help: View help`

## Dependencies

- pandas
- tabulate