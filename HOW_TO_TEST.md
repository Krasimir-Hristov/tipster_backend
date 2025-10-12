# 🧪 Как да тестваш The Odds API интеграцията

## ⚠️ ВАЖНО: Трябват ДВА терминала!

### Терминал 1: Django Сървър (оставяш го да работи)

```powershell
cd D:\myProjects\tipster_backend
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

**📌 НЕ ЗАТВАРЯЙ този терминал! Остави сървъра да работи.**

Ще видиш:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

### Терминал 2: Тестове

Отвори **НОВ PowerShell прозорец** и пусни:

```powershell
cd D:\myProjects\tipster_backend
.\.venv\Scripts\Activate.ps1
python test_odds_api_format.py
```

---

## 📋 Или тествай с curl/Postman:

### Test 1: The Odds API формат (ПРЕПОРЪЧИТЕЛЕН)

```powershell
curl -X POST http://localhost:8000/api/analyze/ `
  -H "Content-Type: application/json" `
  -d '{
    "id": "test_match_001",
    "sport_key": "soccer_uefa_european_championship_qualifying",
    "sport_title": "UEFA Euro Qualifying",
    "commence_time": "2025-10-12T19:00:00Z",
    "home_team": "Turkey",
    "away_team": "Bulgaria"
  }'
```

### Test 2: Legacy формат (също работи)

```powershell
curl -X POST http://localhost:8000/api/analyze/ `
  -H "Content-Type: application/json" `
  -d '{
    "team1": "Spain",
    "team2": "Bulgaria"
  }'
```

---

## 🎯 Очакван резултат:

```json
{
  "success": true,
  "team1": "Turkey",
  "team2": "Bulgaria",
  "match_id": "test_match_001",
  "commence_time": "2025-10-12T19:00:00Z",
  "sport_key": "soccer_uefa_european_championship_qualifying",

  "analysis": {
    "goals_prediction": "...",
    "winner_prediction": "...",
    "score_prediction": "...",
    "final_analysis": "...",
    "research_data": "..."
  },

  "team1_stats": {
    "name": "Turkey",
    "recent_matches": [...],
    "form": "WWLWD",
    "avg_goals_scored": 2.1,
    "avg_goals_conceded": 1.2
  },

  "team2_stats": {
    "name": "Bulgaria",
    "recent_matches": [...],
    "form": "LLDLL",
    "avg_goals_scored": 0.6,
    "avg_goals_conceded": 2.8
  },

  "head_to_head": {
    "total_matches": 10,
    "team1_wins": 6,
    "team2_wins": 2,
    "draws": 2,
    "recent_matches": [...]
  }
}
```

---

## ❌ Ако видиш грешка "Connection refused":

**Проблем:** Django сървърът не работи!

**Решение:** Отвори Терминал 1 и стартирай сървъра:

```powershell
python manage.py runserver
```

**НЕ ЗАТВАРЯЙ** този терминал докато тестваш!

---

## 💡 Frontend интеграция (Next.js пример):

```javascript
// Get match from The Odds API
const match = {
  id: 'abc123',
  sport_key: 'soccer_epl',
  commence_time: '2025-10-15T15:00:00Z',
  home_team: 'Manchester United',
  away_team: 'Liverpool',
};

// Send to backend
const response = await fetch('http://localhost:8000/api/analyze/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(match),
});

const data = await response.json();
console.log('Analysis:', data.analysis);
console.log('Stats:', data.team1_stats, data.team2_stats);
console.log('H2H:', data.head_to_head);
```

---

## 🚀 Production deployment:

Когато деплойваш на production, използвай **Gunicorn** вместо `manage.py runserver`:

```bash
pip install gunicorn
gunicorn tipster_project.wsgi:application --bind 0.0.0.0:8000
```
