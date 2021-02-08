"""
Super duper simple and quick API for serving machine learning model predictions on rainfall
Can predict for Hobart, Melbourne and Sydney
"""
from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load

class PredictionPayload(BaseModel):
    """
    The base model used for passing data to the predictor. Declaring this allows FastAPI to handle all sorts
    of validation and generate clean errors if the incoming data does not match our model
    """
    WindGustSpeed: float
    HumitidtyThreePm: float
    PressureThreePm: float
    TempThreePm: float
    RainToday: int
    WindDirThreePm: int

# Start the instance
app = FastAPI()

"""
In this instance for speed we can load the models into memory and it won't cause too much concern.
The rain prediction models are pretty small in comparison to some complex image recognition or text generation models
Loading from these also means we don't need to import any other dependencies 
"""
hobart_ml_model = load('ml_models/hobart_rain_prediction_model.joblib')
melbourne_ml_model = load('ml_models/melbourne_rain_prediction_model.joblib')
sydney_ml_model = load('ml_models/sydney_rain_prediction_model.joblib')

@app.get("/")
async def root():
    return {"message": "Hi, I will predict rain for you. Get /help if you need some guidance"}

@app.get("/help")
async def help():
    return {"message": "Navigate to docs at /docs ✌"}

@app.get("/predict/hobart")
async def hobart():
    return {"message": "Please post to this route to receive some top notch predictions"}


"""
The routes below are the ones that will generate a rain prediction when posted to
"""

@app.post("/predict/hobart")
async def predict_hobart(payload: PredictionPayload):
    prediction = hobart_ml_model.predict([[payload.WindGustSpeed, payload.HumitidtyThreePm, payload.PressureThreePm, 
                                        payload.TempThreePm, payload.RainToday, payload.WindDirThreePm]])
    return {'prediction': prediction}


@app.post("/predict/melbourne")
async def predict_melbourne(payload: PredictionPayload):
    prediction = melbourne_ml_model.predict([[payload.WindGustSpeed, payload.HumitidtyThreePm, payload.PressureThreePm, 
                                        payload.TempThreePm, payload.RainToday, payload.WindDirThreePm]])
    return {'prediction': prediction}

@app.post("/predict/sydney")
async def predict_sydney(payload: PredictionPayload):    
    prediction = sydney_ml_model.predict([[payload.WindGustSpeed, payload.HumitidtyThreePm, payload.PressureThreePm, 
                                        payload.TempThreePm, payload.RainToday, payload.WindDirThreePm]])
    return {'prediction': prediction}