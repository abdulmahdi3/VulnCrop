import functions
import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates")


# Broken Access Control
def gobuster(target_url, url_folder, selected_attacks):
    if not functions.checkbox_checked(selected_attacks, "Broken Access Control"):
        return None

    functions.ensure_trailing_slash(target_url)
    try:
        output = subprocess.check_output(["gobuster", "dir", "-u", target_url, "-w", "/Users/mahdihussnie/Desktop/VulnCrop/wordlists/wfuzz/general/catala.txt"])
        outfile = os.path.join(url_folder, "Broken_Access_gobuster.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

def katana(target_url, url_folder, selected_attacks):
    if not functions.checkbox_checked(selected_attacks, "Broken Access Control"):
        return None

    target_url = functions.ensure_trailing_slash(target_url)
    try:
        output = subprocess.check_output(["katana", "-u", target_url, "|", "grep", "?"])
        outfile = os.path.join(url_folder, "Broken_Access_katana.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

# Cross-Site Scripting (XSS)
def xsstrike(target_url, url_folder,selected_attacks):
    if not functions.checkbox_checked(selected_attacks, "Cross-Site Scripting (XSS)"):
        return None
    xsstrike_path = os.path.join(app.root_path, "XSStrike", "xsstrike.py")
    try:
        output = subprocess.check_output(["python3", xsstrike_path, "-u", target_url, "--crawl"])
        outfile = os.path.join(url_folder, "XSS_xsstrike.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        return redirect(url_for('attacks_page'))
    return render_template("Homepage.html")

@app.route("/attacks", methods=["POST"])
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
            results[attack + " (gobuster)"] = (gobuster(target_url, url_folder, selected_attacks),)  # Wrap the output in a tuple
            results[attack + " (katana)"] = (katana(target_url, url_folder, selected_attacks),)  # Wrap the output in a tuple
        elif attack == "Cross-Site Scripting (XSS)":
            output = xsstrike(target_url, url_folder, selected_attacks)
            results[attack + " (xsstrike)"] = (output,) if output is not None else ("Error: Failed to execute XSS scan",)  # Wrap the output in a tuple
        else:
            results[attack] = ("Error: Unknown attack",)  # Wrap the error message in a tuple

    return render_template("results.html", target_url=target_url, results=results)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
