# OdooVerse-Analytics ML

Este proyecto implementa un sistema de recomendación de productos utilizando técnicas de filtrado colaborativo, como **KNN** y **SVD**, sobre datos obtenidos de Odoo. Está diseñado para analizar datos empresariales y mejorar la toma de decisiones mediante análisis avanzados.

## 🚀 Características
- **Exploración y limpieza de datos**: Se realiza un análisis exploratorio de datos (EDA) para identificar patrones y anomalías.
- **Preprocesamiento**: Transformación de los datos, incluyendo escalado, codificación y tratamiento de valores nulos.
- **Construcción de modelos**: Implementación de algoritmos de recomendación como **K-Nearest Neighbors (KNN)** y **Singular Value Decomposition (SVD)**.
- **Evaluación de modelos**: Análisis de rendimiento con métricas como **MAE (Mean Absolute Error)** y validación cruzada.
- **Selección de modelo final**: Elección del mejor modelo basado en su rendimiento y capacidad de generalización.

## 📂 Estructura del Proyecto
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
