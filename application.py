from flask import Flask, render_template, request, jsonify


from src.utils import convert_dataset_as_dataframe, mysql_connection_establishment, inserting_data_mysql
from src.pipeline.prediction_pipeline import PredictionPipeline
from src.pipeline.training_pipeline import TrainingPipeline
from src.logger import logging

application = Flask(__name__)

app = application

# Database Connection Establishment
cnx = mysql_connection_establishment(database_name="student")

#route to main page
@app.route("/")
def index():
    return render_template('index.html')

# prediction route
@app.route("/prediction", methods=["GET", "POST"])
def predict_datapoint():
    if request.method == "GET":
        return render_template('prediction.html')
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
        
        inserting_data_mysql(mysql=cnx, data=data)
        
        return render_template('prediction.html', number = model_result[0])
    
@app.route('/train_model', methods=['GET', 'POST'])
def model_training():
    # if someone GETs this URL directly, we'll just start training anyway
    if not cnx.is_connected():
        return jsonify(status="error", message="DB not connected"), 500

    cursor = cnx.cursor()
    cursor.execute("SELECT COUNT(*) FROM secondary_table")
    count = cursor.fetchone()[0]
    cursor.close()

    if count < 1:
        return jsonify(status="error", message="Not enough data to train"), 400

    train_piepline = TrainingPipeline()
    train_piepline.run(cnx)

    return jsonify(status="success", message="Training completed")



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)