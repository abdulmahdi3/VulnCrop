import os
import subprocess
import json


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

def Sublist3r(target_url, url_folder):
    try:
        output = subprocess.check_output(["python3", "/Users/mahdihussnie/Desktop/VulnCrop/Sublist3r/sublist3r.py", "-d", target_url])
        outfile = os.path.join(url_folder, "Sublist3r.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)

# def web_tech(target_url):
#     try:
#         output = subprocess.check_output(["node", "/Users/mahdihussnie/Desktop/VulnCrop/wappalyzer/src/drivers/npm/cli.js", target_url])
#         outfile = os.path.join("/Users/mahdihussnie/Desktop/VulnCrop/web_tech.json")
#         with open(outfile, "wb") as f:
#             f.write(output)
#         return output.decode("utf-8")
#     except subprocess.CalledProcessError as e:
#         print("Error:", e)

def web_tech(target_url):
    try:
        output = subprocess.check_output(["node", "/Users/mahdihussnie/Desktop/VulnCrop/wappalyzer/src/drivers/npm/cli.js", target_url])
        output_str = output.decode("utf-8")
        output_json = json.loads(output_str)
        outfile = "/Users/mahdihussnie/Desktop/VulnCrop/web_tech.json"
        with open(outfile, "w") as f:
            json.dump(output_json, f, indent=4)
        return output_json
    except subprocess.CalledProcessError as e:
        print("Error:", e)
