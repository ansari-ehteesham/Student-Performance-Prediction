from flask import Flask, render_template, request, flash, redirect, jsonify, session, url_for
import pandas as pd
import os


from src.utils import convert_dataset_as_dataframe, mysql_connection_establishment, inserting_data_mysql
from src.pipeline.prediction_pipeline import PredictionPipeline
from src.pipeline.training_pipeline import TrainingPipeline
from src.logger import logging

application = Flask(__name__)

app = application
app.secret_key = os.getenv("SECRET_KEY")

# Database Connection Establishment
cnx = mysql_connection_establishment(database_name="student")

#route to main page
@app.route("/")
def index():
    return render_template('index.html')

# prediction route
@app.route("/prediction", methods=["GET", "POST"])
def predict_datapoint():
    pred_pipeline = PredictionPipeline()
    model_list = pred_pipeline.trained_model_list
    results = {
            "number": None,
            "models_list": model_list,
        }

    if request.method == "GET":
        return render_template('prediction.html', results = results)
    else:
        data = {
            "gender": request.form.get('gender'),
            "race_ethnicity": request.form.get('race_ethnicity'),
            "parental_level_of_education": request.form.get('parental_level_of_education'),
            "lunch": request.form.get('lunch'),
            "test_preparation": request.form.get('test_preparation_course'),
            "reading_score": request.form.get('reading_score'),
            "writing_score": request.form.get('writing_score'),
        }

        model_name = request.form.get('model_selection')

        columns = list(data.keys())
        values = [list(data.values())]

        df = convert_dataset_as_dataframe(dataset=values, column=columns)

        # prediction
        model_result = pred_pipeline.prediction(df=df, model = model_name)
        data["math_score"] = int(model_result)

        # giving data to the database to store it into table
        inserting_data_mysql(mysql=cnx, data=data)

        results["number"] = model_result[0]
        
        return render_template('prediction.html', results = results)
    
@app.route('/train_model', methods=['GET', 'POST'])
def train_model():
    if request.method == 'POST':
        # —— CSV‐UPLOAD PATH —————————————————————————
        if 'file' in request.files:
            file = request.files['file']
            if not file.filename:
                flash("⚠️ Please select a CSV file.")
                return redirect(request.url)

            df = pd.read_csv(file, encoding='ISO-8859-1').where(pd.notnull, None)
            cursor = cnx.cursor(buffered=True)
            cursor.execute("SELECT * FROM secondary_table LIMIT 0")
            db_cols = cursor.column_names
            cursor.close()

            missing = set(db_cols) - set(df.columns)
            extra   = set(df.columns) - set(db_cols)
            if missing or extra:
                parts = []
                if missing: parts.append("Missing: " + ", ".join(sorted(missing)))
                if extra:   parts.append("Unexpected: " + ", ".join(sorted(extra)))
                flash("⚠️ Column mismatch — " + " | ".join(parts))
                return render_template('training_model.html')

            for rec in df.to_dict(orient='records'):
                inserting_data_mysql(mysql=cnx, data=rec)

            session['csv_results'] = {
                'rows': df.shape[0],
                'columns': df.shape[1]
            }
            flash("✅ CSV uploaded and data inserted!")
            return redirect(url_for('train_model'))

        # —— NORMAL-TRAINING PATH —————————————————————————
        elif request.form.get('mode') == 'train':
            try:
                pipeline = TrainingPipeline()
                best_model_name, best_score = pipeline.run(cnx)
                session['model_results'] = {
                    'model_name': best_model_name,
                    'score': best_score
                }
                return redirect(url_for('train_model'))
            except Exception as e:
                app.logger.exception("Training failed")
                flash(f"⚠️ Training failed: {e}")
                return redirect(url_for('train_model'))

    # —— GET (or after redirect) —————————————————————————
    csv_results   = session.pop('csv_results', None)
    model_results = session.pop('model_results', None)
    return render_template(
        'training_model.html',
        results=csv_results,
        model_results=model_results
    )



if __name__ == "__main__":
    app.run(host="0.0.0.0")