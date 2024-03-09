import functions
import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates")


# Broken Access Control
def gobuster(target_url, url_folder, selected_attacks):
    if not functions.checkbox_checked(selected_attacks, "Broken Access Control"):
        return None

    target_url = functions.ensure_start_http(functions.ensure_trailing_slash(target_url))
    try:
        output = subprocess.check_output(["gobuster", "dir", "-u", target_url, "-w", "/Users/mahdihussnie/Desktop/VulnCrop/wordlists/fasttrack.txt"])
        outfile = os.path.join(url_folder, "Broken_Access_gobuster.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        

def katana(target_url, url_folder, selected_attacks):
    if not functions.checkbox_checked(selected_attacks, "Broken Access Control"):
        return None

    target_url = functions.ensure_start_http(functions.ensure_trailing_slash(target_url))
    try:
        output = subprocess.check_output(["katana", "-u", target_url])
        outfile = os.path.join(url_folder, "Broken_Access_katana.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        

# Cross-Site Scripting (XSS)
def xsstrike(target_url, url_folder,selected_attacks):
    if not functions.checkbox_checked(selected_attacks, "Cross-Site Scripting (XSS)"):
        return None
    
    target_url = functions.ensure_start_http(functions.ensure_trailing_slash(target_url))
    xsstrike_path = os.path.join(app.root_path, "XSStrike", "xsstrike.py")
    try:
        output = subprocess.check_output(["python3", xsstrike_path, "-u", target_url, "--crawl"])
        outfile = os.path.join(url_folder, "XSS_xsstrike.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        

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
            results[attack + " gobuster"] = gobuster(target_url, url_folder, selected_attacks)
            results[attack + " katana"] = katana(target_url, url_folder, selected_attacks)
            
        if attack == "Cross-Site Scripting (XSS)":
            results[attack + " xsstrike"] = xsstrike(target_url, url_folder, selected_attacks)

    return render_template("results.html", selected_attacks=selected_attacks, target_url=target_url,results=results)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
