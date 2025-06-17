from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # authentication logic
        return redirect(url_for('chatbot'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # registration logic
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(debug=True)
