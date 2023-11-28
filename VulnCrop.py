import subprocess
import os
from flask import Flask, render_template, request  

app = Flask(__name__, template_folder="templates")

# Path to xsstrike script
XSSTRIKE_PATH = os.path.join(app.root_path, "XSStrike", "xsstrike.py") 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])  
def scan():

    target_url = request.form["target_url"]

    try:
        # Run XSStrike 
        output = subprocess.check_output(["python3", XSSTRIKE_PATH, "-u", target_url, "--crawl"])  
    except subprocess.CalledProcessError as e:
        # Handle errors 
        print(e.output)  
        return "XSStrike failed"

    # Save output to file
    outfile = "xsstrike_output.txt"
    with open(outfile, "wb") as f: 
        f.write(output)

    # Pass file path to template
    return render_template("results.html", output_file=outfile)

if __name__ == "__main__":
   app.run(debug=True, port=5000)
