import os
import subprocess
import Functions.Global_Function as Global_Function

def wapiti(target_url, url_folder, selected_attacks):
    if not Global_Function.checkbox_checked(selected_attacks, "XML External Entity (XXE)"):
        return None
    
    try:
        output = subprocess.check_output(["python3", "/Users/mahdihussnie/Desktop/VulnCrop/wapiti/bin/wapiti", "-u", target_url, "-m", "xxe"])
        outfile = os.path.join(url_folder, "XXE_wapiti.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
