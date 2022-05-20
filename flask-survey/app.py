from flask import Flask, request, render_template, redirect, flash, jsonify, url_for
from surveys import Question, Survey

from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

satisfaction_survey = Survey(
    "Customer Satisfaction Survey",
    "Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?"),
        Question("Did someone else shop with you today?"),
        Question("On average, how much do you spend a month on frisbees?",
                 ["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?"),
    ])

personality_quiz = Survey(
    "Rithm Personality Test",
    "Learn more about yourself with our personality quiz!",
    [
        Question("Do you ever dream about code?"),
        Question("Do you ever have nightmares about code?"),
        Question("Do you prefer porcupines or hedgehogs?",
                 ["Porcupines", "Hedgehogs"]),
        Question("Which is the worst function name, and why?",
                 ["do_stuff()", "run_me()", "wtf()"],
                 allow_text=True),
    ]
)

surveys = {
    "satisfaction": satisfaction_survey,
    "personality": personality_quiz,
}

responses = []

@app.route('/')
def show_survey():
    satisfaction_title = satisfaction_survey.title
    satisfaction_instructions = satisfaction_survey.instructions
    
    return render_template("welcome.html",satisfaction_title=satisfaction_title,satisfaction_instructions=satisfaction_instructions)

@app.route('/questions/<question_num>')
def show_question(question_num):
    question_integer = int(question_num)
    if question_integer >= len(satisfaction_survey.questions):
        flash("Invalid question number")
        return redirect(url_for('show_question',question_num=len(responses)))
    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/thanks")
    the_question = satisfaction_survey.questions[int(question_num)].question
    the_choices = satisfaction_survey.questions[int(question_num)].choices #is either None or a list of questions
    allows_text_response = satisfaction_survey.questions[int(question_num)].allow_text #a boolean
    question_integer = int(question_num)

    if question_integer > len(responses):
        flash("Questions must be completed in order")
        return redirect(url_for('show_question',question_num=len(responses)))
    
    return render_template("question.html",the_question=the_question,the_choices=the_choices,allows_text_response=allows_text_response, question_num=question_num)

@app.route('/answer',methods=['POST','GET'])
def record_answer():
    ans= request.form['answer']
    num = request.form.get("question_num","")
    num_int = int(num)
    next_num = int(num)+1
    num_str = str(next_num)
    responses.append(ans)
    if num_int == len(satisfaction_survey.questions)-1:
        return redirect("/thanks")
    if int(num) < len(satisfaction_survey.questions):
        return redirect(url_for('show_question',question_num=num_str))
   

@app.route('/thanks')
def thank_you():
    return render_template('/thanks.html')
    



