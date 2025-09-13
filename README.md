# Dementia Prediction System

## Overview
A Python application for predicting dementia using Logistic Regression, Random Forest, and XGBoost models. Features a compact two-column GUI built with CustomTkinter for inputting patient data (demographics, medical history, vital signs, lifestyle, clinical assessment, medication). Displays prediction probabilities, model accuracies, valid range indicators, and a scrollable dark-themed interface.

## Features
- Two-column GUI with six input sections  
- Predictions from three ML models  
- Model accuracies shown with results  
- Input range indicators via placeholders and tooltips  
- Scrollable dark mode layout  

## Prerequisites
- Python 3.13  
- Anaconda or Miniconda  
- Dependencies: `customtkinter>=5.2.0`, `pandas>=2.0.0`, `xgboost>=2.0.0`, `scikit-learn>=1.2.0`, `numpy>=1.26.0`  

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Chilliflex/Dementia-Model
   cd dementia-prediction-system

2. Create and activate a virtual environment:

   ```bash
   conda create -p venv python==3.13 -y
   conda activate venv
   ```
3. Install dependencies:

   ```bash
   pip install customtkinter pandas xgboost scikit-learn numpy
   ```
4. Ensure `data.csv` is in the project root with required columns (22 features + Diagnosis).

## File Structure

* `data.csv` – Dataset for training
* `gui.py` – GUI implementation
* `model.py` – ML models
* `README.md` – Documentation
* `venv/` – Virtual environment

## Usage

Run the app:

```bash
python gui.py
```

