import os
import re
import chardet
from lxml import etree
import shutil

# Specify the folder containing the text files
folder_path = r"C:\Users\HD HARIKA\Pictures\Gms"
# Step 1: Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Only process .txt files
    if filename.endswith(('.xml', '.txt')):
        file_path = os.path.join(folder_path, filename)

        # Step 2: Detect the encoding of the file using chardet
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
        print(encoding)

        # Step 3: Backup the original file before making changes
        #backup_file_path = file_path + ".bak"
        #shutil.copy2(file_path, backup_file_path)
        #print(f"Backup created for {filename}: {backup_file_path}")

        # Read XML data
        with open(file_path, 'r', encoding=encoding) as file:
            xml_data = file.read()

        # Step 4: Remove any null characters or non-printable characters
        xml_data = re.sub(r'[\x00-\x1F\x7F]', '', xml_data)

        # Step 5: Parse the cleaned XML data
        try:
            root = etree.fromstring(xml_data)

            # Example usage: Print root tag to verify parsing
            print(f"Processing file: {filename}, Root tag: {root.tag}")

            # Modify XML based on condition (FileSubName is empty)
            for mitem in root.findall(".//file/mitem_props"):
                if mitem.get("FileSubName") == '':
                    mitem.set("AutoDelete", "true")
                    file_name = mitem.get("FileName")
                    if file_name:
                        mitem.set("ScheduleName", file_name)

            # Step 6: Convert XML back to string and replace double quotes with single quotes
            xml_str = etree.tostring(root, pretty_print=True, encoding='unicode')
            # Replace double quotes with single quotes for attribute values
            #xml_str = xml_str.replace('"', "'")

            # Step 7: Save changes back to the file with single quotes for attributes
            with open(file_path, 'w', encoding=encoding) as file:
                file.write(xml_str)

            print(f"Attributes appended successfully in file: {filename}")

        except etree.XMLSyntaxError as e:
            print(f"XML syntax error in file {filename}: {e}")
            # If XML is invalid, restore the backup file
            #print(f"Restoring backup from {backup_file_path}")
            #shutil.copy2(backup_file_path, file_path)

