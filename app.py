from flask import Flask
from flask import render_template, request
import osu_api
import plotly.express as px

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def frontpage():
    
    if request.method == 'GET':
        return render_template('frontpage.html')
    
    if request.method == 'POST':
        osu_username = request.form.get('osu_username')       
        data = osu_api.calculate(osu_username)
        fig = px.pie(data_frame = [data], names=data.keys(), values=data.values(), labels=data.keys(), hole=0.2, title="Scores")
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.write_html("templates/result.html")
        return render_template('result.html')