import os
import subprocess
import Functions.Global_Function as Global_Function

def sqlmap(target_url, url_folder, selected_attacks):
    if not Global_Function.checkbox_checked(selected_attacks, "SQL Injection"):
        return None

    target_url = Global_Function.ensure_start_http(target_url)
    try:
        output = subprocess.check_output(["sqlmap", "-u",target_url,"--dbs","--forms","--crawl=2","--batch","--tables"])
        outfile = os.path.join(url_folder, "SQL_Injection_sqlmap.txt")
        with open(outfile, "wb") as f:
            f.write(output)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
