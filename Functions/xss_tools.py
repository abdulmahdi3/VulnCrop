import os
import subprocess
import Functions.Global_Function as Global_Function

def xsstrike(target_url, url_folder, selected_attacks):
    if not Global_Function.checkbox_checked(selected_attacks, "Cross-Site Scripting (XSS)"):
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
    if not Global_Function.checkbox_checked(selected_attacks, "Cross-Site Scripting (XSS)"):
        return None
    
    target_url = Global_Function.ensure_start_http(Global_Function.ensure_trailing_questionmark(Global_Function.ensure_trailing_slash(target_url)))
    try:
        output = subprocess.check_output(["dalfox", "url", target_url])
        outfile = os.path.join(url_folder, "XSS_Dalfox.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
