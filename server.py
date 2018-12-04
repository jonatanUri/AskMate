from flask import Flask, render_template, redirect
import data_manager

app = Flask(__name__)

@app.route('/')
def mainpage():
    questions_dict = data_manager.csv_read_question()
    return render_template("index.html", questions_dict=questions_dict)


if __name__ == "__main__":
    app.run()
