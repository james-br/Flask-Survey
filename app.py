from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


RESPONSE = "responses"
@app.route("/")
def home_survey():
    """ Select a Survey """
    return render_template("start.html", survey=survey)

@app.route("/begin", methods=["POST"])
def quests():
    session[RESPONSE] = []
    return redirect("/questions/0")

@app.route("/questions/<int:num>")
def show_q(num):
    """ Display a question """
    responses = session.get(RESPONSE)
    if(responses is None):
        return redirect("/")

    if(len(responses) == len(survey.questions)):
        return redirect("/complete")

    if(len(responses) != num):
        flash(f"Invalid Question number:{num}")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[num]
    return render_template("questions.html", question_num=num, question=question)

@app.route("/answer", methods=["POST"])
def take_answer():
    choice = request.form['answer']
    responses = session[RESPONSE]
    responses.append(choice)
    session[RESPONSE] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/complete")
def complete():
    return render_template("complete.html")