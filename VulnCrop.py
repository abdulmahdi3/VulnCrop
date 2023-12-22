import os
import subprocess
from flask import Flask, render_template, request  

app = Flask(__name__, template_folder="templates")

def ensure_trailing_slash(target_url):
    if not target_url.endswith('/'):
        target_url += '/'
    return target_url

#####################################################################################################################
#Broken Access Control
def run_gobuster_Broken_Access_Control(target_url, url_folder): 
    ensure_trailing_slash(target_url)
    output=subprocess.check_output(["gobuster","dir","-u",target_url,"-w","/usr/local/share/wordlists/wfuzz/general/catala.txt"])
    outfile = os.path.join(url_folder,"output_gobuster.txt")
    with open(outfile,"wb") as f:
        f.write(output)
    return render_template("results.html", gobuster_output=output.decode("utf-8"))

def run_ffuf_Broken_Access_Control(target_url, url_folder):
    ensure_trailing_slash(target_url)
    output=subprocess.check_output(["ffuf","-w","/usr/local/share/wordlists/wfuzz/general/catala.txt","-u",target_url+"FUZZ","-mc","200"])
    outfile = os.path.join(url_folder,"output_ffuf.txt")
    with open(outfile,"wb") as f:
        f.write(output)
    return render_template("results.html", ffuf_output=output.decode("utf-8"))

def run_nmap_Broken_Access_Control(target_url, url_folder): 
    ensure_trailing_slash(target_url)
    output=subprocess.check_output(["nmap","-p","80,443","--script","http-enum",target_url])
    outfile = os.path.join(url_folder,"output_nmap.txt")
    with open(outfile,"wb") as f:
        f.write(output)
    return render_template("results.html", nmap_output=output.decode("utf-8"))


#####################################################################################################################
#Cross-Site Scripting(XSS)
def run_toxssin_Cross_site_scripting_XSS(target_url, url_folder):
    return "Cross-Site Scripting(XSS)"

def run_wapiti_Cross_site_scripting_XSS(target_url, url_folder):
    return "Cross-Site Scripting(XSS)"

def run_xsstrike_Cross_site_scripting_XSS(target_url, url_folder):
    xsstrike_path = os.path.join(app.root_path, "XSStrike", "xsstrike.py")
    output = subprocess.check_output(["python3", xsstrike_path, "-u", target_url, "--crawl"])
    outfile = os.path.join(url_folder, "output_xsstrike.txt")
    with open(outfile, "wb") as f:
        f.write(output)
    return render_template("results.html", xsstrike_output=output.decode("utf-8"))

#####################################################################################################################
#SQL Injection
def run_sqlmap_SQL_Injection(target_url, url_folder):
    return "SQL Injection"

def run_dsss_SQL_Injection(target_url, url_folder):
    dss_path= os.path.join(app.root_path,"DSSS","dsss.py")
    output=subprocess.check_output(["python3",dss_path, "-u",target_url, ]) #this requierd new url ending with e.g:listproducts.php?cat=1 

#####################################################################################################################
#XML External Entity (XXE)
def run_wapiti_XML_External_Entity_XXE(target_url, url_folder):
    return "XML External Entity (XXE)"

def run_xxeinjector_XML_External_Entity_XXE(target_url, url_folder):
    return "XML External Entity (XXE)"

#####################################################################################################################
#Remote File Inclusion (RFI) & Local File Inclusion (LFI)
def run_Lfiscan_Local_File_Inclusion_LFI(target_url, url_folder):
    return "Remote File Inclusion (RFI) & Local File Inclusion (LFI)"

def run_Lfispace_Local_File_Inclusion_LFI(target_url, url_folder):
    return "Remote File Inclusion (RFI) & Local File Inclusion (LFI)"

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
#Session Hijacking and Session Fixation
def run_Firesheep_Session_Hijacking_and_Session_Fixation(target_url, url_folder):
    return "Session Hijacking and Session Fixation"

def run_THC_Hydra_Session_Hijacking_and_Session_Fixation(target_url, url_folder):
    return "Session Hijacking and Session Fixation"

#####################################################################################################################
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods=["POST"])  
def results():
    target_url = request.form["target_url"]
    url_folder = os.path.join(app.root_path, "scans", target_url)
    os.makedirs(url_folder, exist_ok=True)  

    run_xsstrike_Cross_site_scripting_XSS(target_url, url_folder)
    run_gobuster_Broken_Access_Control(target_url,url_folder)
    run_ffuf_Broken_Access_Control(target_url, url_folder)
    run_nmap_Broken_Access_Control(target_url, url_folder)

    return render_template("results.html", target_url=target_url)


if __name__ == "__main__":
   app.run(debug=True, port=5000)