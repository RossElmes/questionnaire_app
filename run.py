from flask import Flask, render_template, request, redirect, url_for, flash, jsonify ,session
import pandas as pd



app = Flask(__name__,template_folder='templates')
app.secret_key = 'your_secret_key'

answer_ref = pd.read_csv('static/fixmyfeet_answers_ref.csv')
question_ref = pd.read_csv('static/fixmyfeet_questions_ref.csv')
 
# Dummy questions (replace with your actual questions)
# Example question list
questions = [
  { "id": 1,
    "question": 'What is your gender?',
    "options": [
        {"text":'Male',"value":1},
        {"text":'Female',"value":1}, 
        {"text":'Prefer not to Answer',"value":1}
    ],
  },
  {
    'id': 2,
    "question": 'What is yor age',
    "options": [{"text":'Under 12',"value":6}, 
    {"text":'12-19',"value":5}, 
    {"text":'20-29',"value":5}, 
    {"text":'30-39',"value":4},
    {"text":'40-49',"value":4},
    {"text":'50-59',"value":3},
    {"text":'60-69',"value":2},
    {"text":'70-79',"value":1},
    {"text":'80+',"value":1}],
  },
  {
    "id": 3,
    "question": 'Are you a member of VHI?',
    "options": [
        {"text":'Yes',"value":0},
        {"text":'No',"value":0},
    ]
  },
  {
    "id": 4,
    "question": 'Which of the following best describes your current occupation?',
    "options": [
        {"text":'Office Work',"value":6},
        {"text":'Retail/Hospitality/Duty Manager',"value":5},
        {"text":'Construction/Maintenance/Electriction/Plumber',"value":4},
        {"text":'Teacher/Education',"value":3},
        {"text":'Healthcare support/Nurse/Doctor/Front Line Worker',"value":3},
        {"text":'Student',"value":1},
        {"text":'Leisure/Fitness Instructor',"value":1},
        {"text":'Retired and Active',"value":1},
    ]
  },
  {
    "id": 5,
    "question": 'How long is your working day?',
    "options": [
        {"text":'1-4 hours',"value":1},
        {"text":'5-8 hours',"value":2},
        {"text":'9-12 hours',"value":3},
        {"text":'13+ hours',"value":4},

    ]
  },
  {
    "id": 6,
    "question": 'Number of steps per day?',
    "options": [
        {"text":'2500-4999 steps (Staionary with limited activity)',"value":1},
        {"text":'5000-7499 steps (Low activity)',"value":2},
        {"text":'7500-9999 steps (Somewhat active)',"value":3},
        {"text":'10000-12499 steps (Active)',"value":3},
        {"text":'12500+ steps (Highly active',"value":4},

    ]
  },
  {
    "id": 7,
    "question": 'Are you physically active (after work)?',
    "options": [
        {"text":'No',"value":1},
        {"text":'Light (house duties, light walking)',"value":2},
        {"text":'Moderate (brisk walking, recreational swimming, social tennis)',"value":3},
        {"text":'Vigorous (competitive sports, jogging, aerobic exercise, weight lifting',"value":4},

    ]
  },
  {
    "id": 8,
    "question": 'How many days per week do you exercise?',
    "options": [
        {"text":"I don't exercise","value":1},
        {"text":'I exercise ocasionally',"value":1},
        {"text":'I exercise at least once a week',"value":1},
        {"text":'I exercise at least three times a week',"value":2},
        {"text":'I exercise at least five times a week',"value":3},
        {"text":'I exercise everday',"value":3},

    ]
  },
  {
    "id": 9,
    "question": 'What type of shoes do you wear the most?',
    "options": [
        {"text":"Workboots","image":'./workboots.png',"value":1},
        {"text":"Wellingtons","image":'./wellingtons.png',"value":2},
        {"text":'Runners (Adidas/Nike)', "image":'./runnerssuchasadidasornike.png',"value":3},
        {"text":'Runners (Brooks/Asics)', "image":'./runnerssuchasbrooksorasics.png',"value":4},
        {"text":"Leather Shoes","image":'./leathershoes.png',"value":5}
    ]
  },
  {
    "id": 10,
    "question": 'Which of the following looks similar to your old footwear?',
    "options": [
        {"text":"Worn from inside","image":'./wornfrominside.png',"value":1},
        {"text":"Worn from outside","image":'./wornfromoutside.png',"value":2},
    ]
  },
  {
    "id": 11,
    "question": 'Do you suffer from any of the following types of calluses?',
    "options": [
        {"text":"Option 1","image":'./option1.png',"value":1},
        {"text":"Option 2","image":'./option2.png',"value":2},
        {"text":"I dont suffer from Calluses","value":0},

    ]
  },
  {
    "id": 12,
    "question": 'What is your shoes size',
    "options": [
        {"text":"UK 3-5","value":1},
        {"text":"UK 6-7","value":2},
        {"text":"UK 8-9","value":3},
        {"text":"UK 10-11","value":4},
        {"text":"UK 12-13","value":5},
        {"text":"UK 14 or more","value":6},
    ]
  },
  {
  "id": 13,
    "question": 'What is your weight (Stones)',
    "options": [
        {"text":"Less than 8 stone (less than 50kg)","value":1},
        {"text":"8-10 stone (50-63kg)","value":2},
        {"text":"11-13 stone (69-82kg)","value":3},
        {"text":"14-17 stone (89-108kg)","value":4},
        {"text":"18+ stone (114kg)","value":5},
    ]
  },
    {
        "id": 18,
            "question": 'Do you or any of your family members have a shorter/longer leg (limb length discrepency)',
            "options": [
                {"text":"Yourself","value":6},
                {"text":"Mother","value":5},
                {"text":"Father","value":5},
                {"text":"Grandfather","value":3},
                {"text":"Grandmother","value":3},
                {"text":"Aunt or Uncle","value":2},
                {"text":"No history","value":0},
            ]
    },
    {
        "id": 20,
            "question": 'Do you suffer from any of these ailments',
            "options": [
                {"text":"Heel Pain","value":1},
                {"text":"Sore feet","value":2},
                {"text":"Achilles tendon pain","value":3},
                {"text":"Back Pain","value":4},
                {"text":"Knee Pain","value":5},
                {"text":"Hip Pain","value":6},
                {"text":"Tight Calves","value":7},
                {"text":"Shin splints","value":8},
                {"text":"No history of any of the above","value":0},

            ]
    },
    {
        "id": 21,
            "question": 'Do any of the aliments above wake you up at night',
            "options": [
                {"text":"Yes","value":2},
                {"text":"No","value":1},
            ]
    },
    {
        "id": 22,
            "question": 'Do you suffer from any of the following medical conditions?',
            "options":[
                {"text":"Hammer toe/mallet toe", "image":'./hammertoemallettoe.png',"value":1},
                {"text":"Bunion/Hallux Valgus", "image":'./bunionhalluxvalgus.png',"value":2},
                {"text":"Tailor bunion (bunionette)", "image":'./tailorbunionbunionette.png',"value":3},
                {"text":"No history of the following medical conditions","value":0},
            ]
    },
    {
      "id": 23,
          "question": 'Do you suffer from bow legs (Genu Varum)?',
          "options":[
              {"text":"Yes","value":5},
              {"text":"No","value":0},
          ]
  },
  {
    "id": 24,
        "question": 'Do you suffer from double joint knees?',
        "options":[
            {"text":"Yes","value":5},
            {"text":"No","value":0},
        ]
},
{
  "id": 25,
      "question": 'Do you suffer from Knock knees (Genu Valgum)?',
      "options":[
          {"text":"Yes","value":5},
          {"text":"No","value":0},
      ]
}, 

{"id": 14,
      "question": 'Is there a history of knee replacement',
      "options": [
          {"text":"Yourself","value":6},
          {"text":"Mother","value":5},
          {"text":"Father","value":5},
          {"text":"Grandfather","value":3},
          {"text":"Grandmother","value":3},
          {"text":"Aunt or Uncle","value":2},
          {"text":"No history","value":1},
      ]
    },
    {
        "id": 15,
          "question": 'Is there a history of hip replacement',
          "options": [
              {"text":"Yourself","value":6},
              {"text":"Mother","value":5},
              {"text":"Father","value":5},
              {"text":"Grandfather","value":3},
              {"text":"Grandmother","value":3},
              {"text":"Aunt or Uncle","value":2},
              {"text":"No history","value":1},
        ]
    },
    {
        "id": 17,
            "question": 'Is there a history of back problems',
            "options": [
                {"text":"Yourself","value":6},
                {"text":"Mother","value":5},
                {"text":"Father","value":5},
                {"text":"Grandfather","value":3},
                {"text":"Grandmother","value":3},
                {"text":"Aunt or Uncle","value":2},
                {"text":"No history","value":1},
            ]
    },
    {
        "id": 19,
            "question": 'Which of the pictures below best describes your feet',
            "options": [
                {"text":"Severe high arch (Severe pes cavus)", "image": './severehigharch.png',"value":1},
                {"text":"Middle of the road arch (Subtle pes cavus)", "image": './middleoftheroadhigharch.png',"value":1},
                {"text":"Mild flat foot (Mild pes planus)", "image": './mildflatfoot.png',"value":2},
                {"text":"Moderate flat foot (Moderate pes planus)", "image": './moderateflatfoot.png',"value":2},
                {"text":"Severe flat foot (Severe pes planovalgus)", "image": './severeflatfoot.png',"value":3},
                {"text":"Really flat foot (Abductovarus forefoot)", "image": './severeflatfoot.png',"value":3},
            ]
    }
]

