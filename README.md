# Rain Predictor API - Fast API

For the rain prediction app I needed an API which could receive model inputs and then turn around to deliver the predictions. It seemed like an excellent opportunity to use Fast API which is a no nonsense way to create robust APIs in record time. 

I love the automatic in-built error handling that Fast provides, once an API model is defined it handles pretty much everything else! You just need to specify the route. 

There is one downfall to this implementation, which would definitely hurt the app if the models became more complex. In reality, the prediction step should be shifted into a Celery worker which then publishes to a Redis database. The frontend receives a key to be subscribed to the Redis database event. When the prediction completes, Celery would publish the result and Redis notifies the subscribers. 

Lastly, considering the current state of the app, the smartest option would to be just complete the predictions within the BOM scraper worker - but that'd be no fun 🤷‍♂️😁

