# Daily Poshan - Complete Integration & Deployment Guide

## ✅ Integration Summary

Your backend and frontend are now fully integrated with:

1. ✅ **API Proxy** - Vite proxies `/api` requests to Django backend
2. ✅ **CORS Configured** - Frontend can make cross-origin requests
3. ✅ **Environment Setup** - `.env.local` files created for both
4. ✅ **Enhanced API Client** - Error handling and logging added
5. ✅ **Test Scripts** - Ready to verify integration
6. ✅ **Docker Ready** - Production deployment prepared

---

## 🚀 Run Locally (3 Options)

### Option 1: Automated (Recommended) - ONE COMMAND
```bash
python run.py
```
This will start both backend and frontend. Access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api

### Option 2: Manual (2 Terminals)

**Terminal 1 - Backend:**
```bash
cd backend-django
pip install -r requirements.txt  # First time only
python manage.py migrate         # First time only
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend-react
npm install                      # First time only
npm run dev
```

### Option 3: Docker (Production-like)
```bash
docker-compose up --build
```

---

## 🧪 Test Integration

```bash
# Run comprehensive API tests
python test_api.py
```

Expected output:
```
✅ GET /products/ (3 products found)
✅ POST /auth/register
✅ POST /auth/login
✅ CORS Headers
```

---

## 🔌 API Endpoints Ready

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/login` | Login user |
| POST | `/api/auth/register` | Register new user |
| GET | `/api/products/` | Get all products |
| GET | `/api/products/{id}/` | Get product by ID |
| POST | `/api/orders/` | Create order |
| GET | `/api/orders/{id}/` | Get order details |
| POST | `/api/payments/create` | Create payment |
| POST | `/api/payments/verify` | Verify payment |
| GET | `/api/admin/orders` | Get all orders |
| PUT | `/api/admin/orders/{id}/status` | Update order status |

---

## 🐳 Deploy to Production

### Step 1: Prepare Environment Files

**Create backend-django/.env.production:**
```
DEBUG=False
SECRET_KEY=<change-to-secure-random-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Create frontend-react/.env.production:**
```
VITE_API_BASE_URL=https://yourdomain.com/api
```

### Step 2: Build Docker Images

```bash
docker build -t dailyposhan-backend:latest ./backend-django
docker build -t dailyposhan-frontend:latest ./frontend-react
```

### Step 3: Deploy to Server

```bash
# Option A: Using Docker Compose
docker-compose up -d

# Option B: Using individual containers
docker run -d -p 8000:8000 --name backend dailyposhan-backend:latest
docker run -d -p 80:80 --name frontend --link backend:backend dailyposhan-frontend:latest
```

### Step 4: Verify Deployment

```bash
curl https://yourdomain.com/api/products/
```

---

## 📋 What's Configured

### Frontend (React + Vite)
- ✅ `.env.local` with API base URL
- ✅ `vite.config.js` with `/api` proxy to backend
- ✅ Enhanced `api/client.js` with error handling
- ✅ Dockerfile for production deployment
- ✅ Nginx reverse proxy configured

### Backend (Django)
- ✅ `.env.local` with configuration
- ✅ CORS enabled for frontend communication
- ✅ `settings.py` updated to use environment variables
- ✅ python-dotenv added to requirements.txt
- ✅ Dockerfile for production deployment

### Helper Scripts
- ✅ `run.py` - Start both servers
- ✅ `test_api.py` - Test integration
- ✅ `setup.py` - Install dependencies

---

## 🔄 How It Works

### Local Development
```
Browser (http://localhost:5173)
    ↓
Vite Dev Server (Proxy /api → http://localhost:8000)
    ↓
Django Backend
```

### Production (Docker)
```
Browser (https://yourdomain.com)
    ↓
Nginx (Port 80/443)
├─ / → Frontend (React static files)
└─ /api/ → Backend (Django)
```

---

## 🧪 Quick Test in Browser Console

```javascript
// Test products endpoint
fetch('/api/products/')
  .then(r => r.json())
  .then(d => console.log('Products:', d))

// Test register
fetch('/api/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'test@example.com',
    password: 'password123',
    name: 'Test User'
  })
})
.then(r => r.json())
.then(d => console.log('Registered:', d))

// Test login
fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'test@example.com',
    password: 'password123'
  })
})
.then(r => r.json())
.then(d => console.log('Logged in:', d))
```

---

## ⚡ Common Commands

```bash
# First time setup
python setup.py

# Start all servers
python run.py

# Test everything
python test_api.py

# Backend only
cd backend-django && python manage.py runserver

# Frontend only
cd frontend-react && npm run dev

# Docker deployment
docker-compose up --build

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop everything
docker-compose down
```

---

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Port 8000 in use** | `python manage.py runserver 8001` |
| **Port 5173 in use** | `VITE_PORT=5174 npm run dev` |
| **CORS error** | Check `CORS_ALLOWED_ORIGINS` in `.env.local` |
| **Can't reach API** | Ensure backend is running on port 8000 |
| **Database error** | Run `python manage.py migrate` |
| **npm install fails** | Delete `node_modules` and try again |
| **Docker port conflict** | Check `docker ps` and kill conflicting container |

---

## 📊 Project Files Modified

✅ `frontend-react/vite.config.js` - Added /api proxy
✅ `frontend-react/src/api/client.js` - Enhanced with error handling
✅ `frontend-react/.env.local` - Created with API base URL
✅ `backend-django/dailyposhan_backend/settings.py` - Added env support and CORS config
✅ `backend-django/requirements.txt` - Added python-dotenv
✅ `backend-django/.env.local` - Created with configuration

### New Files Created
✅ `run.py` - Automated server launcher
✅ `test_api.py` - Integration test suite
✅ `setup.py` - Dependency installer
✅ `DEPLOYMENT.md` - Comprehensive deployment guide
✅ `INTEGRATION_SUMMARY.md` - This file

---

## 📚 Full Documentation

See **[DEPLOYMENT.md](./DEPLOYMENT.md)** for:
- Detailed deployment instructions
- Docker setup
- Production configuration
- Security checklist
- Troubleshooting guide

---

## ✨ You're All Set!

Your Daily Poshan application is fully integrated and ready to:

1. **Run locally** - `python run.py`
2. **Test** - `python test_api.py`
3. **Deploy** - `docker-compose up --build`

```bash
# Get started now!
python run.py
```

Then open http://localhost:5173 in your browser.

---

**Happy coding! 🚀**
