import os
import json

# List of DBMS names
dbms_list = [
    'MySQL', 'Oracle', 'PostgreSQL', 'Microsoft SQL Server', 'Microsoft Access',
    'IBM DB2', 'SQLite', 'Firebird', 'Sybase', 'SAP MaxDB', 'Informix', 'MariaDB',
    'Percona', 'MemSQL', 'TiDB', 'CockroachDB', 'HSQLDB', 'H2', 'MonetDB', 'Apache Derby',
    'Amazon Redshift', 'Vertica', 'Mckoi', 'Presto', 'Altibase', 'MimerSQL', 'CrateDB',
    'Greenplum', 'Drizzle', 'Apache Ignite', 'Cubrid', 'InterSystems Cache', 'IRIS',
    'eXtremeDB', 'FrontBase'
]

def Vulnerabl_potentiality_depend_on_url_and_cve(count_potentiality, count_cve):
    if count_potentiality >= 10 or count_cve >= 2:
        return "Critical"
    elif (count_potentiality >= 7 and count_potentiality <= 9) or count_cve == 1:
        return "High"
    elif count_potentiality >= 4 and count_potentiality <= 6 :
        return "Medium"
    elif count_potentiality >= 1 and count_potentiality <= 3 :
        return "Low"
    elif count_potentiality == 0 or count_cve == 0:
        return "None"

def filter_files(directory):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"): 
            file_path = os.path.join(directory, filename)
            count_301 = 0
            count_cve = 0
            line_count = 0 
            count_potentiality = 0
            count_directory = 0
            database_type = None  # Initialize variable to store the DBMS name
            with open(file_path, 'r') as file:
                for line in file:
                    if '301' in line.lower() or '301' in line.upper():
                        count_301 += 1
                        line_count += 1
                    if 'cve' in line.lower() or 'cve' in line.upper():
                        count_cve += 1
                        line_count += 1
                    if 'web application technology' in line:
                        web_technology += 1
                        line_count += 1
                    if '2k' in line.lower() or '2k' in line.upper():
                        count_potentiality += 1
                        line_count += 1
                    for dbms in dbms_list:
                        if dbms in line:
                            line_count += 1
                            database_type = dbms  
                            break  
                Severity = Vulnerabl_potentiality_depend_on_url_and_cve(count_potentiality, count_cve)
        
            if filename.endswith("katana.txt"):
                file_path = os.path.join(directory, filename)  
                with open(file_path, 'r') as katan_file:
                    for line in katan_file:
                        if 'https://' in line or 'http://' in line:
                            count_directory += 1
                            line_count += 1

            result = {
                "file": file_path,
                "directory_number" : count_directory,
                "301": count_301,
                "cve": count_cve,
                "potentiality": count_potentiality,
                "filtered_lines": line_count,
                "Severity": Severity,
                "database_type": database_type  
            }
            results.append(result)

    with open("filter.json", "w") as output_file:
        json.dump(results, output_file, indent=4)

    print("Results saved to filter.json")

filter_files('/Users/mahdihussnie/Desktop/VulnCrop/scans/https:/pentest-ground.com:81')
