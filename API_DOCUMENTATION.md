# 🏆 Tipster Backend API Documentation

## 📋 Общ преглед

Django REST API за анализ на футболни мачове използвайки AI агенти с LangGraph и множество LLM модели.

**Base URL:** `http://localhost:8000`

**🇧🇬 Език на отговорите:** Всички AI анализи се генерират на **БЪЛГАРСКИ ЕЗИК**

**✨ Version:** 1.2.0 - **NEW: The Odds API Integration!**

**Технологии:**

- Django 5.2.7
- Django REST Framework
- LangGraph (multi-agent workflow)
- Google Gemini 2.0 Flash & Thinking
- Tavily Search API
- **The Odds API** (match data source)

---

## 🚀 Как да стартираш сървъра

### 1. Активирай виртуалната среда:

```powershell
cd d:\myProjects\tipster_backend
.\.venv\Scripts\Activate.ps1
```

### 2. Стартирай Django сървъра:

```powershell
python manage.py runserver
```

### 3. Сървърът ще работи на:

```
http://127.0.0.1:8000/
http://localhost:8000/
```

---

## 📡 API Endpoints

### 1️⃣ **Analyze Match (POST)**

Анализира футболен мач между два отбора използвайки AI агенти.

**🎯 NEW:** Сега приема директно данни от The Odds API за точни имена и избягване на правописни грешки!

#### **Endpoint:**

```
POST /api/analyze/
```

#### **Request Headers:**

```http
Content-Type: application/json
```

#### **Request Body (The Odds API Format - ПРЕПОРЪЧИТЕЛЕН):**

```json
{
  "id": "abc123xyz789",
  "sport_key": "soccer_uefa_european_championship_qualifying",
  "sport_title": "UEFA Euro Qualifying",
  "commence_time": "2025-10-12T19:00:00Z",
  "home_team": "Turkey",
  "away_team": "Bulgaria"
}
```

#### **Request Body (Legacy Format - също поддържан):**

```json
{
  "team1": "Turkey",
  "team2": "Bulgaria"
}
```

#### **Request Body Parameters:**

| Parameter       | Type   | Required                    | Description                                    |
| --------------- | ------ | --------------------------- | ---------------------------------------------- |
| `id`            | string | ⭐ Recommended (Odds API)   | Уникален идентификатор на мача от The Odds API |
| `sport_key`     | string | ⭐ Recommended              | Ключ на спорта (напр. `soccer_epl`)            |
| `commence_time` | string | ⭐ Recommended              | ISO 8601 timestamp на началото на мача         |
| `home_team`     | string | ✅ Yes (or team1)           | Име на домакина (ТОЧНО от The Odds API)        |
| `away_team`     | string | ✅ Yes (or team2)           | Име на гостите (ТОЧНО от The Odds API)         |
| `team1`         | string | ✅ Yes (legacy format only) | Име на първия отбор                            |
| `team2`         | string | ✅ Yes (legacy format only) | Име на втория отбор                            |

**💡 Защо The Odds API формат е по-добър:**

- ✅ Точни имена на отборите (без правописни грешки)
- ✅ Избягва неексистиращи мачове
- ✅ Допълнителна информация (време, спорт)
- ✅ Уникален ID за tracking

#### **Success Response (200 OK):**

```json
{
  "success": true,
  "team1": "Turkey",
  "team2": "Bulgaria",
  "match_id": "abc123xyz789",
  "commence_time": "2025-10-12T19:00:00Z",
  "sport_key": "soccer_uefa_european_championship_qualifying",

  "analysis": {
    "goals_prediction": "Турция демонстрира изключителна атакуваща форма с 6 гола в последния мач срещу България, докато българската защита е много уязвима след като пропусна 6 гола. Предвид тази разлика във форма, очаква се много голове.\n\nОчаквани голове: 4+ общо",

    "winner_prediction": "Турция има подавляваща форма и доминация над България в последните мачове. България показва много слаба форма и защита. Турция ще спечели убедително.",

    "score_prediction": "Силната атакуваща форма на Турция (6 гола последно) и слабата защита на България (6 пропуснати) предполагат ясна доминация. Турция играе у дома, което дава допълнително предимство.\n\nПрогнозиран резултат: Турция 4-1 България",

    "final_analysis": "**Финална прогноза за мача: Турция срещу България**\n\n**Преглед на ключовите фактори:**\n\nТурция демонстрира изключителна форма с 6 гола в последния мач...\n\n**Финална прогноза:**\n- **Победител:** Турция\n- **Резултат:** Турция 4-1 България\n- **Ниво на увереност:** Високо",

    "research_data": "=== Research Data for Turkey vs Bulgaria ===\n\n1. Turkey demolishes Bulgaria 6-1..."
  },

  "team1_stats": {
    "name": "Turkey",
    "recent_matches": [
      {
        "date": "2025-10-11",
        "opponent": "Bulgaria",
        "score": "6-1",
        "home_away": "away",
        "result": "win",
        "goals_scored": 6,
        "goals_conceded": 1
      },
      {
        "date": "2025-09-10",
        "opponent": "Iceland",
        "score": "3-1",
        "home_away": "home",
        "result": "win",
        "goals_scored": 3,
        "goals_conceded": 1
      }
      // ... до 10 мача общо
    ],
    "form": "WWWWDL",
    "total_goals_scored": 24,
    "total_goals_conceded": 8,
    "avg_goals_scored": 2.4,
    "avg_goals_conceded": 0.8,
    "matches_analyzed": 10
  },

  "team2_stats": {
    "name": "Bulgaria",
    "recent_matches": [
      {
        "date": "2025-10-11",
        "opponent": "Turkey",
        "score": "1-6",
        "home_away": "home",
        "result": "loss",
        "goals_scored": 1,
        "goals_conceded": 6
      },
      {
        "date": "2025-09-09",
        "opponent": "Georgia",
        "score": "0-2",
        "home_away": "away",
        "result": "loss",
        "goals_scored": 0,
        "goals_conceded": 2
      }
      // ... до 10 мача общо
    ],
    "form": "LLLDLL",
    "total_goals_scored": 6,
    "total_goals_conceded": 22,
    "avg_goals_scored": 0.6,
    "avg_goals_conceded": 2.2,
    "matches_analyzed": 10
  },

  "head_to_head": {
    "total_matches": 15,
    "team1_wins": 8,
    "draws": 3,
    "team2_wins": 4,
    "recent_matches": [
      {
        "date": "2025-10-11",
        "home_team": "Bulgaria",
        "away_team": "Turkey",
        "score": "1-6",
        "winner": "Turkey"
      },
      {
        "date": "2024-11-15",
        "home_team": "Turkey",
        "away_team": "Bulgaria",
        "score": "3-0",
        "winner": "Turkey"
      }
      // ... до 10 H2H мача
    ]
  }
}
```

