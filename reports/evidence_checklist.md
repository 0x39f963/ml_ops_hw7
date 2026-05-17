# Evidence checklist

Файл для фиксации результатов после внешних pipeline и локального smoke.

## Ссылки на pipeline

- GitHub Actions CI:
- GitHub Actions deploy:
- GitLab pipeline:

## Локальные проверки

- Blue `/health`: `screenshots/health-blue.png`
- Green `/health`: `screenshots/health-green.png`
- Green `/predict`: `screenshots/predict-green.png`
- Proxy после switch на Green:
- Proxy после rollback на Blue: `screenshots/proxy-rollback-blue.png`

## Команды

```bash
python3 -m compileall -q app ml_pipeline.py model_gate.py
python3 ml_pipeline.py
python3 model_gate.py
pytest -q
scripts/local_blue_green_smoke.sh
```

## Заметки

- `reports/offline_metrics.json` создается после обучения
- k6 можно запустить отдельно, если он установлен
- основные артефакты проверки: GitHub/GitLab pipeline и ответы API
