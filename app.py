from flask import Flask, render_template, request

from process import *

app = Flask(__name__)

#Base home page.
@app.route('/')
def home():
    return render_template('index.html')



#function that calls another webpage.
@app.route('/submit', methods=['POST'])
def submit():
    name_init = request.form.get('input_user')
    county_select=request.form.get('category')
    name = func_complete_cycle(name_init)
    return render_template('greet.html', name=name, selection=county_select)



#Base home page.
@app.route('/greet')
def greet():
    return render_template('greet.html')


if __name__ == '__main__':
    app.run(debug=True)

