import os
import tools
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates")        

@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        return redirect(url_for('attacks_page'))
    return render_template("homepage.html")

@app.route("/attacks", methods=["GET","POST"])
def attacks_page():
    selected_attacks = request.form.getlist("attacks")
    target_url = request.form.get("target_url", "")
    
    if not target_url or not selected_attacks:
        return redirect(url_for("homepage"))

    url_folder = os.path.join(app.root_path, "scans", target_url)
    os.makedirs(url_folder, exist_ok=True)

    results = {}
    for attack in selected_attacks:
        if attack == "Broken Access Control":
            results[attack + " Gobuster"] = tools.gobuster(target_url, url_folder, selected_attacks)
            results[attack + " Katana"] = tools.katana(target_url, url_folder, selected_attacks)
            
        if attack == "Insecure Design":
            results[attack + " Dirb"] = tools.dirb(target_url, url_folder, selected_attacks)
            results[attack + " Fuff"] = tools.ffuf(target_url, url_folder, selected_attacks)

        if attack == "Cross-Site Scripting (XSS)":   
            results[attack + " Dalfox"] = tools.Dalfox(target_url, url_folder, selected_attacks)
            results[attack + " Xsstrike"] = tools.xsstrike(target_url, url_folder, selected_attacks)

        if attack == "SQL Injection":   
            results[attack + " sqlmap"] = tools.sqlmap(target_url, url_folder, selected_attacks)
        
    return render_template("results.html", selected_attacks=selected_attacks, target_url=target_url,results=results)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
