# Phishing-Email-Detector-App

An AI-powered phishing email detection system built using Machine Learning and Natural Language Processing.

## Features

* Detects phishing emails from raw email text.
* TF-IDF text vectorization.
* Logistic Regression classification model.
* Random Forest classification model.
* Interactive Streamlit web interface.
* Real-time prediction.
* Lightweight and fast deployment.

## Tech Stack

* Python
* Streamlit
* Scikit-Learn
* Pandas
* NumPy
* Matplotlib

## Machine Learning Pipeline

```
Email Text -> Text Cleaning -> TF-IDF -> Vectorization -> Logistic Regression -> Random Forest -> Prediction

```

## Dataset

Phishing Email Text Analytics Dataset

source (https://www.kaggle.com/datasets/subhajournal/phishingemails)

* Approximately 18,600 email samples
* Binary classification:

  * Safe
  * Phishing

## Model Performance

 Metric                    | Score 
 Cross Validation Accuracy | ~96%  

## Installation

```bash
git clone https://github.com/TauheedKazi/Phishing-Email-Detector-App.git

open cmd

cd Phishing-Email-Detector-App

pip install -r requirements.txt

streamlit run app.py
