from flask import Flask, render_template, request, redirect, url_for, flash, jsonify ,session
import pandas as pd
import uuid as uuid

app = Flask(__name__,template_folder='templates')
app.secret_key = 'your_secret_key'

answer_ref = pd.read_csv('static/fixmyfeet_answers_ref.csv')
question_ref = pd.read_csv('static/fixmyfeet_questions_ref.csv')
patient_details_table = pd.read_csv('static/questionnaire_patientdetails.csv')
answers_table = pd.read_csv('static/questionnare_answers.csv')

print(patient_details_table)
print(answers_table)


@app.route('/')
def index():
    session.clear()
    return render_template('index.html', question=question_ref, question_iter=0)


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
    answers = answer_ref[answer_ref['question_iter'] == question_iter][['answer_id', 'answer_text']]
    return render_template('questionnaire.html', question=question_text, answers=answers.to_dict(orient='records'), question_iter=question_iter)



@app.route('/complete')
def complete():
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
    'Patient_Age': patient_details.get('patientAge'),
    'Patient_Gender':patient_details.get('patientGender'),
    'questionnaire_unique_id':questionnaire_unique_id
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
    patient_details_df_new.to_csv('static/questionnaire_patientdetails.csv',index=False)
    merged_df_new.to_csv('static/questionnare_answers.csv',index=False)
    
         
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
    app.run(debug=True)