**ВАЖНО:** Всички AI анализи (goals_prediction, winner_prediction, score_prediction, final_analysis) ще бъдат на **БЪЛГАРСКИ ЕЗИК**.

**НОВО (v1.1.0):** API сега връща **structured data** за последни мачове и head-to-head статистики, готови за визуализация във frontend!

#### **Response Fields:**

| Field                              | Type    | Description                                         |
| ---------------------------------- | ------- | --------------------------------------------------- |
| `success`                          | boolean | Дали заявката е успешна                             |
| `team1`                            | string  | Име на първия отбор                                 |
| `team2`                            | string  | Име на втория отбор                                 |
| **Analysis (AI Predictions)**      |         |                                                     |
| `analysis.goals_prediction`        | string  | AI анализ за очаквания брой голове (на български)   |
| `analysis.winner_prediction`       | string  | AI предвиждане кой отбор ще спечели (на български)  |
| `analysis.score_prediction`        | string  | AI предвиждане на точния резултат (на български)    |
| `analysis.final_analysis`          | string  | Финален агрегиран анализ (на български)             |
| `analysis.research_data`           | string  | Събрани данни от уеб търсене (Tavily API)           |
| **Team1 Stats (Structured)**       |         | **НОВО в v1.1.0** - Structured data за визуализация |
| `team1_stats.name`                 | string  | Име на първия отбор                                 |
| `team1_stats.recent_matches`       | array   | Последни 10 мача (ако има данни)                    |
| `team1_stats.form`                 | string  | Форма като "WWLDW" (W=win, L=loss, D=draw)          |
| `team1_stats.total_goals_scored`   | number  | Общо вкарани голове в анализираните мачове          |
| `team1_stats.total_goals_conceded` | number  | Общо пропуснати голове                              |
| `team1_stats.avg_goals_scored`     | number  | Средно вкарани голове на мач                        |
| `team1_stats.avg_goals_conceded`   | number  | Средно пропуснати голове на мач                     |
| `team1_stats.matches_analyzed`     | number  | Брой анализирани мачове                             |
| **Team2 Stats (Structured)**       |         | Същата структура като team1_stats                   |
| `team2_stats.*`                    |         | (виж team1_stats за детайли)                        |
| **Head-to-Head Data**              |         | **НОВО в v1.1.0** - H2H история                     |
| `head_to_head.total_matches`       | number  | Общо мачове между двата отбора (historical)         |
| `head_to_head.team1_wins`          | number  | Победи на team1                                     |
| `head_to_head.draws`               | number  | Равенства                                           |
| `head_to_head.team2_wins`          | number  | Победи на team2                                     |
| `head_to_head.recent_matches`      | array   | Последни 10 H2H мача (ако има данни)                |

---

#### **Структура на `recent_matches` обект:**

Всеки мач в `team1_stats.recent_matches` или `team2_stats.recent_matches`:

```json
{
  "date": "2025-10-11", // Дата на мача (YYYY-MM-DD)
  "opponent": "Bulgaria", // Противник
  "score": "6-1", // Резултат
  "home_away": "away", // "home" или "away"
  "result": "win", // "win", "loss", или "draw"
  "goals_scored": 6, // Вкарани голове
  "goals_conceded": 1 // Пропуснати голове
}
```

---

#### **Структура на `head_to_head.recent_matches` обект:**

Всеки H2H мач:

```json
{
  "date": "2025-10-11", // Дата на мача
  "home_team": "Bulgaria", // Домакин
  "away_team": "Turkey", // Гост
  "score": "1-6", // Резултат
  "winner": "Turkey" // "Turkey", "Bulgaria", или "Draw"
}
```

---

#### **Handling Missing Data:**

Ако няма достатъчно информация за structured data:

```json
{
  "team1_stats": {
    "error": "Няма достатъчно информация",
    "available_data": null
  },
  "team2_stats": {
    "error": "Няма достатъчно информация"
  },
  "head_to_head": {
    "error": "Няма достатъчно информация"
  }
}
```

#### **Error Response (400 Bad Request):**

```json
{
  "success": false,
  "error": "Both team1 and team2 are required"
}
```

#### **Error Response (500 Internal Server Error):**

```json
{
  "success": false,
  "error": "Analysis failed: [error message]"
}
```

---

## 🤖 AI Workflow Architecture

Системата използва **LangGraph** за оркестрация на множество AI агенти:

### **1. Data Gathering Node**

- **Функция:** `search_web_tavily()`
- **Модел:** Tavily Search API
- **Цел:** Събира актуална информация за мача от интернет
- **Output:** 5 релевантни източника с новини, статистики, квоти

### **2. Goals Analyzer Node**

- **Функция:** `analyze_goals()`
- **Модел:** `gemini-2.0-flash-exp`
- **Цел:** Анализира вероятния брой голове (Over/Under)
- **Prompt:** Използва research data за предвиждане на общ брой голове

