# 🏆 Tipster Backend API Documentation

## 📋 Общ преглед

Django REST API за анализ на футболни мачове използвайки AI агенти с LangGraph и множество LLM модели.

**Base URL:** `http://localhost:8000`

**🇧🇬 Език на отговорите:** Всички AI анализи се генерират на **БЪЛГАРСКИ ЕЗИК**

**Технологии:**

- Django 5.2.7
- Django REST Framework
- LangGraph (multi-agent workflow)
- Google Gemini 2.0 Flash & Thinking
- Tavily Search API

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

#### **Endpoint:**

```
POST /api/analyze/
```

#### **Request Headers:**

```http
Content-Type: application/json
```

#### **Request Body:**

```json
{
  "team1": "Kosovo",
  "team2": "Slovenia"
}
```

#### **Request Body Parameters:**

| Parameter | Type   | Required | Description                     |
| --------- | ------ | -------- | ------------------------------- |
| `team1`   | string | ✅ Yes   | Име на първия отбор (home team) |
| `team2`   | string | ✅ Yes   | Име на втория отбор (away team) |

#### **Success Response (200 OK):**

```json
{
  "success": true,
  "team1": "Kosovo",
  "team2": "Slovenia",
  "analysis": {
    "goals_prediction": "Косово има силна домакинска форма и се нуждае от точки в световните квалификации, което предполага че ще атакуват активно, докато Словения има слаба защита и е уязвима. Въпреки това, Косово ще липсва ключов защитник Рахмани, което може да отвори възможности за Словения да вкара гол. Предвид тези фактори, очаква се умерен брой голове.\n\nОчаквани голове: 2-3 общо",

    "winner_prediction": "Косово има силна домакинска форма и по-високо класиране в групата, което им дава лек превес. Въпреки контузиите, слабата форма на Словения и техните взаимни резултати предполагат че ще им бъде трудно. Косово ще спечели.",

    "score_prediction": "Силната домакинска форма на Косово и проблемите на Словения в групата предполагат лек превес за домакините. Липсата на ключови играчи като Рахмани може да засегне отбраната им, но атакуващата мощ на Косово трябва да бъде достатъчна за тясна победа.\n\nПрогнозиран резултат: Косово 2-1 Словения",

    "final_analysis": "**Финална прогноза за мача: Косово срещу Словения**\n\n**Преглед на ключовите фактори:**\n\nТази квалификация за Световното първенство изправя Косово, в момента второ място в Група Б, срещу Словения на четвърто място...\n\n**Финална прогноза:**\n- **Победител:** Косово\n- **Резултат:** Косово 2-1 Словения\n- **Ниво на увереност:** Средно-високо",

    "research_data": "=== Research Data for Kosovo vs Slovenia ===\n\n1. Kosovo v Slovenia LIVE 10/10/2025 | Football - Flashscore.com\n   Source: https://www.flashscore.com/match/...\n   Kosovo are without a few players due to injury..."
  }
}
```

**ВАЖНО:** Всички AI анализи (goals_prediction, winner_prediction, score_prediction, final_analysis) ще бъдат на **БЪЛГАРСКИ ЕЗИК**.

#### **Response Fields:**

| Field                        | Type    | Description                                  |
| ---------------------------- | ------- | -------------------------------------------- |
| `success`                    | boolean | Дали заявката е успешна                      |
| `team1`                      | string  | Име на първия отбор                          |
| `team2`                      | string  | Име на втория отбор                          |
| `analysis.goals_prediction`  | string  | AI анализ за очаквания брой голове           |
| `analysis.winner_prediction` | string  | AI предвиждане кой отбор ще спечели          |
| `analysis.score_prediction`  | string  | AI предвиждане на точния резултат            |
| `analysis.final_analysis`    | string  | Финален агрегиран анализ от главния AI агент |
| `analysis.research_data`     | string  | Събрани данни от уеб търсене (Tavily API)    |

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

### **Workflow Flow:**

```
START
  ↓
gather_data (Tavily Search)
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
import { analyzeMatch } from '@/lib/api';

export default function Home() {
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    const data = await analyzeMatch('Kosovo', 'Slovenia');
    setResult(data);
  };

  return (
    <div>
      <button onClick={handleAnalyze}>Analyze Match</button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
```

---

## 📞 Support

Ако имаш въпроси или проблеми:

1. Провери този документ
2. Прегледай Django server logs в terminal
3. Провери browser console за frontend errors
4. Тествай с `test_api.py` скрипта

---

**Last Updated:** October 12, 2025
**API Version:** 1.0.0
**Django Version:** 5.2.7
