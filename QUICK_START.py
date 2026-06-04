#!/usr/bin/env python3
"""
Quick Start Guide - Print this to terminal for reference
"""

def print_guide():
    guide = """
╔═══════════════════════════════════════════════════════════════════════╗
║                  Daily Poshan - QUICK START GUIDE                    ║
╚═══════════════════════════════════════════════════════════════════════╝

📍 LOCATION: c:\\Users\\SD\\.git\\dailyposhan

═══════════════════════════════════════════════════════════════════════

🚀 RUN LOCALLY (Pick One)

1️⃣  AUTOMATIC (Easiest) - One Command:
    python run.py
    
    Opens:
    - Frontend: http://localhost:5173
    - Backend API: http://localhost:8000/api

2️⃣  MANUAL (2 Terminals):
    
    Terminal 1:
    cd backend-django
    python manage.py runserver
    
    Terminal 2:
    cd frontend-react
    npm run dev

3️⃣  DOCKER (Production-like):
    docker-compose up --build
    
    Opens:
    - Frontend: http://localhost:5173
    - API: http://localhost/api

═══════════════════════════════════════════════════════════════════════

🧪 TEST INTEGRATION

Run the test suite:
    python test_api.py

Expected Results:
    ✅ GET /products/ (3 products found)
    ✅ POST /auth/register
    ✅ POST /auth/login
    ✅ CORS Headers

═══════════════════════════════════════════════════════════════════════

📦 FIRST TIME SETUP (Only Once)

Option A - Automated:
    python setup.py

Option B - Manual:
    1. cd backend-django && pip install -r requirements.txt
    2. python manage.py migrate
    3. cd ../frontend-react && npm install

═══════════════════════════════════════════════════════════════════════

🔌 API ENDPOINTS READY

Authentication:
    POST   /api/auth/login              Login
    POST   /api/auth/register           Register

Products:
    GET    /api/products/               All products
    GET    /api/products/{id}/          Product by ID

Orders:
    POST   /api/orders/                 Create order
    GET    /api/orders/{id}/            Order details

Payments:
    POST   /api/payments/create         Create payment
    POST   /api/payments/verify         Verify payment

Admin:
    GET    /api/admin/orders            All orders
    PUT    /api/admin/orders/{id}/status Update status

═══════════════════════════════════════════════════════════════════════

🐳 DEPLOY TO PRODUCTION

1. Update Environment Files:
   - Edit backend-django/.env.production
   - Edit frontend-react/.env.production
   
2. Set SECRET_KEY:
   python -c "import secrets; print(secrets.token_hex(32))"
   
3. Build Images:
   docker build -t dailyposhan-backend:latest ./backend-django
   docker build -t dailyposhan-frontend:latest ./frontend-react
   
4. Deploy:
   docker-compose up -d
   
5. Verify:
   curl http://localhost/api/products/

═══════════════════════════════════════════════════════════════════════

📋 FILE STRUCTURE

Daily Poshan/
├── backend-django/         ← Django REST API
│   ├── apps/              ← API endpoints
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.local
│   └── manage.py
├── frontend-react/        ← React SPA
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js   ← API Client
│   │   └── App.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   ├── .env.local
│   └── index.html
├── docker-compose.yml     ← Container config
├── run.py                 ← ⭐ START HERE
├── test_api.py            ← Test integration
├── setup.py               ← Install dependencies
└── DEPLOYMENT.md          ← Full deployment guide

═══════════════════════════════════════════════════════════════════════

⚡ COMMONLY USED COMMANDS

Setup (first time):
    python setup.py

Start all servers:
    python run.py

Test everything:
    python test_api.py

Backend only:
    cd backend-django && python manage.py runserver

Frontend only:
    cd frontend-react && npm run dev

Docker deployment:
    docker-compose up --build

View Docker logs:
    docker-compose logs -f backend
    docker-compose logs -f frontend

Stop Docker:
    docker-compose down

═══════════════════════════════════════════════════════════════════════

✅ INTEGRATION CHECKLIST

[✓] API Proxy configured (Vite → Django)
[✓] CORS enabled for frontend
[✓] Environment files created (.env.local)
[✓] Enhanced API client with error handling
[✓] Backend settings updated
[✓] Docker containers ready
[✓] Test scripts created
[✓] Documentation complete

═══════════════════════════════════════════════════════════════════════

🔍 QUICK TESTS

Browser Console (while running):
    
    // Get products
    fetch('/api/products/').then(r => r.json()).then(console.log)
    
    // Register user
    fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'test@test.com',
        password: 'pass123',
        name: 'User'
      })
    }).then(r => r.json()).then(console.log)
    
    // Login
    fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'test@test.com',
        password: 'pass123'
      })
    }).then(r => r.json()).then(console.log)

═══════════════════════════════════════════════════════════════════════

📞 TROUBLESHOOTING

Port in use?
    python manage.py runserver 8001

Can't connect to API?
    - Check backend is running: http://localhost:8000
    - Check Vite proxy in vite.config.js
    - Check CORS in .env.local

CORS error?
    - Verify localhost:5173 in CORS_ALLOWED_ORIGINS
    - Restart backend

Database error?
    cd backend-django && python manage.py migrate

═══════════════════════════════════════════════════════════════════════

📚 DOCUMENTATION

See:
    INTEGRATION_SUMMARY.md  ← Overview & quick guide
    DEPLOYMENT.md           ← Full deployment guide
    
═══════════════════════════════════════════════════════════════════════

🎉 YOU'RE READY!

Start with:
    python run.py

Then open:
    http://localhost:5173

Test with:
    python test_api.py

Deploy with:
    docker-compose up --build

═══════════════════════════════════════════════════════════════════════

Questions? Check DEPLOYMENT.md for detailed guide.

Happy Coding! 🚀

"""
    print(guide)

if __name__ == "__main__":
    print_guide()
