# Titanic Data Analysis Project

# Overview
This project aims to analyze the Titanic dataset, identify and handle missing values, and visualize key insights such as age distribution of survivors and survival rates by gender. The analysis includes data cleaning, handling missing values, and generating various plots to understand the data better.

# Features
Load and preview the dataset.
Handle missing values using appropriate techniques.
Generate HTML tables for data preview and summary statistics.
Create heatmaps to visualize missing and handled values.
Generate histograms for age distribution of survivors.
Generate count plots for survival by gender.

# Requirements
Python 3.x
Django
Pandas
Seaborn
Matplotlib
BytesIO
Base64

# Set Up Django Project
django-admin startproject myproject
cd myproject
python manage.py startapp myapp

# Configure settings.py
INSTALLED_APPS = [
'myapp',
]

# Add the Analysis Code
Place the provided analyze function in your views.py in the Django app (e.g., myapp/views.py):

# Create Templates
Create an HTML template (analyze.html) in your app's templates directory (e.g., myapp/templates/analyze.html):

# Run the Server
# Access the Analysis
Open your web browser and go to http://127.0.0.1:8000/analyze/<file_id>/ to view the analysis. Replace <file_id> with the actual ID of the file you want to analyze.

# GIT
Create the git repository
Initialize the git repository
Add and commit your files 
Connect to your git repository
Push the code to github
