import json

def analyze_json_files():
    with open('/Users/mahdihussnie/Desktop/VulnCrop/filter.json', 'r') as f:
        data = json.load(f)

    totals = {
        "file": 0,
        "directory_number": 0,
        "301": 0,
        "cve": 0,
        "potentiality": 0,
        "filtered_lines": 0,
        "Severity": 0,
        "database_type": 0,
        "informations": 0,
        "infos_details": 0
    }
    
    for item in data:
        for key in totals.keys():
            if item[key] is not None and item[key] != 0:
                totals[key] += 1
    
    return totals

