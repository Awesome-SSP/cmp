from RPA.Database import Database
from RPA.Excel.Application import Application
import pandas as pd
import os
from datetime import datetime
from RPA.FileSystem import FileSystem
from datetime import datetime, timedelta
import shutil
import subprocess
from dotenv import load_dotenv
import mysql.connector


'''
pip install rpaframework
pip install pandas
'''


# Export all tables
def Data(table_list,folder,databaseName,choice):
    tables = [item[f'Tables_in_{databaseName}'] for item in table_list ]
    
    
    for table in tables:
        data = db.query(f"SELECT * FROM `{table}`")
        df = pd.DataFrame(data)
        
        if choice == 1:
            
            df.to_csv(os.path.join(os.path.join(folder, f"{table}.csv")), index=False)
            
        elif choice == 2:
            df.to_json(os.path.join(folder, f"{table}.json"), index=False)
        elif choice == 3:
            df.to_excel(os.path.join(folder, f"{table}.xlsx"), index=False)
        
        elif choice == 4:
            df.to_csv(os.path.join(folder, f"{table}.csv"), index=False)
            df.to_json(os.path.join(folder, f"{table}.json"), index=False)
        elif choice == 5:
            df.to_json(os.path.join(folder, f"{table}.json"), index=False)
            df.to_excel(os.path.join(folder, f"{table}.xlsx"), index=False)
        elif choice == 6:
            df.to_csv(os.path.join(folder, f"{table}.csv"), index=False)
            df.to_excel(os.path.join(folder, f"{table}.xlsx"), index=False)
            
        elif choice == 7:
            
            df.to_csv(os.path.join(folder, f"{table}.csv"), index=False)
            df.to_json(os.path.join(folder, f"{table}.json"), index=False)
            df.to_excel(os.path.join(folder, f"{table}.xlsx"), index=False)
        
        # To covert the data into PDF
        elif choice == 8:
            # Your DataFrame saving logic
            df.to_excel(os.path.join(folder, f"{table}.xlsx"), index=False)

            # Initialize Excel COM automation
            excel = Application()
            excel.visible = False  # Keep Excel hidden

            # Open the Excel file
            workbook = excel.open_workbook(os.path.join(folder, f"{table}.xlsx"))

            # Save as PDF
            workbook.export_as_fixed_format(0, os.path.join(folder, f"{table}.pdf"))
            fs = FileSystem()
            fs.remove_file(os.path.join(folder, f"{table}.xlsx"))
            # Close workbook and quit Excel
            excel.close_workbook()
            excel.quit()
        
        else:
            print("wrong choice")
               
def backup_databases(databases, output_dir= '.', filename="combined_backup.sql", user=os.getenv('user'), password=os.getenv("password")):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_dir, f"{filename}")

    # Create one combined .sql file
    with open(file_path, 'w') as outfile:
        for db in databases:
            print(f"🔄 Dumping database: {db}")
            try:
                mysqldump_path = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"

                dump = subprocess.run(
                    [mysqldump_path, "-u", user, f"-p{password}", "--databases", db],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                    text=True
                    )

                outfile.write(dump.stdout)
                outfile.write("\n\n")
                print(f"✅ {db} added to backup.")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error dumping {db}: {e.stderr}")

    print(f"\n📁 Backup created: {file_path}")      
       
def script(n):
    load_dotenv()
    while(n):
        databaseName = input("enter database name: ")
        choice = int(input("\n Enter your choice of file [csv , json , excel ,{csv,json} , {json ,excel} , {csv, excel} ,all \nusing number [1,2,3,4,5,6,7]: "))
        # Create timestamped folder
        
        folder = f"DATA_{databaseName}_{datetime.now():%Y%m%d_%H%M%S}"
        fullfolder = os.path.join(mainFolder,folder)
        os.makedirs(fullfolder, exist_ok=True)

        db.connect_to_database(
    "mysql.connector", 
    databaseName,
    f"{os.getenv("user")}", 
    f"{os.getenv("password")}", 
    "localhost", 
    3306)


        tables = db.query("SHOW TABLES")
        table_list = [row for row in tables]
        print("-"*60,"\n")
        print(table_list)
        print("\n SUCCESSFUL OPERATION \n")
        print("-"*60,"\n")
        Data(table_list,fullfolder,databaseName ,choice)

        db.disconnect_from_database()
        n -=1

# def delete_old_backups(days=7):
#     now = datetime.now()
#     cutoff_date = now - timedelta(days=days)
#     current_dir = os.getcwd()

#     for folder in os.listdir(current_dir):
#         folder_path = os.path.join(current_dir, folder)
#         if os.path.isdir(folder_path) and folder.startswith("backup_"):
#             try:
#                 folder_date = datetime.strptime(folder.split('_')[-1], '%Y-%m-%d')
#                 if folder_date < cutoff_date:
#                     shutil.rmtree(folder_path)
#                     print(f"🗑 Deleted old backup: {folder_path}")
#             except Exception as e:
#                 print(f"⚠ Skipping folder {folder_path}: {e}")

def delete_old_backups(days=7):
    now = datetime.now()
    cutoff_date = now - timedelta(days=days)
    current_dir = os.getcwd()

    for folder in os.listdir(current_dir):
        folder_path = os.path.join(current_dir, folder)
        if os.path.isdir(folder_path):
            try:
                # Expecting folder name as 'YYYYMMDD'
                folder_date = datetime.strptime(folder, '%Y%m%d')
                if folder_date < cutoff_date:
                    shutil.rmtree(folder_path)
                    print(f"🗑 Deleted old backup: {folder_path}")
            except ValueError:
                # Skip folders that are not in the expected date format
                pass
            except Exception as e:
                print(f"⚠ Skipping folder {folder_path}: {e}")


if __name__ == "__main__":
    
    ''' This code is working for the 7 elements and PDF ka code on progress hai
    
    Enter your MYSQL USER NAME AND PASSWORD ACCORDINGLY IN THE 
    SCRIPT() AND backup_databases()
    
    '''
    
    
    load_dotenv()
    db = Database()
    
    mainFolder = f"{datetime.now():%Y%m%d}"
    os.makedirs(mainFolder, exist_ok=True)
    print("\n\nHello Boss Good Morning (-_-)\n")
    # n = int(input("Enter a number for how many databases you want to fetch  :  "))
    choice  =int(input("you want data in .sql or other format press[1,2] :  "))
    
    # if(choice == 1):
    #     db_list = []
    #     while(n):
    #         dbc = input("enter a database name: ")
    #         db_list.append(dbc)
    #         n -= 1
    #     backup_databases(db_list, output_dir = mainFolder, user=os.getenv("user"), password=os.getenv("password"))
        
        
    if(choice == 1):
        db_list = []
            # Connect to MySQL
        conn = mysql.connector.connect(
             host="localhost",
                user=os.getenv("user"),
            password=os.getenv("password")
            )

        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")

        # Append all database names to db_list
        db_list = [db[0] for db in cursor.fetchall()]
        cursor.close()
        conn.close()
        backup_databases(db_list, output_dir = mainFolder, user=os.getenv("user"), password=os.getenv("password"))
    elif(choice == 2):
        # script(n)
        pass
    else:
        print("Wrong Choice")
        
    delete_old_backups()

    db.disconnect_from_database()


