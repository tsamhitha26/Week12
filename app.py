from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("myForm.html")

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username", "").strip()
    return render_template("greeting.html", name=username)

if __name__ == "__main__":
    # 0.0.0.0 allows access from Docker containers.
    app.run(host="0.0.0.0", port=5000, debug=False)
