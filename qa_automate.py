import argparse
import pandas as pd  
from pymongo import MongoClient 
import os
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--files", dest="workFiles", nargs='+', help="files to process")
parser.add_argument("--verbose", action="store_true", help="show verbose")
parser.add_argument("--db1", action="store_true")
parser.add_argument("--db2", action="store_true")
parser.add_argument("--user", dest="userName")
parser.add_argument("--csv", action="store_true")
parser.add_argument("--repeatable", action="store_true")
parser.add_argument("--blocker", action="store_true")
parser.add_argument("--date", dest="buildDate")

args = parser.parse_args()

if args.workFiles is None:
    print("No testing files selected")
    exit(2)
else:
    total_filtered_data = []
    
    for job in args.workFiles:
        if args.verbose:
            print("verbose!")
            
        if args.db1:
            db_name = "database1"
        elif args.db2:
            db_name = "database2"
            
        try:
            data = pd.read_excel(job)
            base_filename = os.path.basename(job)
            base_name_without_ext = os.path.splitext(base_filename)[0]
            
            filtered_data = data.copy()
            
            if args.userName and "Test Owner" in data.columns:
                filtered_data = filtered_data[filtered_data["Test Owner"].str.contains(args.userName, na=False)]
                
            if args.buildDate and "Build #" in data.columns:
                filtered_data = filtered_data[filtered_data["Build #"].astype(str).str.contains(args.buildDate)]
                
            if args.repeatable and "Repeatable?" in data.columns:
                filtered_data = filtered_data[filtered_data["Repeatable?"].isin(["YES", "Yes", "yes", "Y", "y"])]
                
            if args.blocker and "Blocker?" in data.columns:
                filtered_data = filtered_data[filtered_data["Blocker?"].isin(["YES", "Yes", "yes", "Y", "y"])]
            
            if args.verbose:
                print(f"verbose worked.\n")
                print(f"Total rows: {data.shape[0]}\n")
                
                try:
                    verbose_output_file = f"{base_name_without_ext}_verbose.txt"
                    
                    output_dir = os.path.dirname(verbose_output_file)
                    if output_dir and not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    
                    with open(verbose_output_file, 'w') as f:
                        f.write(f"Total rows: {data.shape[0]}\n")
                        
                        if not data.empty:
                            for index, row in data.iterrows():
                                values = [str(row[column]) for column in row.index if pd.notna(row[column])]
                                line = "\t".join(values)
                                f.write(f"{line}\n")
                    
                    print(f"Verbose output saved to: {verbose_output_file}")
                except Exception as e:
                    print(f"Error creating verbose output file: {e}")
                                
                if not data.empty:
                    for index, row in data.iterrows():
                        values = [str(row[column]) for column in row.index if pd.notna(row[column])]
                        print("\t".join(values))
            
            if args.userName and "Test Owner" in data.columns:
                print(f"{filtered_data.shape[0]} rows")
                
                if not args.verbose and not filtered_data.empty:
                    for index, row in filtered_data.iterrows():
                        values = [str(row[column]) for column in row.index if pd.notna(row[column])]
                        print("\t".join(values))
            
            if args.buildDate and "Build #" in data.columns:
                try:
                    safe_build_date = str(args.buildDate).replace("/", "_").replace("\\", "_").replace(":", "_")
                    date_output_file = f"{base_name_without_ext}_{safe_build_date}.txt"
                    
                    output_dir = os.path.dirname(date_output_file)
                    if output_dir and not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    
                    with open(date_output_file, 'w') as f:
                        f.write(f"Total rows: {filtered_data.shape[0]}\n")
                        
                        if not filtered_data.empty:
                            for index, row in filtered_data.iterrows():
                                values = [str(row[column]) for column in row.index if pd.notna(row[column])]
                                line = "\t".join(values)
                                f.write(f"{line}\n")
                    
                except Exception as e:
                    print(f"Error: {e}")
                    
                print(f"{filtered_data.shape[0]} rows")
                
                if not args.verbose and not args.userName and not filtered_data.empty:
                    for index, row in filtered_data.iterrows():
                        values = [str(row[column]) for column in row.index if pd.notna(row[column])]
                        print("\t".join(values))
            
            if (args.repeatable or args.blocker) and filtered_data is not None:
                try:
                    filter_desc = []
                    if args.repeatable:
                        filter_desc.append("repeatable")
                    if args.blocker:
                        filter_desc.append("blocker")
                    
                    filter_name = "_".join(filter_desc)
                    output_file = f"{base_name_without_ext}_{filter_name}.txt"
                    
                    output_dir = os.path.dirname(output_file)
                    if output_dir and not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    
                    with open(output_file, 'w') as f:
                        f.write(f"Total rows: {filtered_data.shape[0]}\n")
                        
                        if not filtered_data.empty:
                            for index, row in filtered_data.iterrows():
                                values = [str(row[column]) for column in row.index if pd.notna(row[column])]
                                line = "\t".join(values)
                                f.write(f"{line}\n")
                                
                    print(f"output saved")
                except Exception as e:
                    print(f"Error: {e}")
                
                print(f"{filtered_data.shape[0]}")
                
                if not args.verbose and not args.userName and not args.buildDate and not filtered_data.empty:
                    for index, row in filtered_data.iterrows():
                        values = [str(row[column]) for column in row.index if pd.notna(row[column])]
                        print("\t".join(values))
            
            filtered_data['Source_File'] = os.path.basename(job)
            total_filtered_data.append(filtered_data)
            
            if args.csv:
                output_file = f"{base_name_without_ext}.csv"
                filtered_data.to_csv(output_file, index=False)
                print(f"{output_file}")

            if not args.verbose and not args.userName and not args.buildDate and not args.repeatable and not args.blocker:
                print(f"\nRows: {filtered_data.shape[0]}")
                
                if "Test Owner" in filtered_data.columns:
                    owners_count = {}
                    for owner in filtered_data["Test Owner"].dropna():
                        if owner in owners_count:
                            owners_count[owner] += 1
                        else:
                            owners_count[owner] = 1
                    
                    print("\nTest Owners:")
                    for owner, count in owners_count.items():
                        print(f"{owner}: {count} tests")
            
            if args.db1 or args.db2:
                myclient = MongoClient('mongodb://localhost:27017/')
                mydb = myclient[db_name]
                collection_name = f"{base_name_without_ext}"
                mycol = mydb[collection_name]
                records = filtered_data.to_dict('records')
                
                for record in records:
                    record['import_date'] = datetime.datetime.now()
                    record['source_file'] = job
                
                result = mycol.insert_many(records)
                
                if args.verbose:
                    print(f"\nConnected to mongo")
                    print(f"{len(result.inserted_ids)} records in database: {db_name}, {collection_name}")

        except Exception as e:
            print(f"{e}")
            continue
    
    if args.csv and len(args.workFiles) > 1 and total_filtered_data:
        combined = pd.concat(total_filtered_data, ignore_index=True)
        
        if args.userName:
            output_file = f"{args.userName}.csv"
            combined_txt_file = f"{args.userName}.txt"
            
            try:
                output_dir = os.path.dirname(combined_txt_file)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                with open(combined_txt_file, 'w') as f:
                    f.write(f"Total rows: {combined.shape[0]}\n")
                    
                    if not combined.empty:
                        for index, row in combined.iterrows():
                            values = [str(row[column]) for column in row.index if pd.notna(row[column])]
                            line = "\t".join(values)
                            f.write(f"{line}\n")
            except Exception as e:
                print(f"Error: {e}")
            
            print(f"Total rows: {combined.shape[0]}")
        else:
            filter_type = []
            if args.repeatable:
                filter_type.append("repeatable")
            if args.blocker:
                filter_type.append("blocker")
            if args.buildDate:
                filter_type.append(f"build_{args.buildDate}")
            
            filter_name = "_".join(filter_type) if filter_type else "combined"
            output_file = f"{filter_name}.csv"
            combined_txt_file = f"{filter_name}_combined.txt"
            
            try:
                output_dir = os.path.dirname(combined_txt_file)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                with open(combined_txt_file, 'w') as f:
                    f.write(f"Total rows: {combined.shape[0]}\n")
                    
                    if not combined.empty:
                        for index, row in combined.iterrows():
                            values = [str(row[column]) for column in row.index if pd.notna(row[column])]
                            line = "\t".join(values)
                            f.write(f"{line}\n")
            except Exception as e:
                print(f"Error : {e}")
            
            print(f"Total rows: {combined.shape[0]}\n")
        
        combined.to_csv(output_file, index=False)
