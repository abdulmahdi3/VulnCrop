import os
import subprocess
import functions
from flask import Flask

app = Flask(__name__, template_folder="templates")


# Broken Access Control
def gobuster(target_url, url_folder, selected_attacks):
    if not functions.checkbox_checked(selected_attacks, "Broken Access Control"):
        return None

    target_url = functions.ensure_start_http(functions.ensure_trailing_slash(target_url))
    try:
        output = subprocess.check_output(["gobuster", "dir", "-u", target_url, "-w", "/usr/local/share/wordlists/dirb/catala.txt"])
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
def xsstrike(target_url, url_folder, selected_attacks):
    if not functions.checkbox_checked(selected_attacks, "Cross-Site Scripting (XSS)"):
        return None
    
    try:
        output = subprocess.check_output(["python3", "/Users/mahdihussnie/Desktop/VulnCrop/XSStrike/xsstrike.py", "-u", target_url, "--crawl"])
        outfile = os.path.join(url_folder, "XSS_xsstrike.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)

def Dalfox(target_url, url_folder, selected_attacks):
    if not functions.checkbox_checked(selected_attacks, "Cross-Site Scripting (XSS)"):
        return None

    try:
        output = subprocess.check_output(["dalfox", "url", target_url])
        outfile = os.path.join(url_folder, "XSS_Dalfox.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)

# Insecure design
def dirb(target_url, url_folder, selected_attacks):
    if not functions.checkbox_checked(selected_attacks, "Insecure Design"):
        return None

    target_url = functions.ensure_start_http(functions.ensure_trailing_slash(target_url))
    try:
        output = subprocess.check_output(["dirb", target_url,"/usr/local/share/wordlists/dirb/common.txt"])
        outfile = os.path.join(url_folder, "Insecure_Design_dirb.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)


def ffuf(target_url, url_folder, selected_attacks):
    if not functions.checkbox_checked(selected_attacks, "Insecure Design"):
        return None

    target_url = functions.ensure_start_http(functions.ensure_trailing_slash(target_url))
    try:
        output = subprocess.check_output(["ffuf", "-u", target_url + "FUZZ", "-w", "/usr/local/share/wordlists/dirb/big.txt"])
        outfile = os.path.join(url_folder, "Insecure_Design_ffuf.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)

#SQL Injection
def sqlmap(target_url, url_folder, selected_attacks):
    if not functions.checkbox_checked(selected_attacks, "SQL Injection"):
        return None

    target_url = functions.ensure_start_http(functions.ensure_trailing_slash(target_url))
    try:
        output = subprocess.check_output(["sqlmap", "-u","'"+target_url+"'"," --dbs"])
        outfile = os.path.join(url_folder, "SQL_Injection_sqlmap.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
