# QA Report Automation & Database Population Script

This Python script automates the processing of global QA test reports from Excel files. It filters, summarizes, and optionally stores the results in a MongoDB database. This is particularly useful for QA teams managing test case data across builds, regions, and contributors.

## Features

- Automates ingestion of QA reports from `.xlsx` files
- Filters test cases by:
  - Test owner (`--user`)
  - Build number (`--date`)
  - Repeatable tests (`--repeatable`)
  - Blocker tests (`--blocker`)
- Outputs results to:
  - Console (terminal)
  - Text files
  - CSV files (`--csv`)
  - MongoDB (`--db1` or `--db2`)
- Verbose mode for detailed insights (`--verbose`)
- Supports batch processing of multiple files

## Requirements

- Python 3.x
- pandas
- pymongo
- openpyxl

Install dependencies:

```bash
pip install pandas pymongo openpyxl
```

## Usage

```bash
python qa_automate.py --files EG4-DBDump_Fall2024.xlsx EG4-DBDump_Spring2024.xlsx [options]
```

### Command-Line Arguments

| Argument        | Description |
|-----------------|-------------|
| `--files`       | One or more Excel files to process |
| `--verbose`     | Output detailed info to the terminal and save as `.txt` |
| `--user`        | Filter tests by "Test Owner" |
| `--date`        | Filter tests by "Build #" value |
| `--repeatable`  | Include only repeatable tests (`Yes`, `Y`, etc.) |
| `--blocker`     | Include only blocker tests (`Yes`, `Y`, etc.) |
| `--csv`         | Export filtered results to CSV |
| `--db1`         | Save results to MongoDB `database1` |
| `--db2`         | Save results to MongoDB `database2` |

### Example Commands

- Process a file with verbose logs:

  ```bash
  python qa_automate.py --files EG4-DBDump_Fall2024.xlsx --verbose
  ```

- Filter by user and export to CSV:

  ```bash
  python qa_automate.py --files EG4-DBDump_Fall2024.xlsx --user "Alice" --csv
  ```

- Insert repeatable + blocker tests into MongoDB:

  ```bash
  python qa_automate.py --files EG4-DBDump_Fall2024.xlsx EG4-DBDump_Spring2024.xlsx --repeatable --blocker --db1
  ```

- Filter by build version and generate reports:

  ```bash
  python qa_automate.py --files EG4-DBDump_Fall2024.xlsx EG4-DBDump_Spring2024.xlsx --date "2.4.1" --csv
  ```

## Output

Depending on options, the script will:

- Display filtered data in the terminal
- Save `.txt` summaries by filename
- Export `.csv` files of filtered results
- Insert structured records into MongoDB with metadata:
  - `import_date`
  - `source_file`

## MongoDB Integration

Requires a running MongoDB instance at `mongodb://localhost:27017/`.

You can target:
- `database1` using `--db1`
- `database2` using `--db2`

Collections are auto-named after the source file (without extension).

## Notes

- Only processes `.xlsx` files
- Relies on columns:
  - `"Test Owner"`
  - `"Build #"`
  - `"Repeatable?"`
  - `"Blocker?"`
