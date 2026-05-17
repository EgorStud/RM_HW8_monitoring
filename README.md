# HW8 Monitoring: ML Service

## SLO
- Latency (p95) < 1 сек
- Error Rate < 1%
- Availability > 99%

## Запуск
```bash
docker compose up -d
```

## Компоненты
- **ML-сервис** (FastAPI) — порт 8000, эндпоинты /health, /predict, /metrics
- **Prometheus** — порт 9090, сбор метрик с ML-сервиса
- **Grafana** — порт 3000, дашборд p95 Latency, алерт при превышении 1 сек

## Проверка
```bash
curl http://localhost:8000/health
curl http://localhost:8000/predict
```

## MLflow UI
http://localhost:3000 (admin/admin)
