from flask import Flask, render_template
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def Test():
    return render_template('plot.html', name='new_plot', url ='/static/output.pdf')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080')