### **3. Winner Analyzer Node**

- **Функция:** `analyze_winner()`
- **Модел:** `gemini-2.0-flash-exp`
- **Цел:** Предвижда кой отбор ще спечели
- **Prompt:** Анализира форма, статистики, Head-to-Head

### **4. Score Analyzer Node**

- **Функция:** `analyze_score()`
- **Модел:** `gemini-2.0-flash-exp`
- **Цел:** Предвижда точния резултат
- **Prompt:** Комбинира всички фактори за конкретен резултат

### **5. Aggregator Node**

- **Функция:** `aggregate_analysis()`
- **Модел:** `gemini-2.0-flash-thinking-exp` (по-мощен модел)
- **Цел:** Обединява всички анализи в финално предвиждане
- **Prompt:** Синтезира информация от всички агенти и дава финално заключение
- **Език на отговор:** 🇧🇬 **БЪЛГАРСКИ**

**⚠️ ВАЖНО:** Всички AI агенти са инструктирани да отговарят на **БЪЛГАРСКИ ЕЗИК**. Всички анализи (goals_prediction, winner_prediction, score_prediction, final_analysis) ще бъдат на български.

### **6. Data Parser Node** ✨ NEW in v1.1.0

- **Функция:** `parse_structured_data()`
- **Модел:** `gemini-2.0-flash-exp`
- **Цел:** Извлича structured data от research text
- **Output:** team1_stats, team2_stats, head_to_head (JSON format)
- **Scope:** Последни 10 мача за всеки отбор + последни 10 H2H мача

### **Workflow Flow:**

```
START
  ↓
gather_data (Tavily Search - 3 searches)
  ↓
parse_data (Extract structured JSON) ✨ NEW
  ↓
analyze_goals (Gemini Flash)
  ↓
analyze_winner (Gemini Flash)
  ↓
analyze_score (Gemini Flash)
  ↓
aggregate (Gemini Thinking)
  ↓
END
```

---

## 🔧 CORS Configuration

Backend-ът е конфигуриран да приема requests от Next.js frontend:

### **Allowed Origins:**

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Next.js dev server
    'http://127.0.0.1:3000',
]
```

### **Allowed Methods:**

- GET
- POST
- PUT
- PATCH
- DELETE
- OPTIONS

### **Allowed Headers:**

- `Content-Type`
- `Authorization`
- `Accept`
- `Origin`
- `X-Requested-With`
- `X-CSRFToken`

---

## 📦 Environment Variables

Създай `.env` файл в root директорията:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

**Къде да получиш API ключове:**

- **Google Gemini:** https://aistudio.google.com/apikey
- **Tavily Search:** https://tavily.com/

---

## 🧪 Тестване на API-то

### **Вариант 1: С `curl` (PowerShell)**

```powershell
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    team1 = "Kosovo"
    team2 = "Slovenia"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/analyze/" `
    -Method POST `
    -Headers $headers `
    -Body $body
```

### **Вариант 2: С Python test script**

```powershell
python test_api.py
```

### **Вариант 3: От Next.js Frontend**

```javascript
const analyzeMatch = async (team1, team2) => {
  const response = await fetch('http://localhost:8000/api/analyze/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ team1, team2 }),
  });

  if (!response.ok) {
    throw new Error('Analysis failed');
  }

  return await response.json();
};

// Използване:
const result = await analyzeMatch('Kosovo', 'Slovenia');
console.log(result.analysis.final_analysis);
```

---

## 📊 Rate Limits

### **Google Gemini Free Tier:**

- **gemini-2.0-flash-exp:** 15 requests/minute
- **gemini-2.0-flash-thinking-exp:** 15 requests/minute

### **Tavily Search Free Tier:**

- **1000 requests/month**

**Забележка:** При надвишаване на лимита ще получиш 429 (Too Many Requests) грешка.

---

## 🗂️ Project Structure

```
tipster_backend/
├── manage.py                    # Django management script
├── db.sqlite3                   # SQLite database
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (не commitvай!)
├── API_DOCUMENTATION.md         # Този файл
│
├── tipster_project/
│   ├── settings.py              # Django settings (CORS config тук)
│   ├── urls.py                  # Main URL routing
│   └── wsgi.py
│
└── api/
    ├── views.py                 # API endpoint handlers
    ├── urls.py                  # API URL routing
    ├── models.py
    │
    └── agent/                   # AI Agent modules
        ├── __init__.py          # Package exports
        ├── state.py             # GraphState definition
        ├── tools.py             # Data collection (Tavily)
        ├── analyzers.py         # 3 Gemini analyzers
        ├── aggregator.py        # Main aggregator
        └── graph.py             # LangGraph workflow
```

---

## 🐛 Common Issues & Solutions

### **1. ERR_CONNECTION_REFUSED**

**Проблем:** Frontend не може да се свърже със сървъра

**Решение:**

```powershell
# Провери дали сървърът работи:
python manage.py runserver

