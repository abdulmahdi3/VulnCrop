import os
import subprocess
from flask import Flask, render_template, request  

#pip install wapiti3 #usning this tool in xss and xxe

app = Flask(__name__, template_folder="templates")

def ensure_trailing_slash(target_url):
    if not target_url.endswith('/'):
        target_url += '/'
    return target_url

#####################################################################################################################
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
    ensure_trailing_slash(target_url)
    try:
        output=subprocess.check_output(["katana", "-u" ,target_url,"|","grep","?"])
        outfile = os.path.join(url_folder,"Broken_Access_katana.txt")
        with open(outfile,"wb") as f:
            f.write(output)
        return output.decode("utf-8")

    except subprocess.CalledProcessError as e:
        print("Error:", e)
        output=None            
        return output.decode("utf-8")
    pass

#####################################################################################################################
#Cross-Site Scripting(XSS)

def run_wapiti_Cross_site_scripting_XSS(target_url, url_folder):
    return "Cross-Site Scripting(XSS)"

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

#####################################################################################################################
#SQL Injection
def run_sqlmap_SQL_Injection(target_url, url_folder):
    return "SQL Injection"

def run_dsss_SQL_Injection(target_url, url_folder):
    return "SQL Injection"


#####################################################################################################################
#XML External Entity (XXE)
def run_wapiti_XML_External_Entity_XXE(target_url, url_folder):
    return "XML External Entity (XXE)"

def run_xxeinjector_XML_External_Entity_XXE(target_url, url_folder):
    return "XML External Entity (XXE)"

#####################################################################################################################
#File Upload
def run_nikto_File_upload(target_url, url_folder):
    return "File Upload"

def run_Fuxploider_File_upload(target_url, url_folder):
    return "FIle upload"

#####################################################################################################################
#Insecure design
def run_dirb_Insecure_design(target_url, url_folder):
    return "Insecure design"

def run_OWASP_Dependency_Check_Insecure_design(target_url, url_folder):
    return "Insecure design"

#####################################################################################################################
#Server-Side Request Forgery(SSRF)
def run_See_SURF_Server_Side_Request_Forgery(target_url, url_folder):
    return "Server-Side Request Forgery(SSRF)"

def run_Skipfish_Server_Side_Request_Forgery(target_url, url_folder):
    return "Server-Side Request Forgery(SSRF)"
#####################################################################################################################
#Cross-Site Request Forgery(CSRF)
def run_XSRFProbe_Cross_Site_Request_Forgery(target_url, url_folder):
    return "Server-Side Request Forgery(SSRF)"

def run_CSRFTester_Cross_Site_Request_Forgery(target_url, url_folder):
    return "Server-Side Request Forgery(SSRF)"

#####################################################################################################################


@app.route("/")
def Homepage():
    return render_template("Homepage.html")

@app.route("/results", methods=["POST"])  
def results():
    selected_attacks = request.form.getlist("attacks[]")
    target_url = request.form["target_url"]
    url_folder = os.path.join(app.root_path, "scans", target_url)
    os.makedirs(url_folder, exist_ok=True)  

    results = {}
    for attack in selected_attacks:
        if attack == "Broken Access Control":
            results[attack + " (gobuster)"] = gobuster(target_url, url_folder)
            results[attack + " (katana)"] = katana(target_url, url_folder)
        elif attack == "Cross-Site Scripting (XSS)":
            results[attack] = run_xsstrike_Cross_site_scripting_XSS(target_url, url_folder)

    return render_template("results.html", target_url=target_url, results=results)

if __name__ == "__main__":
   app.run(debug=True, port=5000)