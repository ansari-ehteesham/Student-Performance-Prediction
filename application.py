from flask import Flask, render_template, request
import pandas as pd

from src.utils import convert_dataset_as_dataframe, mysql_connection_establishment, inserting_data_mysql
from src.pipeline.prediction_pipeline import PredictionPipeline

application = Flask(__name__)

app = application

#route to main page
@app.route("/")
def index():
    return render_template('index.html')

# prediction route
@app.route("/prediction", methods=["GET", "POST"])
def predict_datapoint():
    if request.method == "GET":
        return render_template('home.html')
    else:
        data = {
            "gender": request.form.get('gender'),
            "race_ethnicity": request.form.get('ethnicity'),
            "parental_level_of_education": request.form.get('parental_level_of_education'),
            "lunch": request.form.get('lunch'),
            "test_preparation": request.form.get('test_preparation_course'),
            "reading_score": request.form.get('writing_score'),
            "writing_score": request.form.get('reading_score')
        }

        columns = list(data.keys())
        values = [list(data.values())]

        df = convert_dataset_as_dataframe(dataset=values, column=columns)

        # prediction
        pred_pipeline = PredictionPipeline()
        model_result = pred_pipeline.prediction(df=df)
        data["math_score"] = int(model_result)

        # giving data to the database to store it into table
        mysql = mysql_connection_establishment(database_name="student")
        inserting_data_mysql(mysql=mysql, data=data)
        
        return render_template('home.html', results = model_result[0])



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)