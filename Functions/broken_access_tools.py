import os
import subprocess
import Functions.Global_Function as Global_Function

def katana(target_url, url_folder, selected_attacks):
    if not Global_Function.checkbox_checked(selected_attacks, "Broken Access Control"):
        return None

    target_url = Global_Function.ensure_start_http(Global_Function.ensure_trailing_slash(target_url))
    try:
        output = subprocess.check_output(["katana", "-u", target_url])
        outfile = os.path.join(url_folder, "Broken_Access_katana.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)

def gobuster(target_url, url_folder, selected_attacks):
    if not Global_Function.checkbox_checked(selected_attacks, "Broken Access Control"):
        return None

    target_url = Global_Function.ensure_start_http(Global_Function.ensure_trailing_slash(target_url))
    try:
        output = subprocess.check_output(["gobuster", "dir", "-u", target_url, "-w", "/usr/local/share/wordlists/dirb/catala.txt"])
        outfile = os.path.join(url_folder, "Broken_Access_gobuster.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)