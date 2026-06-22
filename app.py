from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz')
def quiz():

    questions = []

    with open('questions.txt', 'r') as file:

        for line in file:

            parts = line.strip().split('|')

            if len(parts) == 3:

                question = parts[0]
                options = parts[1].split(',')
                answer = parts[2]

                questions.append({
                    'question': question,
                    'options': options,
                    'answer': answer
                })

    return render_template(
        'quiz.html',
        questions=questions
    )
@app.route('/result')
def result():
    return render_template('result.html')
@app.route('/admin')
def admin():

    total_attempts = 0
    highest_score = 0
    total_score = 0

    try:

        with open('results.txt', 'r') as file:

            for line in file:

                parts = line.strip().split(' - ')

                if len(parts) == 2:

                    score = int(
                        parts[1].split('/')[0]
                    )

                    total_attempts += 1
                    total_score += score

                    if score > highest_score:
                        highest_score = score

    except:
        pass

    average_score = 0

    if total_attempts > 0:
        average_score = round(
            total_score / total_attempts,
            2
        )

    question_count = 0

    try:

        with open('questions.txt', 'r') as file:

            question_count = len(
                file.readlines()
            )

    except:
        pass

    return render_template(
        'admin.html',
        total_attempts=total_attempts,
        highest_score=highest_score,
        average_score=average_score,
        question_count=question_count
    )
@app.route('/add_question')
def add_question():
    return render_template('add_question.html')
@app.route('/view_results')
def view_results():

    try:
        with open('results.txt', 'r') as file:
            results = file.read()

    except Exception as e:
        results = str(e)

    return render_template(
        'view_results.html',
        results=results
    )
@app.route('/save_result', methods=['POST'])
def save_result():

    username = request.form['username']
    score = request.form['score']

    with open('results.txt', 'a') as file:
        file.write(f"{username} - {score}/3" + "\n")

    return "Saved"
@app.route('/delete_results')
def delete_results():

    open('results.txt', 'w').close()

    return render_template(
        'admin.html'
    )
@app.route('/save_question', methods=['POST'])
def save_question():

    question = request.form['question']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3 = request.form['option3']
    option4 = request.form['option4']
    answer = request.form['answer']

    line = (
        question + "|" +
        option1 + "," +
        option2 + "," +
        option3 + "," +
        option4 + "|" +
        answer + "\n"
    )

    with open('questions.txt', 'a') as file:
        file.write(line)

    return render_template('admin.html')
@app.route('/leaderboard')
def leaderboard():

    scores = []

    try:

        with open('results.txt', 'r') as file:

            for line in file:

                parts = line.strip().split(' - ')

                if len(parts) == 2:

                    name = parts[0]

                    score = int(
                        parts[1].split('/')[0]
                    )

                    scores.append(
                        (name, score)
                    )

        scores.sort(
            key=lambda x: x[1],
            reverse=True
        )

    except:
        pass

    return render_template(
        'leaderboard.html',
        scores=scores
    )
if __name__ == '__main__':
    app.run(debug=True)