entries=[]

@app.route('/')
def index():
    session.clear()
    return render_template('index.html', question=questions[0], question_iter=0)

""" @app.route('/next', methods=['POST'])
def next_question():
    question_id = int(request.form['question_id'])
    if question_id < len(questions) - 1:
        return render_template('questionnaire.html', question=questions[question_id + 1], question_id=question_id + 1)
    else:
        return redirect(url_for('complete')) """


@app.route('/questionnaire/<int:question_iter>', methods=['GET', 'POST'])
def questionnaire(question_iter):
    if request.method == 'POST':
        selected_answer_value = request.form.get('answer_value')
        print(selected_answer_value)
        # Save the submitted answer to the session
        if 'answers' not in session:
            session['answers'] = []  # Ensure there is a list to append to
        session['answers'].append(selected_answer_value)
        
        if 'value' not in session:
            session['value'] = []  # Initialize if not already present
        session['value'].append(int(selected_answer_value))  # Store value, convert to int
        
        session.modified = True  # Ensure session is marked as modified
        
        if question_iter < len(questions):
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
    total_score = sum(session.get('values', []))  # Calculate total score

    # Here, you could calculate the score based on answers
    # For demonstration, just print answers to the console
    print("User's Answers:", answers)
    
    # Render the results template, passing in answers or calculated score
    return render_template('complete.html', answers=answers,total_score=total_score)


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