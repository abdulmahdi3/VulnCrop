import os
import subprocess


def ensure_trailing_slash(target_url):
    if not target_url.endswith('/'):
        target_url += '/'
    return target_url

def ensure_trailing_questionmark(target_url):
    if not target_url.endswith('?'):
        target_url += '?'
    return target_url

def ensure_start_http(target_url):
    if not target_url.startswith('http://') and not target_url.startswith('https://'):
        target_url = 'http://' + target_url
    return target_url

def checkbox_checked(selected_attacks, attack_name):
    return attack_name in selected_attacks

def Sublist3r(target_url, url_folder, selected_attacks):
    if not checkbox_checked(selected_attacks, "Cross-Site Scripting (XSS)"):
        return None
    
    try:
        output = subprocess.check_output(["python3", "/Users/mahdihussnie/Desktop/VulnCrop/Sublist3r/sublist3r.py", "-d", target_url])
        outfile = os.path.join(url_folder, "Sublist3r.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
