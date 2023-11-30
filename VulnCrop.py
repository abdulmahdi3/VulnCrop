import os
import subprocess
from flask import Flask, render_template, request  

app = Flask(__name__, template_folder="templates")

# Function to run XSStrike
def run_xss_strike(target_url, url_folder):
    xsstrike_path = os.path.join(app.root_path, "XSStrike", "xsstrike.py")
    output = subprocess.check_output(["python3", xsstrike_path, "-u", target_url, "--crawl"])
    outfile = os.path.join(url_folder, "output_xss_strike.txt")
    with open(outfile, "wb") as f:
        f.write(output)
    return render_template("results.html", xsstrike_output=output.decode("utf-8"))


# Function to run SQL Injection tool
def run_sql_injection(target_url, url_folder):
    # Add code to run SQL Injection tool and save output to a file inside the URL folder
    pass  # Placeholder for SQL Injection tool execution


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods=["POST"])  
def results():
    target_url = request.form["target_url"]
    url_folder = os.path.join(app.root_path, "scans", target_url)
    os.makedirs(url_folder, exist_ok=True)  # Create a folder for the scanned URL if it doesn't exist

    # Run each security tool function for the scanned URL
    run_xss_strike(target_url, url_folder)
    run_sql_injection(target_url, url_folder)
    # Call functions for other security tools in a similar manner

    return render_template("results.html", target_url=target_url)


if __name__ == "__main__":
   app.run(debug=True, port=5000)