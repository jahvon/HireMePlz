from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def hello_world():
    author = "Me"
    return render_template('index.html', author=author)

@app.route('/signup', methods = ['POST'])
def signup():
    name = reqeust.form['name']
    email = request.form['email']
    print("The name is '" + name + "'")
    print("The email address is '" + email + "'")
    return redirect('/')

if __name__ == '__main__':
    app.run()
