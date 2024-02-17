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
def run_gobuster_Broken_Access_Control(target_url, url_folder): 
    ensure_trailing_slash(target_url)
    output=subprocess.check_output(["gobuster","dir","-u",target_url,"-w","/Users/mahdihussnie/Desktop/VulnCrop/wordlists/wfuzz/general/catala.txt"])
    outfile = os.path.join(url_folder,"Broken_Access_gobuster.txt")
    with open(outfile,"wb") as f:
        f.write(output)
    return output.decode("utf-8")

def run_ffuf_Broken_Access_Control(target_url, url_folder):
    ensure_trailing_slash(target_url)
    output=subprocess.check_output(["ffuf","-w","/Users/mahdihussnie/Desktop/VulnCrop/wordlists/wfuzz/general/catala.txt","-u",target_url+"FUZZ","-mc","200"])
    outfile = os.path.join(url_folder,"Broken_Access_ffuf.txt")
    with open(outfile,"wb") as f:
        f.write(output)
    return output.decode("utf-8")

def run_nmap_Broken_Access_Control(target_url, url_folder): 
    ensure_trailing_slash(target_url)
    output=subprocess.check_output(["nmap","-sV","--script","http-enum","-p80,443",target_url])
    outfile = os.path.join(url_folder,"Broken_Access_nmap.txt")
    with open(outfile,"wb") as f:
        f.write(output)
    return output.decode("utf-8")

def katana_Broken_Access_Control(target_url, url_folder): 
    ensure_trailing_slash(target_url)
    output=subprocess.check_output(["katana", "-u" ,target_url,"|","grep","?"])
    outfile = os.path.join(url_folder,"Broken_Access_katana.txt")
    with open(outfile,"wb") as f:
        f.write(output)
    return output.decode("utf-8")


#####################################################################################################################
#Cross-Site Scripting(XSS)

def run_wapiti_Cross_site_scripting_XSS(target_url, url_folder):
    return "Cross-Site Scripting(XSS)"

def run_xsstrike_Cross_site_scripting_XSS(target_url, url_folder):
    xsstrike_path = os.path.join(app.root_path, "XSStrike", "xsstrike.py")
    output = subprocess.check_output(["python3", xsstrike_path, "-u", target_url, "--crawl"])
    outfile = os.path.join(url_folder, "XSS_xsstrike.txt")
    with open(outfile, "wb") as f:
        f.write(output)
    return output.decode("utf-8")

#####################################################################################################################
#SQL Injection
def run_sqlmap_SQL_Injection(target_url, url_folder):
    return "SQL Injection"

def run_dsss_SQL_Injection(target_url, url_folder):
    dsss_path= os.path.join(app.root_path,"DSSS","dsss.py")
    output=subprocess.check_output(["python3",dsss_path, "-u","https://alfeker.net/library.php?catid=95"]) #this requierd new url ending with e.g:listproducts.php?cat=1 so we will put the result of katana here and test all the directoryes
    outfile = os.path.join(url_folder, "SQL_injection_dsss.txt")
    with open(outfile, "wb") as f:
        f.write(output)
    return output.decode("utf-8")

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

    #broken access control
    gobuster_output = run_gobuster_Broken_Access_Control(target_url, url_folder)
    nmap_output = run_nmap_Broken_Access_Control(target_url, url_folder)
    ffuf_output = run_ffuf_Broken_Access_Control(target_url, url_folder)
    katana_output=katana_Broken_Access_Control(target_url, url_folder)

    #XSS
    xsstrike_output = run_xsstrike_Cross_site_scripting_XSS(target_url, url_folder)

    #SQL injection
    # dsss_output=run_dsss_SQL_Injection(target_url, url_folder)

    return render_template("results.html", target_url=target_url, katana_output=katana_output,gobuster_output=gobuster_output,ffuf_output=ffuf_output, nmap_output=nmap_output, xsstrike_output=xsstrike_output)#dsss_output=dsss_output

if __name__ == "__main__":
   app.run(debug=True, port=5000)