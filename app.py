from flask import Flask, request, render_template_string, jsonify, redirect, url_for, flash, session
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages and session

# HTML for main page
main_page_html = '''
<!DOCTYPE html>
<html>
<head>
  <title>Quiz Website</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
    }
    header {
      background-color: #333;
      color: white;
      padding: 10px 0;
      text-align: center;
    }
    main {
      padding: 20px;
    }
    section {
      margin-bottom: 20px;
    }
    a {
      color: #007bff;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
    #articles-list, #quizzes-list {
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <header>
    <h1>Quiz Website</h1>
  </header>
  <main>
    <section id="signup">
      <h2>Sign up</h2>
      <a href="/signup-page">Go to Sign up Page</a>
    </section>
    <section id="login">
      <h2>Login</h2>
      <a href="/login-page">Go to Login Page</a>
    </section>
    <section id="leaderboard">
      <h2>Leaderboard</h2>
      <a href="/leaderboard">View Leaderboard</a>
    </section>
  </main>
</body>
</html>
'''

# HTML for signup page
signup_page_html = '''
<!DOCTYPE html>
<html>
<head>
  <title>Sign up</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
    }
    header {
      background-color: #333;
      color: white;
      padding: 10px 0;
      text-align: center;
    }
    main {
      padding: 20px;
    }
    #signup-form {
      max-width: 400px;
      margin: auto;
    }
    label {
      display: block;
      margin-bottom: 5px;
    }
    input[type="email"], input[type="password"] {
      width: 100%;
      padding: 8px;
      margin-bottom: 10px;
    }
    input[type="submit"] {
      padding: 10px 20px;
      background-color: #007bff;
      color: white;
      border: none;
      cursor: pointer;
    }
    input[type="submit"]:hover {
      background-color: #0056b3;
    }
    #output {
      margin-top: 20px;
      padding: 10px;
      border: 1px solid #ddd;
      background-color: #f9f9f9;
    }
  </style>
</head>
<body>
  <header>
    <h1>Sign up</h1>
  </header>
  <main>
    <section id="signup">
      <form id="signup-form" method="post" action="/signup">
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>
        <input type="submit" value="Sign up">
      </form>
    </section>
  </main>
</body>
</html>
'''

