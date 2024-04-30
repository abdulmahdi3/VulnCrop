import json
import os, time
import Functions.broken_access_tools ,Functions.xss_tools ,Functions.inscure_design_tools,Functions.sql_tools, Functions.xxe_tools ,Functions.filters
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates")        

@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        return redirect(url_for('attacks_page'))
    return render_template("homepage.html")

@app.route('/visualisation', methods=['GET', 'POST'])
def index(directory_to_scan):
    # Read the contents of filter.json
    with open('filter.json', 'r') as f:
        data = json.load(f)

    # Process the data as needed
    payloads = sum(entry['filtered_lines'] for entry in data)
    tools_executed = len(data)
    potentiality = sum(entry['potentiality'] for entry in data)

    # Determine the site_state based on the severity
    site_state = 'vulnerable' if any(entry['Severity'] == 'Low' or entry['Severity'] == 'Medium' or entry['Severity'] == 'High' or entry['Severity'] == 'Critical' for entry in data) else 'secure'
    doughnutChart_Low = sum(entry['Severity'] == 'Low' for entry in data)
    doughnutChart_Medium = sum(entry['Severity'] == 'Medium' for entry in data)
    doughnutChart_High = sum(entry['Severity'] == 'High' and entry['Severity'] == 'Critical' for entry in data)

    data_json = json.dumps(data)
    Functions.filters.filter_files(directory_to_scan)
    return render_template('index.html', data_json=data_json,doughnutChart_Low=doughnutChart_Low,doughnutChart_Medium=doughnutChart_Medium,doughnutChart_High=doughnutChart_High,data=data, payloads=payloads, tools_executed=tools_executed, potentiality=potentiality, site_state=site_state)


@app.route("/attacks", methods=["GET","POST"])
def attacks_page():
    start_time = time.time() 
    selected_attacks = request.form.getlist("attacks")
    target_url = request.form.get("target_url", "")
    if not target_url or not selected_attacks:
        return redirect(url_for("homepage"))
    url_folder = os.path.join(app.root_path, "scans", target_url)
    os.makedirs(url_folder, exist_ok=True)
    results = {}
    timing_data = {}
    for attack in selected_attacks:
        attack_start_time = time.time()  
        if attack == "Broken Access Control":
            results[attack + " Gobuster"] = Functions.broken_access_tools.gobuster(target_url, url_folder, selected_attacks)
            results[attack + " Katana"] = Functions.broken_access_tools.katana(target_url, url_folder, selected_attacks)
        if attack == "Cross-Site Scripting (XSS)":
            # results[attack + " Dalfox"] = Functions.xss_tools.Dalfox(target_url, url_folder, selected_attacks)
            results[attack + " xsstrike"] = Functions.xss_tools.xsstrike(target_url, url_folder, selected_attacks)
        if attack == "SQL Injection":
            results[attack + " sqlmap"] = Functions.sql_tools.sqlmap(target_url, url_folder, selected_attacks)
        if attack == "XML External Entity (XXE)":
            results[attack + " wapiti"] = Functions.xxe_tools.wapiti(target_url, url_folder, selected_attacks)
        if attack == "Insecure Design":
            results[attack + " Dirb"] = Functions.inscure_design_tools.dirb(target_url, url_folder, selected_attacks)
            results[attack + " Fuff"] = Functions.inscure_design_tools.ffuf(target_url, url_folder, selected_attacks)
            # results[attack + " Dependency-Check"] = Functions.inscure_design_tools.dependency_check(target_url, url_folder, selected_attacks)
        attack_end_time = time.time()
        attack_duration = attack_end_time - attack_start_time
        print(f"{attack} processing time: {attack_duration:.2f} seconds")

    end_time = time.time()
    total_duration = end_time - start_time
    timing_data["Total"] = total_duration
    if total_duration >= 60:
        minutes = total_duration // 60
        seconds = total_duration % 60
        print(f"Total processing time: {minutes} minutes and {seconds:.2f} seconds")
    else:
        print(f"Total processing time: {total_duration:.2f} seconds")

    render_template("results.html", selected_attacks=selected_attacks, target_url=target_url, results=results, timing_data=timing_data)
    return index(url_folder)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
