from django.shortcuts import render,redirect
from .models import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64


def index(request):
    if request.method == "POST":
        file = request.FILES['file']
        uploaded_file = File.objects.create(file=file)
        return redirect('analyze', file_id=uploaded_file.id)
    return render(request, 'index.html', {})

def change_age(value):
    Age = value[0]
    Pclass = value[1]

    if pd.isnull(Age):
        if Pclass == 1:
            return 37
        elif Pclass == 2:
            return 29
        else:
            return 24
    else:
        return Age

def analyze(request, file_id):
    file_instance = File.objects.get(id=file_id)
    file_path = file_instance.file.path
    df = pd.read_csv(file_path)
    head_html = df.head().to_html()
    summary_html = df.describe().to_html()

    # missing Values 
    missing_values_html = df.isnull().sum().to_dict()
    filtered_missing = {key: value for key, value in missing_values_html.items() if value != 0}
    if  filtered_missing:
        print("Missing values:")
        for key,value in filtered_missing.items():
            print(f"{key}: {value}")
    else:
        print("No missing values")

    #sns for heatmap ploting for null values
    plt.figure(figsize=(5, 5))
    sns.heatmap(df.isnull(), cbar=True, cmap='magma')
    plt.title('Missing Values Heatmap')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    image_base64 = base64.b64encode(image_png).decode('utf-8')

    #handeling missing values
    sex = pd.get_dummies(df['Sex'], drop_first=True) 
    embark_new = pd.get_dummies(df['Embarked'], drop_first=True)
    df.drop(['Sex','Embarked','Name','Ticket','PassengerId'],axis = 1,inplace=True)
    df = pd.concat([df,sex],axis=1)
    df = pd.concat([df,embark_new],axis=1)
    if 'male' in df.columns:
      df.rename(columns={'male': 'Sex'}, inplace=True)
    df.drop(['Cabin'],axis=1,inplace=True)

    #handelAge
    reate_age_pclass = df.groupby('Pclass').describe()['Age']
    create_age_pclass_html = reate_age_pclass.to_html()
    df['Age'] = df[['Age', 'Pclass']].apply(change_age, axis=1)

    #sns for heatmap ploting for handeled values
    plt.figure(figsize=(5, 5))
    sns.heatmap(df.isnull(), cbar=True, cmap='crest')
    plt.title('Handeled Values Heatmap')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    handel_image_base64 = base64.b64encode(image_png).decode('utf-8')
    
    # Draw histogram for age of survivors
    plt.figure(figsize=(10, 6))
    sns.histplot(df[df['Survived'] == 1]['Age'], bins=20, kde=False, color='blue', label='Survived')
    plt.title('Age Distribution of Survivors')
    plt.xlabel('Age')
    plt.ylabel('Count')
    plt.legend()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    survived_image_base64 = base64.b64encode(image_png).decode('utf-8')

    # Draw histogram for survival by gender
    plt.figure(figsize=(6, 6))
    sns.countplot(data=df, x='Survived', hue='Sex')
    plt.title('Survival Count by Gender')
    plt.xlabel('Survived')
    plt.ylabel('Count')
    plt.legend(title='Sex', labels=['Female', 'Male'])
    plt.xticks(ticks=[0, 1], labels=['No', 'Yes'])
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    survived_gender_image_base64 = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'analyze.html', {
        'head': head_html,
        # 'tail': tail_html,
        'summary': summary_html,
        'missing' : filtered_missing,
        'heatmap': image_base64,
        'train': df.head(3).to_html(),
        'handeled': handel_image_base64,
        'relate': create_age_pclass_html,
        'histogram_survived':survived_image_base64,
        'histogram_survived_gender':survived_gender_image_base64
    })
