from flask import Flask, render_template, request, redirect, url_for, flash, jsonify ,session
import pandas as pd
import uuid as uuid
from datetime import date

app = Flask(__name__,template_folder='templates')
app.secret_key = 'your_secret_key'

answer_ref = pd.read_csv('static/data/fixmyfeet_answers_ref.csv')
question_ref = pd.read_csv('static/data/fixmyfeet_questions_ref.csv')
patient_details_table = pd.read_csv('static/data/questionnaire_patientdetails.csv')
answers_table = pd.read_csv('static/data/questionnare_answers.csv')

@app.route('/')
def index():
    session.clear()
    return render_template('index.html', question=question_ref, question_iter=0)

@app.route('/admin')
def show_results():
    # Convert the DataFrame to HTML; other parameters can customize the table appearance
    results_html = patient_details_table.to_html(classes='data', index=False, border=0,header="true")
    return render_template('admin.html', tables=results_html)


@app.route('/questionnaire/<int:question_iter>', methods=['GET', 'POST'])
def questionnaire(question_iter):
    if request.method == 'POST':
        selected_answer_value = request.form.get('answer_value')
        #print(selected_answer_value)
        # Save the submitted answer to the session
        if 'answers' not in session:
            session['answers'] = []  # Ensure there is a list to append to
        session['answers'].append(selected_answer_value)
                
        session.modified = True  # Ensure session is marked as modified
        
        if question_iter < len(question_ref):
            return redirect(url_for('questionnaire', question_iter=question_iter + 1))
        else:
            return redirect(url_for('complete'))
    
    question_text = question_ref.loc[question_ref['question_iter'] == question_iter, 'question_text'].values[0]
    answers = answer_ref[answer_ref['question_iter'] == question_iter][['answer_id', 'answer_text','answer_image']]
    return render_template('questionnaire.html', question=question_text, answers=answers.to_dict(orient='records'), question_iter=question_iter)



@app.route('/complete')
def complete():
    
    # Get today's date (only the date part, without time)
    today_date = date.today()

    # Format as a string
    date_string = today_date.strftime("%Y-%m-%d")
    
    # Retrieve answers from the session
    answers = session.get('answers', [])
    patient_details = session.get('patient_details', [])
    
    #Create a df from the answers
    selected_answers_df = pd.DataFrame(answers, columns=['answer_id'])
    # Join the answers back to the answer reference
    merged_df = selected_answers_df.merge(answer_ref, on='answer_id', how='inner')
    
    # Calcualte the score.  Addtion and Multply logic 
    multiply_df = merged_df[merged_df['logic'] == 'multiply']
    addition_df = merged_df[merged_df['logic'] == 'addition']
    
    # Calculate a score
    score = multiply_df['answer_value'].prod() * addition_df['answer_value'].sum()
    # Pull the answers
    answer_text = merged_df['answer_text']
    
    # Create a results with an id for the patient and tie to the answes
    questionnaire_unique_id = uuid.uuid4()
    
    ## Patient Details Df
    patient_details_df = pd.DataFrame({
    'Patient_Name': patient_details.get('patientName'),
    'Patient_Email': patient_details.get('patientEmail'),
    'questionnaire_unique_id':questionnaire_unique_id,
    'complete_date':date_string
    # add as many columns as you have
    },index=[0])
    
    ## Tie it to the answers
    merged_df['questionnaire_unique_id'] = questionnaire_unique_id
    
    ## Join new patient details to history
    frames = [patient_details_table,patient_details_df]
    patient_details_df_new = pd.concat(frames)
    ## Join new answers to history
    frames = [answers_table,merged_df]
    merged_df_new = pd.concat(frames)
    
    
    ## Write the answers to the results table 
    patient_details_df_new.to_csv('static/data/questionnaire_patientdetails.csv',index=False)
    merged_df_new.to_csv('static/data/questionnare_answers.csv',index=False)
    
         
    # Render the results template, passing in answers or calculated score
    return render_template('complete.html', answers=answer_text,score=score,patient_details=patient_details)


@app.route('/patient', methods=['GET', 'POST'])
def patient_details():
    if request.method == 'POST':
        # Initialize or reset the answers list in the session
        session['answers'] = []
        # Save patient details and redirect to the first question
        session['patient_details'] = request.form.to_dict()
        return redirect(url_for('questionnaire', question_iter=1))
    return render_template('patient_details.html')

if __name__ == '__main__':
    app.run()