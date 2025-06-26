# Student Performance Prediction

A Flask-based machine learning web application that predicts students' math scores based on various demographic and educational features. The application uses a MySQL database to store, retrieve, and update student performance data.

---

## 🔍 Introduction

In this project, we build a predictive model to estimate a student's math score out of 100 using the following input features:

* **Gender** (e.g., male, female)
* **Race/Ethnicity**
* **Parental Level of Education**
* **Lunch** (standard or free/reduced)
* **Test Preparation Course** (none or completed)
* **Reading Score**
* **Writing Score**

The trained model provides quick predictions that can be used for educational assessment and decision-making.

---

## ⚙️ Features

* **Flask Web Interface**: User-friendly forms for single predictions and batch CSV uploads.
* **MySQL Integration**: Stores historical data in two tables:

  * `performance`: raw data ingested from CSV uploads.
  * `secondary_table`: enriched records with timestamps and model results.
* **Batch Upload**: Upload a `.csv` file to insert or merge data directly into the database.
* **Normal Training**: Train the model on the existing database records with one click.

---

## 🛠️ Prerequisites

* Python 3.8 or above
* MySQL Server (local or Azure MySQL Flexible Server)
* Git (to clone the repository)

---

## 🚀 Setup and Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/ansari-ehteesham/Student-Performance-Prediction
   cd student-performance-prediction
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create an **\`\`** file** in the project root with the following variables:

   ```dotenv
   MYSQL_HOST=<your_mysql_host>
   MYSQL_PORT=<your_mysql_port>
   MYSQL_USER=<your_mysql_user>
   MYSQL_PASSWORD=<your_mysql_password>
   ```

4. **Prepare your database**

   * Database name must be \`\`.
   * Create two tables in `student` database:

     ```sql
     CREATE TABLE IF NOT EXISTS performance (
       gender VARCHAR(20),
       race_ethnicity VARCHAR(50),
       parental_level_of_education VARCHAR(50),
       lunch VARCHAR(20),
       test_preparation VARCHAR(20),
       math_score INT,
       reading_score INT,
       writing_score INT
     );

     CREATE TABLE IF NOT EXISTS secondary_table (
       gender VARCHAR(20),
       race_ethnicity VARCHAR(50),
       parental_level_of_education VARCHAR(50),
       lunch VARCHAR(20),
       test_preparation VARCHAR(20),
       math_score INT,
       reading_score INT,
       writing_score INT,
     );
     ```

5. **Start the Flask application**

   ```bash
   python application.py
   ```

6. **Access the app** in your browser:

   ```
   ```

[http://127.0.0.1:5000](http://127.0.0.1:5000)

```

---

## 📂 Project Structure

```

├── artifacts/            # Processed Dataset and Trained Model 
├── logs/                 # Application Logs
├── notebook              # Jupyter Notebook for Experiment
├── application.py        # Main Flask application 
├── requirements.txt      # Python dependencies 
├── .env                  # Environment variables (not in repo) 
├── src/                  # Project modules 
│   ├── components/       # Lifecycle of Model 
│   ├── pipeline/         # ML pipelines for training & prediction 
│   └── exception.py      # Custom Exception configuration 
│   └── logger.py         # Logging configuration 
│   └── utils.py          # Extra Utility and MySQL Connection Configuration 
├── templates/            # Jinja2 HTML templates 
└── static/               # CSS & JS assets
└── setup.py              # Setup for our own library

```

---

## 📈 Usage

1. **Single Prediction**: Fill out the form on `/prediction` with student details.
2. **Batch Upload**: Upload a `.csv` of multiple records on `/train_model`.
3. **Normal Training**: Click “Start Training” to re-train on full dataset.


---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for details.

```