# Трябва да видиш:
# Starting development server at http://127.0.0.1:8000/
```

### **2. CORS Error**

**Проблем:** Browser блокира requests заради CORS

**Решение:** Провери че в `settings.py` има:

```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',  # Преди CommonMiddleware!
    ...
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]
```

### **3. 400 Bad Request**

**Проблем:** Липсващи или невалидни параметри

**Решение:** Провери че изпращаш:

```json
{
  "team1": "Kosovo",
  "team2": "Slovenia"
}
```

### **4. 500 Internal Server Error**

**Проблем:** Грешка в AI агентите или API keys

**Решение:**

- Провери `.env` файла за валидни API keys
- Провери Django terminal за detailed error logs
- Провери rate limits на Gemini/Tavily

---

## 🔐 Security Notes

### **Development:**

- ✅ DEBUG = True (за development)
- ✅ CORS разрешен само за localhost:3000
- ✅ API keys в `.env` файл (не в git!)

### **Production (TODO):**

- ⚠️ DEBUG = False
- ⚠️ ALLOWED_HOSTS = ['yourdomain.com']
- ⚠️ Използвай production WSGI server (Gunicorn)
- ⚠️ HTTPS за API requests
- ⚠️ Database migrations
- ⚠️ Static files configuration

---

## 📝 Next Steps (Frontend Integration)

### **1. Създай Next.js проект:**

```bash
npx create-next-app@latest tipster_frontend
cd tipster_frontend
```

### **2. Създай API service file:**

```javascript
// lib/api.js
export async function analyzeMatch(team1, team2) {
  const response = await fetch('http://localhost:8000/api/analyze/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ team1, team2 }),
  });

  if (!response.ok) throw new Error('Failed to analyze match');
  return response.json();
}
```

### **3. Използвай в компонент:**

```javascript
// app/page.js
'use client';
import { useState } from 'react';
import { analyzeMatch } from '@/lib/api';

