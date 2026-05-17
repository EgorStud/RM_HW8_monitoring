from fastapi import FastAPI
from prometheus_client import Histogram, Counter, make_asgi_app
import time
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

app = FastAPI()

# Prometheus метрики
LATENCY = Histogram("request_latency_seconds", "Request latency")
PREDICTIONS = Counter("predictions_total", "Total predictions made")

# Обучение модели при старте
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Подключение /metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/predict")
def predict():
    start = time.time()
    sample = X_test[np.random.randint(0, len(X_test))].reshape(1, -1)
    prediction = model.predict(sample)
    LATENCY.observe(time.time() - start)
    PREDICTIONS.inc()
    return {"prediction": int(prediction[0])}

@app.get("/predict_slow")
def predict_slow():
    start = time.time()
    # Искусственная задержка для проверки алерта
    time.sleep(2)
    sample = X_test[np.random.randint(0, len(X_test))].reshape(1, -1)
    prediction = model.predict(sample)
    LATENCY.observe(time.time() - start)
    PREDICTIONS.inc()
    return {"prediction": int(prediction[0])}
