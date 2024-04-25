import os
import subprocess
import Functions.Global_Function as Global_Function

def dirb(target_url, url_folder, selected_attacks):
    if not Global_Function.checkbox_checked(selected_attacks, "Insecure Design"):
        return None

    target_url = Global_Function.ensure_start_http(Global_Function.ensure_trailing_slash(target_url))
    try:
        output = subprocess.check_output(["dirb", target_url,"/usr/local/share/wordlists/dirb/common.txt"])
        outfile = os.path.join(url_folder, "Insecure_Design_dirb.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)

def ffuf(target_url, url_folder, selected_attacks):
    if not Global_Function.checkbox_checked(selected_attacks, "Insecure Design"):
        return None

    target_url = Global_Function.ensure_start_http(Global_Function.ensure_trailing_slash(target_url))
    try:
        output = subprocess.check_output(["ffuf", "-u", target_url + "FUZZ", "-w", "/usr/local/share/wordlists/dirb/big.txt"])
        outfile = os.path.join(url_folder, "Insecure_Design_ffuf.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)

def dependency_check(target_url, url_folder, selected_attacks):
    if not Global_Function.checkbox_checked(selected_attacks, "Insecure Design"):
        return None

    target_url = Global_Function.ensure_start_http(Global_Function.ensure_trailing_slash(target_url))
    file_url = subprocess.check_output(["wget" ,target_url])
    file_html = file_url + '.html'

    try:
        output = subprocess.check_output(["dependency-check", "--project","test","--scan",file_html , "--out" , "Results.html"])
        outfile = os.path.join(url_folder, "Insecure_Design_dependency_check.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)