export default function Home() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const data = await analyzeMatch('Turkey', 'Bulgaria');
      setResult(data);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='container mx-auto p-8'>
      <button
        onClick={handleAnalyze}
        className='bg-blue-500 text-white px-6 py-2 rounded'
        disabled={loading}
      >
        {loading ? 'Analyzing...' : 'Analyze Match'}
      </button>

      {result && (
        <div className='mt-8 space-y-6'>
          {/* AI Analysis */}
          <div className='bg-white p-6 rounded shadow'>
            <h2 className='text-2xl font-bold mb-4'>Final Analysis</h2>
            <p className='whitespace-pre-wrap'>
              {result.analysis.final_analysis}
            </p>
          </div>

          {/* Team 1 Stats - NEW! */}
          {result.team1_stats && !result.team1_stats.error && (
            <div className='bg-white p-6 rounded shadow'>
              <h3 className='text-xl font-bold mb-4'>
                {result.team1_stats.name} - Recent Form
              </h3>

              {/* Form Badge */}
              <div className='mb-4'>
                <span className='text-sm text-gray-600'>Form: </span>
                <div className='inline-flex gap-1'>
                  {result.team1_stats.form.split('').map((char, idx) => (
                    <span
                      key={idx}
                      className={`w-8 h-8 flex items-center justify-center rounded ${
                        char === 'W'
                          ? 'bg-green-500 text-white'
                          : char === 'L'
                          ? 'bg-red-500 text-white'
                          : 'bg-gray-400 text-white'
                      }`}
                    >
                      {char}
                    </span>
                  ))}
                </div>
              </div>

              {/* Stats Grid */}
              <div className='grid grid-cols-2 gap-4 mb-4'>
                <div className='bg-blue-50 p-3 rounded'>
                  <p className='text-sm text-gray-600'>Avg Goals Scored</p>
                  <p className='text-2xl font-bold'>
                    {result.team1_stats.avg_goals_scored}
                  </p>
                </div>
                <div className='bg-red-50 p-3 rounded'>
                  <p className='text-sm text-gray-600'>Avg Goals Conceded</p>
                  <p className='text-2xl font-bold'>
                    {result.team1_stats.avg_goals_conceded}
                  </p>
                </div>
              </div>

              {/* Recent Matches Table */}
              <table className='w-full'>
                <thead>
                  <tr className='border-b'>
                    <th className='text-left py-2'>Date</th>
                    <th className='text-left py-2'>Opponent</th>
                    <th className='text-center py-2'>Score</th>
                    <th className='text-center py-2'>Result</th>
                  </tr>
                </thead>
                <tbody>
                  {result.team1_stats.recent_matches.map((match, idx) => (
                    <tr key={idx} className='border-b'>
                      <td className='py-2'>{match.date}</td>
                      <td className='py-2'>{match.opponent}</td>
                      <td className='text-center py-2'>{match.score}</td>
                      <td className='text-center py-2'>
                        <span
                          className={`px-2 py-1 rounded text-xs ${
                            match.result === 'win'
                              ? 'bg-green-100 text-green-800'
                              : match.result === 'loss'
                              ? 'bg-red-100 text-red-800'
                              : 'bg-gray-100 text-gray-800'
                          }`}
                        >
                          {match.result.toUpperCase()}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Team 2 Stats - Same structure */}
          {/* ... (copy team1 structure) */}

          {/* Head-to-Head - NEW! */}
          {result.head_to_head && !result.head_to_head.error && (
            <div className='bg-white p-6 rounded shadow'>
              <h3 className='text-xl font-bold mb-4'>Head-to-Head History</h3>

              {/* H2H Summary */}
              <div className='flex justify-around mb-6'>
                <div className='text-center'>
                  <p className='text-3xl font-bold text-blue-600'>
                    {result.head_to_head.team1_wins}
                  </p>
                  <p className='text-sm text-gray-600'>{result.team1} Wins</p>
                </div>
                <div className='text-center'>
                  <p className='text-3xl font-bold text-gray-600'>
                    {result.head_to_head.draws}
                  </p>
                  <p className='text-sm text-gray-600'>Draws</p>
                </div>
                <div className='text-center'>
                  <p className='text-3xl font-bold text-red-600'>
                    {result.head_to_head.team2_wins}
                  </p>
                  <p className='text-sm text-gray-600'>{result.team2} Wins</p>
                </div>
              </div>

              {/* Recent H2H Matches */}
              <table className='w-full'>
                <thead>
                  <tr className='border-b'>
                    <th className='text-left py-2'>Date</th>
                    <th className='text-left py-2'>Match</th>
                    <th className='text-center py-2'>Score</th>
                    <th className='text-center py-2'>Winner</th>
                  </tr>
                </thead>
                <tbody>
                  {result.head_to_head.recent_matches.map((match, idx) => (
                    <tr key={idx} className='border-b'>
                      <td className='py-2'>{match.date}</td>
                      <td className='py-2'>
                        {match.home_team} vs {match.away_team}
                      </td>
                      <td className='text-center py-2'>{match.score}</td>
                      <td className='text-center py-2 font-semibold'>
                        {match.winner}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

### **4. Визуализация с Chart.js (Optional):**

```bash
npm install chart.js react-chartjs-2
```

```javascript
// components/GoalsChart.js
import { Line } from 'react-chartjs-2';

export function GoalsChart({ team1Stats, team2Stats }) {
  const data = {
    labels: team1Stats.recent_matches.map(m => m.date),
    datasets: [
      {
        label: `${team1Stats.name} Goals Scored`,
        data: team1Stats.recent_matches.map(m => m.goals_scored),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
      },
      {
        label: `${team2Stats.name} Goals Scored`,
        data: team2Stats.recent_matches.map(m => m.goals_scored),
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
      }
    ]
  };

  return <Line data={data} />;
}
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
```

---

## 🎨 Frontend UI Components Guide

### **Препоръчителна структура на UI:**

```
┌─────────────────────────────────────────────────────────┐
│  🏆 Match Analysis: Turkey vs Bulgaria                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📊 AI Prediction Summary                              │
│  ┌───────────────┬───────────────┬──────────────────┐  │
│  │ Winner        │ Score         │ Total Goals      │  │
│  │ Turkey ✓      │ 4-1           │ Over 2.5 ✓       │  │
│  │ Confidence:   │ Confidence:   │ Confidence:      │  │
│  │ ⭐⭐⭐⭐⭐     │ ⭐⭐⭐⭐       │ ⭐⭐⭐⭐⭐       │  │
│  └───────────────┴───────────────┴──────────────────┘  │
│                                                         │
│  📝 Detailed Analysis (Collapsible)                    │
│  Final AI analysis text in Bulgarian...                │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  📈 Team Statistics                                     │
│                                                         │
│  Turkey                          Bulgaria               │
│  Form: W W W W D L              Form: L L D L L        │
│  ✅✅✅✅➖❌                      ❌❌➖❌❌              │
│                                                         │
│  Avg Goals: 2.4 ⚽                Avg Goals: 0.6 ⚽      │
│  Avg Conceded: 0.8 🥅            Avg Conceded: 2.2 🥅   │
│                                                         │
│  📋 Recent 5 Matches (Table)                           │
│  ┌──────────┬───────────┬────────┬────────┐           │
│  │ Date     │ Opponent  │ Score  │ Result │           │
│  ├──────────┼───────────┼────────┼────────┤           │
│  │ 10/11/25 │ Bulgaria  │ 6-1 🏆 │ WIN    │           │
│  │ 09/10/25 │ Iceland   │ 3-1 🏆 │ WIN    │           │
│  └──────────┴───────────┴────────┴────────┘           │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  ⚔️ Head-to-Head History                               │
│                                                         │
│  Turkey 8 wins  │  3 Draws  │  Bulgaria 4 wins         │
│  ████████░░░░░░░│           │  ░░░░                    │
│  53%            │  20%      │  27%                     │
│                                                         │
│  📋 Last 5 H2H Matches                                 │
│  ┌──────────┬────────────────────────┬────────┐       │
│  │ Date     │ Match                  │ Score  │       │
│  ├──────────┼────────────────────────┼────────┤       │
│  │ 10/11/25 │ Bulgaria vs Turkey     │ 1-6    │       │
│  │ 11/15/24 │ Turkey vs Bulgaria     │ 3-0    │       │
│  └──────────┴────────────────────────┴────────┘       │
│                                                         │
│  📊 Optional: Goals Chart (Line chart)                 │
│     Show goals scored trend for both teams             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Complete Frontend Integration Examples

### **1. API Service (TypeScript)**

```typescript
// lib/api/tipsterApi.ts
export interface MatchAnalysisRequest {
  // The Odds API format (RECOMMENDED)
  id?: string;
  sport_key?: string;
  sport_title?: string;
  commence_time?: string;
  home_team?: string;
  away_team?: string;

  // Legacy format (still supported)
  team1?: string;
  team2?: string;
}

export interface RecentMatch {
  date: string;
  opponent: string;
  score: string;
  home_away: 'home' | 'away';
  result: 'win' | 'loss' | 'draw';
  goals_scored: number;
  goals_conceded: number;
}

export interface TeamStats {
  name: string;
  recent_matches: RecentMatch[];
  form: string;
  total_goals_scored: number;
  total_goals_conceded: number;
  avg_goals_scored: number;
  avg_goals_conceded: number;
  matches_analyzed: number;
}

export interface H2HMatch {
  date: string;
  home_team: string;
  away_team: string;
  score: string;
  winner: string;
}

export interface HeadToHead {
  total_matches: number;
  team1_wins: number;
  draws: number;
  team2_wins: number;
  recent_matches: H2HMatch[];
}

export interface MatchAnalysisResponse {
  success: boolean;
  team1: string;
  team2: string;
  match_id?: string;
  commence_time?: string;
  sport_key?: string;
  analysis: {
    goals_prediction: string;
    winner_prediction: string;
    score_prediction: string;
    final_analysis: string;
    research_data: string;
  };
  team1_stats: TeamStats | { error: string };
  team2_stats: TeamStats | { error: string };
  head_to_head: HeadToHead | { error: string };
}

const API_BASE_URL = 'http://localhost:8000';

export async function analyzeMatch(
  request: MatchAnalysisRequest
): Promise<MatchAnalysisResponse> {
  const response = await fetch(`${API_BASE_URL}/api/analyze/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Analysis failed');
  }

  return response.json();
}

// Helper: Convert The Odds API match to request format
export function oddsApiToRequest(oddsMatch: any): MatchAnalysisRequest {
  return {
    id: oddsMatch.id,
    sport_key: oddsMatch.sport_key,
    sport_title: oddsMatch.sport_title,
    commence_time: oddsMatch.commence_time,
    home_team: oddsMatch.home_team,
    away_team: oddsMatch.away_team,
  };
}
```

---

### **2. React Components**

#### **2.1 Form Badge Component**

```tsx
// components/FormBadge.tsx
interface FormBadgeProps {
  form: string; // "WWLDW"
}

export function FormBadge({ form }: FormBadgeProps) {
  const getColor = (result: string) => {
    switch (result) {
      case 'W':
        return 'bg-green-500';
      case 'L':
        return 'bg-red-500';
      case 'D':
        return 'bg-gray-400';
      default:
        return 'bg-gray-300';
    }
  };

  const getLabel = (result: string) => {
    switch (result) {
      case 'W':
        return '✓';
      case 'L':
        return '✗';
      case 'D':
        return '=';
      default:
        return '?';
    }
  };

  return (
    <div className='flex gap-1'>
      {form.split('').map((char, idx) => (
        <div
          key={idx}
          className={`w-8 h-8 flex items-center justify-center rounded font-bold text-white ${getColor(
            char
          )}`}
          title={char === 'W' ? 'Win' : char === 'L' ? 'Loss' : 'Draw'}
        >
          {getLabel(char)}
        </div>
      ))}
    </div>
  );
}
```

#### **2.2 Team Stats Card**

```tsx
// components/TeamStatsCard.tsx
import { FormBadge } from './FormBadge';
import { TeamStats } from '@/lib/api/tipsterApi';

interface TeamStatsCardProps {
  stats: TeamStats;
  color: 'blue' | 'red';
}

export function TeamStatsCard({ stats, color }: TeamStatsCardProps) {
  const colorClasses = {
    blue: {
      bg: 'bg-blue-50',
      border: 'border-blue-200',
      text: 'text-blue-700',
      accent: 'bg-blue-500',
    },
    red: {
      bg: 'bg-red-50',
      border: 'border-red-200',
      text: 'text-red-700',
      accent: 'bg-red-500',
    },
  };

  const c = colorClasses[color];

  return (
    <div className={`${c.bg} ${c.border} border-2 rounded-lg p-6`}>
      <h3 className={`text-2xl font-bold ${c.text} mb-4`}>{stats.name}</h3>

      {/* Form */}
      <div className='mb-6'>
        <p className='text-sm text-gray-600 mb-2'>Recent Form:</p>
        <FormBadge form={stats.form} />
      </div>

      {/* Stats Grid */}
      <div className='grid grid-cols-2 gap-4 mb-6'>
        <div className='bg-white p-4 rounded shadow-sm'>
          <p className='text-xs text-gray-500 uppercase'>Avg Scored</p>
          <p className='text-3xl font-bold text-green-600'>
            {stats.avg_goals_scored.toFixed(1)} ⚽
          </p>
        </div>
        <div className='bg-white p-4 rounded shadow-sm'>
          <p className='text-xs text-gray-500 uppercase'>Avg Conceded</p>
          <p className='text-3xl font-bold text-red-600'>
            {stats.avg_goals_conceded.toFixed(1)} 🥅
          </p>
        </div>
      </div>

      {/* Recent Matches */}
      <div>
        <h4 className='font-semibold mb-3'>
          Last {Math.min(5, stats.recent_matches.length)} Matches:
        </h4>
        <div className='space-y-2'>
          {stats.recent_matches.slice(0, 5).map((match, idx) => (
            <div
              key={idx}
              className='bg-white p-3 rounded shadow-sm flex items-center justify-between'
            >
              <div className='flex-1'>
                <p className='text-sm font-semibold'>{match.opponent}</p>
                <p className='text-xs text-gray-500'>{match.date}</p>
              </div>
              <div className='text-center px-4'>
                <p className='font-bold text-lg'>{match.score}</p>
                <p className='text-xs text-gray-500'>
                  {match.home_away === 'home' ? 'Home' : 'Away'}
                </p>
              </div>
              <div>
                <span
                  className={`px-3 py-1 rounded text-xs font-semibold ${
                    match.result === 'win'
                      ? 'bg-green-100 text-green-800'
                      : match.result === 'loss'
                      ? 'bg-red-100 text-red-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {match.result.toUpperCase()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

#### **2.3 Head-to-Head Component**

```tsx
// components/HeadToHeadCard.tsx
import { HeadToHead } from '@/lib/api/tipsterApi';

interface H2HCardProps {
  h2h: HeadToHead;
  team1Name: string;
  team2Name: string;
}

export function HeadToHeadCard({ h2h, team1Name, team2Name }: H2HCardProps) {
  const team1Percentage = (h2h.team1_wins / h2h.total_matches) * 100;
  const drawPercentage = (h2h.draws / h2h.total_matches) * 100;
  const team2Percentage = (h2h.team2_wins / h2h.total_matches) * 100;

  return (
    <div className='bg-white rounded-lg shadow-lg p-6'>
      <h3 className='text-2xl font-bold text-center mb-6'>
        ⚔️ Head-to-Head History
      </h3>

      {/* Win Stats */}
      <div className='grid grid-cols-3 gap-4 mb-6'>
        <div className='text-center'>
          <p className='text-4xl font-bold text-blue-600'>{h2h.team1_wins}</p>
          <p className='text-sm text-gray-600'>{team1Name} Wins</p>
          <p className='text-xs text-gray-400'>{team1Percentage.toFixed(0)}%</p>
        </div>
        <div className='text-center'>
          <p className='text-4xl font-bold text-gray-600'>{h2h.draws}</p>
          <p className='text-sm text-gray-600'>Draws</p>
          <p className='text-xs text-gray-400'>{drawPercentage.toFixed(0)}%</p>
        </div>
        <div className='text-center'>
          <p className='text-4xl font-bold text-red-600'>{h2h.team2_wins}</p>
          <p className='text-sm text-gray-600'>{team2Name} Wins</p>
          <p className='text-xs text-gray-400'>{team2Percentage.toFixed(0)}%</p>
        </div>
      </div>

      {/* Visual Bar */}
      <div className='h-8 flex rounded-lg overflow-hidden mb-6'>
        <div
          className='bg-blue-500 flex items-center justify-center text-white text-xs font-bold'
          style={{ width: `${team1Percentage}%` }}
        >
          {team1Percentage > 15 && `${team1Percentage.toFixed(0)}%`}
        </div>
        <div
          className='bg-gray-400 flex items-center justify-center text-white text-xs font-bold'
          style={{ width: `${drawPercentage}%` }}
        >
          {drawPercentage > 10 && `${drawPercentage.toFixed(0)}%`}
        </div>
        <div
          className='bg-red-500 flex items-center justify-center text-white text-xs font-bold'
          style={{ width: `${team2Percentage}%` }}
        >
          {team2Percentage > 15 && `${team2Percentage.toFixed(0)}%`}
        </div>
      </div>

      {/* Recent H2H Matches */}
      <div>
        <h4 className='font-semibold mb-3'>
          Last {h2h.recent_matches.length} Meetings:
        </h4>
        <table className='w-full'>
          <thead>
            <tr className='border-b'>
              <th className='text-left py-2 text-sm'>Date</th>
              <th className='text-left py-2 text-sm'>Match</th>
              <th className='text-center py-2 text-sm'>Score</th>
              <th className='text-center py-2 text-sm'>Winner</th>
            </tr>
          </thead>
          <tbody>
            {h2h.recent_matches.map((match, idx) => (
              <tr key={idx} className='border-b hover:bg-gray-50'>
                <td className='py-3 text-sm'>{match.date}</td>
                <td className='py-3 text-sm'>
                  {match.home_team} vs {match.away_team}
                </td>
                <td className='text-center py-3 font-semibold'>
                  {match.score}
                </td>
                <td className='text-center py-3'>
                  <span
                    className={`px-2 py-1 rounded text-xs font-semibold ${
                      match.winner === team1Name
                        ? 'bg-blue-100 text-blue-800'
                        : match.winner === team2Name
                        ? 'bg-red-100 text-red-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {match.winner}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

#### **2.4 AI Prediction Summary**

```tsx
// components/PredictionSummary.tsx
interface PredictionSummaryProps {
  analysis: {
    goals_prediction: string;
    winner_prediction: string;
    score_prediction: string;
    final_analysis: string;
  };
}

export function PredictionSummary({ analysis }: PredictionSummaryProps) {
  // Extract key info from text (simple regex parsing)
  const extractWinner = (text: string) => {
    const match = text.match(/(\w+)\s+ще спечели/i);
    return match ? match[1] : 'Unknown';
  };

  const extractScore = (text: string) => {
    const match = text.match(/(\d+-\d+)/);
    return match ? match[1] : 'N/A';
  };

  const extractGoals = (text: string) => {
    if (text.includes('Over') || text.includes('4+')) return 'Over 2.5 ⚽';
    if (text.includes('Under')) return 'Under 2.5';
    return 'Unknown';
  };

  const winner = extractWinner(analysis.winner_prediction);
  const score = extractScore(analysis.score_prediction);
  const goals = extractGoals(analysis.goals_prediction);

  return (
    <div className='bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg shadow-xl p-6 mb-8'>
      <h2 className='text-3xl font-bold mb-6 text-center'>🏆 AI Prediction</h2>

      <div className='grid grid-cols-1 md:grid-cols-3 gap-6'>
        {/* Winner */}
        <div className='bg-white/10 backdrop-blur rounded-lg p-4 text-center'>
          <p className='text-sm opacity-80 mb-2'>Winner</p>
          <p className='text-3xl font-bold'>{winner}</p>
          <p className='text-xs opacity-70 mt-2'>⭐⭐⭐⭐⭐</p>
        </div>

        {/* Score */}
        <div className='bg-white/10 backdrop-blur rounded-lg p-4 text-center'>
          <p className='text-sm opacity-80 mb-2'>Predicted Score</p>
          <p className='text-3xl font-bold'>{score}</p>
          <p className='text-xs opacity-70 mt-2'>⭐⭐⭐⭐</p>
        </div>

        {/* Goals */}
        <div className='bg-white/10 backdrop-blur rounded-lg p-4 text-center'>
          <p className='text-sm opacity-80 mb-2'>Total Goals</p>
          <p className='text-2xl font-bold'>{goals}</p>
          <p className='text-xs opacity-70 mt-2'>⭐⭐⭐⭐⭐</p>
        </div>
      </div>

      {/* Full Analysis (Collapsible) */}
      <details className='mt-6'>
        <summary className='cursor-pointer text-sm font-semibold hover:underline'>
          📝 View Detailed Analysis (Bulgarian)
        </summary>
        <div className='mt-4 bg-white/10 backdrop-blur rounded p-4 text-sm whitespace-pre-wrap'>
          {analysis.final_analysis}
        </div>
      </details>
    </div>
  );
}
```

#### **2.5 Main Page Component**

```tsx
// app/analysis/page.tsx
'use client';

import { useState } from 'react';
import {
  analyzeMatch,
  MatchAnalysisResponse,
  oddsApiToRequest,
} from '@/lib/api/tipsterApi';
import { TeamStatsCard } from '@/components/TeamStatsCard';
import { HeadToHeadCard } from '@/components/HeadToHeadCard';
import { PredictionSummary } from '@/components/PredictionSummary';

export default function AnalysisPage() {
  const [result, setResult] = useState<MatchAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Example: Handle match from The Odds API
  const handleAnalyzeFromOddsApi = async (oddsMatch: any) => {
    setLoading(true);
    setError(null);
    try {
      const request = oddsApiToRequest(oddsMatch);
      const data = await analyzeMatch(request);
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Example: Test with hardcoded match
  const handleTestAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyzeMatch({
        id: 'test_001',
        sport_key: 'soccer_uefa_european_championship_qualifying',
        commence_time: '2025-10-12T19:00:00Z',
        home_team: 'Turkey',
        away_team: 'Bulgaria',
      });
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='container mx-auto px-4 py-8 max-w-7xl'>
      <h1 className='text-4xl font-bold text-center mb-8'>
        ⚽ Football Match Analysis
      </h1>

      {/* Test Button */}
      <div className='text-center mb-8'>
        <button
          onClick={handleTestAnalysis}
          disabled={loading}
          className='bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg shadow-lg disabled:opacity-50 disabled:cursor-not-allowed'
        >
          {loading
            ? '🔄 Analyzing...'
            : '🚀 Test Analysis (Turkey vs Bulgaria)'}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className='bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-8'>
          <p className='font-bold'>Error:</p>
          <p>{error}</p>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className='text-center py-12'>
          <div className='inline-block animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600'></div>
          <p className='mt-4 text-gray-600'>
            Analyzing match with AI agents...
          </p>
        </div>
      )}

      {/* Results */}
      {result && !loading && (
        <div className='space-y-8'>
          {/* Match Header */}
          <div className='bg-gray-800 text-white rounded-lg p-6 text-center'>
            <h2 className='text-3xl font-bold'>
              {result.team1} <span className='text-gray-400'>vs</span>{' '}
              {result.team2}
            </h2>
            {result.commence_time && (
              <p className='text-sm text-gray-400 mt-2'>
                {new Date(result.commence_time).toLocaleString()}
              </p>
            )}
          </div>

          {/* AI Prediction */}
          <PredictionSummary analysis={result.analysis} />

          {/* Team Stats Side by Side */}
          {!('error' in result.team1_stats) &&
            !('error' in result.team2_stats) && (
              <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
                <TeamStatsCard stats={result.team1_stats} color='blue' />
                <TeamStatsCard stats={result.team2_stats} color='red' />
              </div>
            )}

          {/* Head-to-Head */}
          {!('error' in result.head_to_head) && (
            <HeadToHeadCard
              h2h={result.head_to_head}
              team1Name={result.team1}
              team2Name={result.team2}
            />
          )}

          {/* Raw Data (Debug - Optional) */}
          <details className='bg-gray-100 rounded p-4'>
            <summary className='cursor-pointer font-semibold'>
              🔍 View Raw API Response (Debug)
            </summary>
            <pre className='mt-4 text-xs overflow-auto'>
              {JSON.stringify(result, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}
```

---

## 📦 Required NPM Packages

```bash
# Install Tailwind CSS (if not already installed)
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Optional: Chart.js for data visualization
npm install chart.js react-chartjs-2

# TypeScript types (if using TypeScript)
npm install -D @types/node @types/react @types/react-dom
```

---

## 🎨 Tailwind Config (tailwind.config.js)

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Custom colors for your brand
      },
    },
  },
  plugins: [],
};
```

---

## 🚀 Quick Start Checklist for Frontend Developer

- [ ] **1. Install dependencies** (`npm install`)
- [ ] **2. Copy `lib/api/tipsterApi.ts`** - TypeScript types & API client
- [ ] **3. Copy components:**
  - `FormBadge.tsx` - Win/Loss/Draw badges
  - `TeamStatsCard.tsx` - Team statistics display
  - `HeadToHeadCard.tsx` - H2H history
  - `PredictionSummary.tsx` - AI prediction summary
- [ ] **4. Create analysis page** - `app/analysis/page.tsx`
- [ ] **5. Test API connection:**

  ```bash
  # Make sure Django backend is running:
  cd ../tipster_backend
  python manage.py runserver

  # Then test frontend:
  npm run dev
  # Open http://localhost:3000/analysis
  ```

- [ ] **6. Integrate with The Odds API:**
  - Get matches from The Odds API
  - Pass match data to `analyzeMatch()` function
  - Display results using provided components

---

## 📞 Support

Ако имаш въпроси или проблеми:

1. Провери този документ
2. Прегледай Django server logs в terminal
3. Провери browser console за frontend errors
4. Тествай с `test_api.py` скрипта

---

## 📝 Changelog

### **v1.2.0** - October 12, 2025

- ✨ **NEW:** The Odds API integration (recommended format)
- ✨ **NEW:** Match ID, commence time, sport key in response
- ✨ **NEW:** Backward compatible with legacy team1/team2 format
- 📚 **NEW:** Complete frontend UI components guide with React/TypeScript examples
- 📚 **NEW:** Ready-to-use components: FormBadge, TeamStatsCard, HeadToHeadCard, PredictionSummary

### **v1.1.0** - October 12, 2025

- ✨ **NEW:** Added structured data extraction for frontend visualization
- ✨ **NEW:** `team1_stats` - Last 10 matches, form, statistics
- ✨ **NEW:** `team2_stats` - Last 10 matches, form, statistics
- ✨ **NEW:** `head_to_head` - Last 10 H2H matches and summary stats
- ✨ **NEW:** Parser node in workflow using Gemini Flash for data extraction
- 📊 **Improved:** Enhanced Tavily searches (3 searches instead of 1)
- 📊 **Improved:** AI prompts now prioritize recent form for better predictions
- 🐛 **Fixed:** Conservative predictions for dominant teams

### **v1.0.0** - October 11, 2025

- 🎉 Initial release with AI match analysis
- 🤖 Multi-agent LangGraph workflow
- 🇧🇬 Bulgarian language responses

---

**Last Updated:** October 12, 2025  
**API Version:** 1.2.0  
**Django Version:** 5.2.7