# HTML for login page
login_page_html = '''
<!DOCTYPE html>
<html>
<head>
  <title>Login</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
    }
    header {
      background-color: #333;
      color: white;
      padding: 10px 0;
      text-align: center;
    }
    main {
      padding: 20px;
    }
    #login-form {
      max-width: 400px;
      margin: auto;
    }
    label {
      display: block;
      margin-bottom: 5px;
    }
    input[type="email"], input[type="password"] {
      width: 100%;
      padding: 8px;
      margin-bottom: 10px;
    }
    input[type="submit"] {
      padding: 10px 20px;
      background-color: #007bff;
      color: white;
      border: none;
      cursor: pointer;
    }
    input[type="submit"]:hover {
      background-color: #0056b3;
    }
    #output {
      margin-top: 20px;
      padding: 10px;
      border: 1px solid #ddd;
      background-color: #f9f9f9;
    }
  </style>
</head>
<body>
  <header>
    <h1>Login</h1>
  </header>
  <main>
    <section id="login">
      <form id="login-form" method="post" action="/login">
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>
        <input type="submit" value="Login">
      </form>
    </section>
  </main>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(main_page_html)

@app.route('/signup-page')
def signup_page():
    return render_template_string(signup_page_html)

@app.route('/login-page')
def login_page():
    return render_template_string(login_page_html)

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if user already exists
    with open(r"C:\Users\Mannan Bajaj\Downloads\project\users.csv", 'r+') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == email:
                flash('User already exists. Please login.')
                return redirect(url_for('login_page'))
    
    # Add the new user with 0 points
    with open(r"C:\Users\Mannan Bajaj\Downloads\project\users.csv", 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, password, 0])

    flash('Thanks for signing up!')
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Check credentials and load user points
    with open(r"C:\Users\Mannan Bajaj\Downloads\project\users.csv", 'r+') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == email and row[1] == password:
                session['email'] = email
                session['points'] = int(row[2])
                flash(f'Login successful! You have {row[2]} points.')
                return redirect(url_for('articles'))
    
    flash('Invalid credentials. Please try again.')
    return redirect(url_for('login_page'))

@app.route('/articles')
def articles():
    sustainability_articles = [
        {"title": "Understanding Climate Change", "url": "/article/climate-change"},
        {"title": "Sustainable Living Tips", "url": "/article/sustainable-living"},
        {"title": "Renewable Energy Sources", "url": "/article/renewable-energy"},
        {"title": "Reducing Plastic Waste", "url": "/article/plastic-waste"},
    ]
    
    articles_html = '<h2>Sustainability Articles</h2><ul>'
    for article in sustainability_articles:
        articles_html += f'''
        <li>
            <h3>{article["title"]}</h3>
            <a href="{article["url"]}">Read more</a>
        </li>'''
    articles_html += '</ul>'

    return render_template_string(articles_html)

@app.route('/article/<article_name>')
def full_article(article_name):
    articles = {
        "climate-change": '''
        <h2>Understanding Climate Change</h2>
        <p>Climate change refers to significant changes in global temperature, precipitation, wind patterns, 
        and other measures of climate over long periods. While climate change can result from natural factors 
        such as changes in solar intensity, volcanic eruptions, and variations in Earth's orbit, human activities 
        in recent decades have become the primary driver.</p>
        <p><a href="/quiz/climate-change">Take Quiz</a></p>
        ''',
        "sustainable-living": '''
        <h2>Sustainable Living Tips</h2>
        <p>Sustainable living is a lifestyle that attempts to reduce an individual's or society's use of the Earth's 
        natural resources and personal resources. Individuals who live sustainably often try to reduce their 
        carbon footprint by altering their transportation methods, energy consumption, and diet.</p>
        <p><a href="/quiz/sustainable-living">Take Quiz</a></p>
        ''',
        "renewable-energy": '''
        <h2>Renewable Energy Sources</h2>
        <p>Renewable energy comes from sources that are naturally replenishing, such as wind, solar, and water.</p>
        <p><a href="/quiz/renewable-energy">Take Quiz</a></p>
        ''',
        "plastic-waste": '''
        <h2>Reducing Plastic Waste</h2>
        <p>Plastic waste is one of the major contributors to environmental pollution. Here are some tips to reduce it.</p>
        <p><a href="/quiz/plastic-waste">Take Quiz</a></p>
        '''
    }

    if article_name in articles:
        return render_template_string(articles[article_name])
    else:
        return "Article not found"

@app.route('/quiz/<quiz_name>', methods=['GET', 'POST'])
def quiz(quiz_name):
    if 'email' not in session:
        flash('Please login to take quizzes.')
        return redirect(url_for('login_page'))
    
    quizzes = {
        "climate-change": {
            "questions": [
                {
                    "question": "What is the primary cause of climate change?",
                    "options": ["Burning fossil fuels", "Deforestation", "Both of the above"],
                    "correct": "Both of the above"
                },
                {
                    "question": "Which gas is most associated with global warming?",
                    "options": ["Oxygen", "Carbon dioxide", "Nitrogen"],
                    "correct": "Carbon dioxide"
                },
                {
                    "question": "What is the key solution to combat climate change?",
                    "options": ["Renewable energy", "More deforestation", "More plastic use"],
                    "correct": "Renewable energy"
                }
            ]
        },
        "sustainable-living": {
            "questions": [
                {
                    "question": "What is the first step towards sustainable living?",
                    "options": ["Buy more products", "Reduce, reuse, recycle", "Use fossil fuels"],
                    "correct": "Reduce, reuse, recycle"
                },
                {
                    "question": "Which of the following is a sustainable product?",
                    "options": ["Plastic straws", "Reusable cloth bags", "Single-use plastic cups"],
                    "correct": "Reusable cloth bags"
                }
            ]
        },
        "renewable-energy": {
            "questions": [
                {
                    "question": "Which of the following is a renewable energy source?",
                    "options": ["Coal", "Solar energy", "Natural gas"],
                    "correct": "Solar energy"
                },
                {
                    "question": "Why is renewable energy important?",
                    "options": ["It reduces carbon emissions", "It is non-renewable", "It harms the environment"],
                    "correct": "It reduces carbon emissions"
                }
            ]
        },
        "plastic-waste": {
            "questions": [
                {
                    "question": "How long does it take plastic to decompose?",
                    "options": ["50 years", "100 years", "Hundreds of years"],
                    "correct": "Hundreds of years"
                },
                {
                    "question": "What is a simple way to reduce plastic waste?",
                    "options": ["Use reusable bags", "Throw more plastic", "Use single-use plastics"],
                    "correct": "Use reusable bags"
                }
            ]
        }
    }

    if request.method == 'POST':
        user_answers = request.form.to_dict()
        correct_answers = [q['correct'] for q in quizzes[quiz_name]['questions']]
        user_correct_answers = 0
        for i, answer in enumerate(user_answers.values()):
            if answer == correct_answers[i]:
                user_correct_answers += 1

        # Update user points in CSV
        update_user_points(session['email'], user_correct_answers)
        
        flash(f'You got {user_correct_answers} out of {len(correct_answers)} questions right!')
        return redirect(url_for('quiz', quiz_name=quiz_name))
    
    # Generate quiz form
    quiz_html = f'<h2>{quiz_name.replace("-", " ").title()} Quiz</h2>'
    quiz_html += '<form method="post">'
    for i, question in enumerate(quizzes[quiz_name]['questions']):
        quiz_html += f'<p>{i + 1}. {question["question"]}</p>'
        for option in question['options']:
            quiz_html += f'<input type="radio" name="q{i + 1}" value="{option}" required> {option}<br>'
    quiz_html += '<br><input type="submit" value="Submit"></form>'

    return render_template_string(quiz_html)

def update_user_points(email, points_to_add):
    # Read the existing users
    users = []
    with open(r"C:\Users\Mannan Bajaj\Downloads\project\users.csv", 'r+') as file:
        reader = csv.reader(file)
        for row in reader:
            users.append(row)

    # Update the points for the given user
    for user in users:
        if user[0] == email:
            user[2] = str(int(user[2]) + points_to_add)  # Add the points

    # Write back the updated user data
    with open(r"C:\Users\Mannan Bajaj\Downloads\project\users.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(users)

@app.route('/leaderboard')
def leaderboard():
    users = []
    
    # Read user data from CSV
    with open(r"C:\Users\Mannan Bajaj\Downloads\project\users.csv", 'r+') as file:
        reader = csv.reader(file)
        for row in reader:
            users.append({"email": row[0], "points": int(row[2])})
    
    # Sort users by points in descending order and get the top 10
    top_users = sorted(users, key=lambda x: x['points'], reverse=True)[:10]

    leaderboard_html = '''
    <h2>Leaderboard - Top 10 Users</h2>
    <table border="1">
      <tr><th>Email</th><th>Points</th></tr>
    '''
    
    for user in top_users:
        leaderboard_html += f"<tr><td>{user['email']}</td><td>{user['points']}</td></tr>"
    
    leaderboard_html += '</table>'
    return render_template_string(leaderboard_html)

if __name__ == '__main__':
    app.run(debug=True)









