from flask import Flask, render_template
import os
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

app = Flask(__name__)

@app.route('/')
def Test():
    return render_template('plot.html', name='new_plot', url ='/static/output.pdf')

def create_figure():
    data = pd.read_csv('data.csv')
    plt.figure(figsize=(12, 6))
    sns_plot = sns.lineplot(x='timestamp', y='value', hue='variable', data=pd.melt(data, ['timestamp']))
    sns_plot.tick_params(axis='x', labelrotation=30)
    sns_plot.figure.savefig(os.path.join(os.getcwd(), "static/output.pdf"), bbox_inches="tight")

if __name__ == '__main__':
    create_figure()
    app.run(debug=True)
