# Disaster-Response-Pipeline-using-SVC

   1)Description of the Project
   
   This research uses Natural Language Processing (NLP) techniques to categorize texts sent during a crisis. Every communication will be examined and assigned to one of 36 distinct categories, including those pertaining to missing persons, complaints of infrastructure damage, or calls for medical assistance. By guaranteeing that every message is routed to the proper response team, this thorough classification will aid in expediting emergency response activities.

    The first step was to clean the data and store it in a database table. We then used the data to train a classifier 
    model after it has been saved, using grid search to choose the best hyperparameters. The model was be stored for     further use when it has been trained. Lastly, a web application will be created to show training data       
    visualizations and identify new messages.

     - genre
     - related
     - request
     - offer
     - aid_related
     - medical_help
     - medical_products
     - search_and_rescue
     - security
     - military
     - child_alone
     - water
     - food
     - shelter
     - clothing
     - money
     - missing_people
     - refugees
     - death
     - other_aid
     - infrastructure_related
     - transport
     - buildings
     - electricity
     - tools
     - hospitals
     - shops
     - aid_centers
     - other_infrastructure
     - weather_related
     - floods
     - storm
     - fire
     - earthquake
     - cold
     - other_weather
     - direct_report

    2) Project Libraries
        - flask: Framework use in developing the web applications.
        - Linear Support Vector machine: Machine learning package that includes the classifier for model training.
        - nltk: Employed for tokenizing and processing text data for model training.
        - pandas: Assists in data manipulation and model training.
        - pickle: Used to save the final trained model.
        - plotly: Package for data visualizations.
        - sklearn: Machine learning package used for training and enhancing the model.
        - SQLalchemy: Utilized for querying the database and storing data.
      
    3) Running the project
       Root Directory:
        - App
          - templates
          - go.html: Renders the model output
          - master.html: index of webapp, renders graphs
          - run.py: houses flask app, and initialises web app
        - Data
          - categories.csv: category data
          - messages.csv: messages data
          - Disaster.db: SQLite DB to save data
          - process_data.py: executed file to clean and save data
        - Models
          - train_classifier: trains and saves the classifier model
         
     4) To execute the project a terminal is used. Install all the necessary packages in your environment. To run the project, follow these steps
        
          a. Run the command to run the ETL pipeline to clean data and save it into the DB.
        
            - python3 data/process_data.py data/messages.csv data/categories.csv data/DisasterResponse.DB
        
          b. Run the command to run the classifier and save the model.
        
            - python3 models/train_classifier.py data/DisasterResponse.DB models/new_best_model.plk
    
          c. Run the command to view the APP and classify messages
    
            - python3 app/run.py 
