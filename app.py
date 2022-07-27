from flask import Flask,request, render_template , redirect , flash ,jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickensRcool"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)


responses=[]

@app.route('/')
def show_start_survey():
    return render_template('survey.html', survey = survey)

@app.route('/begin', methods=['POST'])
def start_survey():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/answer',methods=['POST'])
def handle_question():
    choice = request.form['answer']

    responses = session['responses'] 
    responses.append(choice)
    session['responses'] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/questions/<int:id>')
def show_question(id):
    responses = session.get('responses')
    if (responses is None):
        return redirect('/')

    question = survey.questions[id]
    if(len(responses) != id):
        flash(f'Invalid Question ID:{id} ','error')
        return redirect(f'/questions/{len(responses)}')
        
    return render_template('question.html', question_num = id, question=question)

@app.route('/complete')
def complete():
    return render_template('completion.html')