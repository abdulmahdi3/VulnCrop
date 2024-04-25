import os, time
import Functions.broken_access_tools ,Functions.xss_tools ,Functions.inscure_design_tools,Functions.sql_tools
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates")        

@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        return redirect(url_for('attacks_page'))
    return render_template("homepage.html")

@app.route("/attacks", methods=["GET","POST"])
def attacks_page():
    start_time = time.time()  # Start the timer
    selected_attacks = request.form.getlist("attacks")
    target_url = request.form.get("target_url", "")
    if not target_url or not selected_attacks:
        return redirect(url_for("homepage"))
    url_folder = os.path.join(app.root_path, "scans", target_url)
    os.makedirs(url_folder, exist_ok=True)
    results = {}
    timing_data = {}
    for attack in selected_attacks:
        attack_start_time = time.time()  # Start the timer for each attack
        if attack == "Broken Access Control":
            results[attack + " Gobuster"] = Functions.broken_access_tools.gobuster(target_url, url_folder, selected_attacks)
            results[attack + " Katana"] = Functions.broken_access_tools.katana(target_url, url_folder, selected_attacks)
        if attack == "Insecure Design":
            results[attack + " Dirb"] = Functions.inscure_design_tools.dirb(target_url, url_folder, selected_attacks)
            results[attack + " Fuff"] = Functions.inscure_design_tools.ffuf(target_url, url_folder, selected_attacks)
            # results[attack + " Dependency-Check"] = Functions.inscure_design_tools.dependency_check(target_url, url_folder, selected_attacks)
        if attack == "Cross-Site Scripting (XSS)":
            # results[attack + " Dalfox"] = Functions.xss_tools.Dalfox(target_url, url_folder, selected_attacks)
            results[attack + " xsstrike"] = Functions.xss_tools.xsstrike(target_url, url_folder, selected_attacks)
        if attack == "SQL Injection":
            results[attack + " sqlmap"] = Functions.sql_tools.sqlmap(target_url, url_folder, selected_attacks)
        attack_end_time = time.time()  # End the timer for each attack
        attack_duration = attack_end_time - attack_start_time
        print(f"{attack} processing time: {attack_duration:.2f} seconds")

    end_time = time.time()
    total_duration = end_time - start_time
    timing_data["Total"] = total_duration
    print(f"Total processing time: {total_duration % 60:.2f} seconds")

    return render_template("results.html", selected_attacks=selected_attacks, target_url=target_url, results=results, timing_data=timing_data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
