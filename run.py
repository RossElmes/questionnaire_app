from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__,template_folder='app/templates')

# Dummy questions (replace with your actual questions)
questions = [
    "Question 1",
    "Question 2",
    # ... add more questions
]

@app.route('/')
def index():
    return render_template('index.html', question=questions[0], index=0)

@app.route('/next', methods=['POST'])
def next_question():
    index = int(request.form['index'])
    if index < len(questions) - 1:
        return render_template('index.html', question=questions[index + 1], index=index + 1)
    else:
        return redirect(url_for('complete'))

@app.route('/complete')
def complete():
    # Process answers and render the output page
    # For simplicity, just passing the questions and answers to the template
    return render_template('complete.html', questions=questions, answers=request.form,zip=zip)

if __name__ == '__main__':
    app.run(debug=True)
