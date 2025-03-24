import os
import pyodbc
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time

finalduration = '02:10:00'
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\USER\Documents\Channel1\MultiCasterDatabase.mdb;'
)
con = pyodbc.connect(conn_str)
cur = con.cursor()
query = f"SELECT MAX(scheduleid) FROM Schedule;"
cur.execute(query)
row_count = cur.fetchone()[0]

# Read data from the Notepad file
notepad_file_path = r"C:\Users\USER\Documents\Channel1\list.txt"  # Replace with your actual file path
with open(notepad_file_path, "r") as notepad_file:
    lines = notepad_file.readlines()

# Iterate over each line in the Notepad file
for line in lines:
    # Split the line into parts
    parts = line.strip().split(',')

    # Extract data from parts
    folder_path = parts[0]
    input_date_str = parts[1]
    time_slot_str = parts[2]

    # Convert date and time strings to datetime objects
    try:
        input_date = datetime.strptime(input_date_str, "%d %b %Y")
        time_slot = datetime.strptime(time_slot_str, "%I:%M:%S %p").strftime("%H:%M:%S")
    except ValueError:
        print("Invalid date or time format in the Notepad file.")
        exit()

    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.xml', '.txt')):
            file_path = os.path.join(folder_path, filename)

            # Attempt to parse the XML file
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Your existing code for parsing duration...
                for child in root:
                    if child.tag == 'file':
                        for file_child in child:
                            if file_child.tag == 'info':
                                duration = file_child.get('duration')
                                duration_seconds = float(duration)
                                finalduration = time.strftime("%H:%M:%S", time.gmtime(duration_seconds))

            except ET.ParseError as e:
                print(f"Error parsing XML file {filename}: {e}")
                finalduration = '02:10:00'  # Set to default value in case of an error

            file_name = os.path.splitext(filename)[0]
            row_count += 1
            formatted_date = input_date.strftime("%d %b %Y")
            print(finalduration)

            cur.execute("INSERT INTO Schedule VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (row_count, time_slot, formatted_date, file_name, file_path, finalduration, 1, False))
            con.commit()
            input_date += timedelta(days=1)
