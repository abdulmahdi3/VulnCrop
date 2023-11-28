from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__,template_folder='templates')

@app.route("/") 
def index():
    return render_template("index.html")

@app.route("/run_scan", methods=["POST"])
def run_scan():
    target = request.form["target"]
    
    # List of scanning tools 
    tools = ["nmap", "nikto", "wpscan"]
    
    # Run scans and save output
    outputs = {}
    for tool in tools:
        output = subprocess.check_output([tool, target])
        outfile = f"{tool}_output.txt"
        with open(outfile, "wb") as f:
            f.write(output)
        outputs[tool] = outfile
        
    # Render results page  
    return render_template("results.html", outputs=outputs)

if __name__ == "__main__":
    app.run(port=8000,debug=True)
