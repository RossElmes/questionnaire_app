from flask import Flask, render_template, request, redirect, url_for, flash, jsonify ,session


app = Flask(__name__,template_folder='app/templates')
app.secret_key = 'your_secret_key'

# Dummy questions (replace with your actual questions)
# Example question list
questions = [
    {"id": 1, "question": "What is your favorite color?", "answers": ["Red", "Blue", "Green", "Yellow"]},
    {"id": 2, "question": "What is your favorite animal?", "answers": ["Dog", "Cat", "Bird", "Fish"]},
    # Add more questions as needed
]


entries=[]

@app.route('/')
def index():
    return render_template('index.html', question=questions[0], question_id=0)

""" @app.route('/next', methods=['POST'])
def next_question():
    question_id = int(request.form['question_id'])
    if question_id < len(questions) - 1:
        return render_template('questionnaire.html', question=questions[question_id + 1], question_id=question_id + 1)
    else:
        return redirect(url_for('complete')) """


@app.route('/questionnaire/<int:question_id>', methods=['GET', 'POST'])
def questionnaire(question_id):
    if request.method == 'POST':
        # Save the submitted answer to the session
        submitted_answer = request.form.get('answer')
        if 'answers' not in session:
            session['answers'] = []  # Ensure there is a list to append to
        session['answers'].append(submitted_answer)
        
        # Force the session to be modified
        session.modified = True

        # Check if there are more questions
        if question_id < len(questions):
            # Go to the next question
            return redirect(url_for('questionnaire', question_id=question_id + 1))
        else:
            # No more questions, go to the results page
            return redirect(url_for('complete'))
    
    # Get the current question based on question_id
    current_question = questions[question_id - 1]  # Adjusting for 0-based index
    return render_template('questionnaire.html', question=current_question, question_id=question_id)



@app.route('/complete')
def complete():
    # Retrieve answers from the session
    answers = session.get('answers', [])
    
    # Here, you could calculate the score based on answers
    # For demonstration, just print answers to the console
    print("User's Answers:", answers)
    
    # Render the results template, passing in answers or calculated score
    return render_template('complete.html', answers=answers)

@app.route('/patient', methods=['GET', 'POST'])
def patient_details():
    if request.method == 'POST':
        # Initialize or reset the answers list in the session
        session['answers'] = []
        # Save patient details and redirect to the first question
        session['patient_details'] = request.form.to_dict()
        return redirect(url_for('questionnaire', question_id=1))
    return render_template('patient_details.html')

if __name__ == '__main__':
    app.run(debug=True)