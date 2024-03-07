import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates")

def ensure_trailing_slash(target_url):
    if not target_url.endswith('/'):
        target_url += '/'
    return target_url

#Broken Access Control
def gobuster(target_url, url_folder): 
    ensure_trailing_slash(target_url)
    try:
        output=subprocess.check_output(["gobuster","dir","-u",target_url,"-w","/Users/mahdihussnie/Desktop/VulnCrop/wordlists/wfuzz/general/catala.txt"])
        outfile = os.path.join(url_folder,"Broken_Access_gobuster.txt")
        with open(outfile,"wb") as f:
            f.write(output)
        return output.decode("utf-8")

    except subprocess.CalledProcessError as e:
        print("Error:", e)
        output=None            
        return output.decode("utf-8")
    pass
    

def katana(target_url, url_folder):
    target_url = ensure_trailing_slash(target_url)
    try:
        output = subprocess.check_output(["katana", "-u", target_url, "|", "grep", "?"])
        outfile = os.path.join(url_folder, "Broken_Access_katana.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        output = None
        return output.decode("utf-8") if output else None

#Cross-Site Scripting(XSS)

def run_xsstrike_Cross_site_scripting_XSS(target_url, url_folder):
    xsstrike_path = os.path.join(app.root_path, "XSStrike", "xsstrike.py")
    try:
        output=subprocess.check_output(["python3", xsstrike_path, "-u", target_url, "--crawl"])
        outfile = os.path.join(url_folder, "XSS_xsstrike.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        output=None            
        return output.decode("utf-8")
    pass


@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        return redirect(url_for('attacks_page'))
    return render_template("Homepage.html")

@app.route("/attacks", methods=["GET", "POST"])
def attacks_page():
    if request.method == "POST":
        selected_attacks = request.form.getlist("attacks")
        target_url = request.form.get("target_url", "")
        
        if not target_url or not selected_attacks:
            return redirect(url_for("homepage"))

        url_folder = os.path.join(app.root_path, "scans", target_url)
        os.makedirs(url_folder, exist_ok=True)

        results = {}
        for attack in selected_attacks:
            if attack == "Broken Access Control":
                # Call the appropriate function for each selected attack
                results[attack + " (gobuster)"] = gobuster(target_url, url_folder)
                results[attack + " (katana)"] = katana(target_url, url_folder)
            elif attack == "Cross-Site Scripting (XSS)":
                results[attack] = run_xsstrike_Cross_site_scripting_XSS(target_url, url_folder)
            # Add more elif conditions for other attacks if needed

        return render_template("results.html", target_url=target_url, results=results)
    
    return render_template("attacks.html")

if __name__ == "__main__":
   app.run(debug=True, port=5000)