"""
Super duper simple and quick API for serving machine learning model predictions on rainfall
Can predict for Hobart, Melbourne and Sydney
"""
from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from pydantic import BaseModel
from joblib import load
import psycopg2
import os

class PredictionPayload(BaseModel):
    """
    The base model used for passing data to the predictor. Declaring this allows FastAPI to handle all sorts
    of validation and generate clean errors if the incoming data does not match our model
    """
    WindGustSpeed: float
    HumidityThreePm: float
    PressureThreePm: float
    TempThreePm: float
    RainToday: int
    WindDirThreePm: int

origins = ['*']

middleware = [Middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])]

# Start the instance
app = FastAPI(middleware=middleware)


"""
In this instance for speed we can load the models into memory and it won't cause too much concern.
The rain prediction models are pretty small in comparison to some complex image recognition or text generation models
"""
hobart_ml_model = load('ml_models/hobart_rain_prediction_model.joblib')
melbourne_ml_model = load('ml_models/melbourne_rain_prediction_model.joblib')
sydney_ml_model = load('ml_models/sydney_rain_prediction_model.joblib')

@app.get("/")
async def root():
    return {"message": "Hi, I will predict rain for you. Get /help if you need some guidance"}

"""
The routes below are the ones that will generate a rain prediction when posted to
"""

@app.post("/predict/hobart")
async def predict_hobart(payload: PredictionPayload):
    prediction = hobart_ml_model.predict([[payload.WindGustSpeed, payload.HumitidtyThreePm, payload.PressureThreePm, 
                                        payload.TempThreePm, payload.RainToday, payload.WindDirThreePm]])
    return {'prediction': prediction[0]}


@app.post("/predict/melbourne")
async def predict_melbourne(payload: PredictionPayload):
    prediction = melbourne_ml_model.predict([[payload.WindGustSpeed, payload.HumitidtyThreePm, payload.PressureThreePm, 
                                        payload.TempThreePm, payload.RainToday, payload.WindDirThreePm]])
    return {'prediction': prediction[0]}

@app.post("/predict/sydney")
async def predict_sydney(payload: PredictionPayload):    
    prediction = sydney_ml_model.predict([[payload.WindGustSpeed, payload.HumitidtyThreePm, payload.PressureThreePm, 
                                        payload.TempThreePm, payload.RainToday, payload.WindDirThreePm]])
    return {'prediction': prediction[0]}


@app.get('/obs/{city}')
async def get_observations(city: str):
    print(city)
    connection = psycopg2.connect(os.environ['BOM_DATA_POSTGRES_URI'])
    cursor = connection.cursor()
    cursor.execute("""SELECT * from weatherData where location = %s ORDER BY id DESC LIMIT 1""", (city,))
    obs_data = cursor.fetchone()
    
    returning_data = {
        "WindGustSpeed": obs_data[3],
        "HumidityThreePm": obs_data[4],
        "PressureThreePm": obs_data[5],
        "TempThreePm": obs_data[6],
        "RainToday": obs_data[7],
        "WindDirThreePm": obs_data[8]
        }

    connection.close()  
    return returning_data