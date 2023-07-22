from flask import Flask, request, make_response, render_template, redirect, url_for
from flask.helpers import url_for
import pandas as pd
# import warnings
# warnings.filterwarnings('ignore')

# Initialize Flask app
app = Flask(__name__)  

def recommendation_kdrama(name):
    data = pd.read_csv("project trending/data/kdrama.csv")
    cosine_sim = pd.read_csv("project trending/data/cosine_sim.csv")
    indexprod = int(data.loc[data['Name'] == name].index.values[0])
    similar_review = list(enumerate(cosine_sim.iloc[indexprod], start=-1))
    sorted_similar_review = sorted(similar_review, key=lambda x:x[1], reverse=True)
    aa = []
    for i in range(1,7) :
        aa.append(sorted_similar_review[i][0])
    return data.iloc[aa,:5]

# @app.route("/")
# def home_page():
#     return render_template("index.html")

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/recommendation", methods=["POST"])

def recommendation():
    if request.method == "POST":
        result = request.form
        kdrama_name = str(request.form["Name"])
        df = recommendation_kdrama(kdrama_name)
        headers = list(enumerate(df.columns, 1))
        rows = []

        for _, row in df.iterrows():
            rows.append(list(enumerate(row, 1)))

        return render_template("table.html", result=result, headers=headers, rows=rows, Name=kdrama_name)
    # else:
        # return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
    