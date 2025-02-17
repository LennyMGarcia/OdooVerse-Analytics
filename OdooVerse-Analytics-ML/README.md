# OdooVerse-Analytics ML

This project implements a product recommendation system using collaborative filtering techniques, such as **KNN** and **SVD**, on data obtained from Odoo. It is designed to analyze business data and enhance decision-making through advanced analytics.

## 🚀 Features
- **Data exploration and cleaning**: An exploratory data analysis (EDA) is performed to identify patterns and anomalies.
- **Preprocessing**: Data transformation, including scaling, encoding, and handling missing values.
- **Model construction**: Implementation of recommendation algorithms such as **K-Nearest Neighbors (KNN)** and **Singular Value Decomposition (SVD)**.
- **Model evaluation**: Performance analysis using metrics like **MAE (Mean Absolute Error)** and cross-validation.
- **Final model selection**: Choosing the best model based on its performance and generalization ability.


## 📂 Project structure
```ruby
/odooverse-analytics-ml
│
├── /data/
│   ├── raw/                      # Raw data
│   └── processed/                # Processed data
│
├── /logs/                      
│   └── error_log.log/            # logs
│              
├── /notebooks/                   # Jupyter Notebooks
│   ├── 01_EDA.ipynb              # Exploratory data analysis
│   ├── 02_preprocessing.ipynb    # Preprocessing
│   ├── 03_basic_model.ipynb      # Basic models
│   ├── 04_model_evaluation.ipynb # Model evaluation
│   └── 05_final_model.ipynb      # Final model
│
├── /src/                         # Scripts and functions
│   ├── preprocessing.py          # Data transformation
│   ├── models.py                 # Algorithm implementation
│   ├── evaluation.py             # Metrics calculation
│   └── utils.py                  # Helper functions
│
├── /models/                      # Saved models
│   ├── knn_model.pkl             # knn model implementation
│   └── svd_model.pkl             # svd model implementation
│
├── /reports/                     # Results and analysis   
│
├── .gitignore             
├── requirements.txt              # Dependencies
├── enviroment.yml                # Conda Dependencies
├── README.md                     # Project description
└── config.yaml                   # Configuration

```
