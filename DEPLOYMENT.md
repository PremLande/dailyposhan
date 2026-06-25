# Daily Poshan - Full Stack Setup & Deployment Guide

## 📋 Quick Start (Local Development)

### Prerequisites
- Python 3.12+
- Node.js 20+
- pip and npm

### 1. Install Dependencies

**Backend:**
```bash
cd backend-django
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend-react
npm install
```

### 2. Run Local Servers

**Option A - Automated (Recommended):**
```bash
python run.py
```

**Option B - Manual (2 terminals):**

Terminal 1 - Backend:
```bash
cd backend-django
python manage.py runserver
```

Terminal 2 - Frontend:
```bash
cd frontend-react
npm run dev
```

### 3. Access the Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000/api
- **Admin Panel:** http://localhost:8000/admin

### 4. Test Integration

```bash
python test_api.py
```

Expected output:
```
✅ GET /products/ (3 products found)
✅ POST /auth/register
✅ POST /auth/login
✅ CORS Headers
```

## 🔄 How It Works

### Local Development Architecture

```
Browser (http://localhost:5173)
    ↓
Vite Dev Server
    ↓ [Proxy /api → http://localhost:8000/api]
Django Backend (http://localhost:8000)
```

**Key Points:**
- Vite proxy routes `/api/*` requests to Django backend
- CORS allows frontend to make API requests
- Hot module reloading on both frontend and backend

### Configuration Files

**Frontend (.env.local):**
```
VITE_API_BASE_URL=http://localhost:8000/api
```

**Backend (.env.local):**
```
DEBUG=True
SECRET_KEY=dailyposhan-dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,backend
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

## 🐳 Docker Deployment

### Prerequisites
- Docker
- Docker Compose

### Build and Run

```bash
docker-compose up --build
```

This will:
1. Build backend image (Django + Gunicorn)
2. Build frontend image (Node build → Nginx serve)
3. Set up nginx reverse proxy on port 80
4. Create network between containers

### Access Deployed App

- **Frontend:** http://localhost:5173 (or http://localhost if mapped)
- **API:** http://localhost/api
- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3000
- **Jaeger UI:** http://localhost:16686

### Docker Network

```
Frontend Container (Nginx)
    ↓
Backend Container (Django)
    ↓
SQLite Database
```

### Stop Containers

```bash
docker-compose down
```

### View Logs

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🚀 Production Deployment

### Environment Setup

Create `.env.production` files:

**Backend (.env.production):**
```
DEBUG=False
SECRET_KEY=<generate-secure-random-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Frontend (.env.production):**
```
VITE_API_BASE_URL=https://yourdomain.com/api
```

### Build Docker Images

```bash
docker build -t dailyposhan-backend:latest ./backend-django
docker build -t dailyposhan-frontend:latest ./frontend-react
```

### Deploy to Server

**Option 1: Docker Compose (Recommended)**

```bash
# Copy docker-compose.yml and environment files to server
scp docker-compose.yml user@server:/app/
scp backend-django/.env.production user@server:/app/backend-django/
scp frontend-react/.env.production user@server:/app/frontend-react/

# SSH into server and run
ssh user@server
cd /app
docker-compose up -d
```

**Option 2: Docker Swarm/Kubernetes**
- Adapt docker-compose.yml to Kubernetes manifests
- Use container orchestration tools for scaling

### Database Persistence

Current setup uses SQLite. For production with persistent data:

```bash
# Mount volume for database
volumes:
  - db_data:/app/backend-django
```

### Reverse Proxy (Optional - Nginx on Host)

```nginx
upstream backend {
  server 127.0.0.1:8000;
}

server {
  listen 443 ssl;
  server_name yourdomain.com;
  
  ssl_certificate /path/to/cert.pem;
  ssl_certificate_key /path/to/key.pem;

  location /api/ {
    proxy_pass http://backend/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }

  location / {
    proxy_pass http://127.0.0.1:80;
    proxy_set_header Host $host;
  }
}
```

## 🔍 Troubleshooting

### Backend Won't Start
```bash
# Check if port 8000 is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
python manage.py runserver 8001
```

### Frontend Can't Reach Backend
```bash
# Verify backend is running
curl http://localhost:8000/api/products/

# Check Vite proxy in vite.config.js
# Check CORS is configured in Django settings.py
```

### CORS Errors
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
1. Check `CORS_ALLOWED_ORIGINS` in `.env.local`
2. Ensure frontend URL is in the list
3. Verify backend is running

### Port Already in Use
```bash
# Change port in vite.config.js (frontend)
# Or use environment variable
VITE_PORT=5174 npm run dev

# For backend
python manage.py runserver 8001
```

## 📊 Project Structure

```
dailyposhan/
├── backend-django/
│   ├── apps/
│   │   ├── authentication/    # Login/Register
│   │   ├── products/          # Products API
│   │   ├── orders/            # Orders API
│   │   ├── payments/          # Payments API
│   │   └── adminpanel/        # Admin API
│   ├── dailyposhan_backend/   # Django config
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.local
│   └── manage.py
│
├── frontend-react/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js      # API client
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── .env.local
│   └── index.html
│
├── database/
│   └── schema.sql
│
├── docker-compose.yml
├── run.py                      # Start both servers
├── test_api.py                 # Test integration
└── DEPLOYMENT.md
```

## 🧪 Testing

### Unit Tests (Frontend)
```bash
cd frontend-react
npm test
```

### Integration Tests
```bash
python test_api.py
```

### Manual Testing

**Register User:**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123","name":"Test User"}'
```

**Login User:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123"}'
```

**Get Products:**
```bash
curl http://localhost:8000/api/products/
```

## 📝 Environment Variables Summary

| Variable | Frontend | Backend | Purpose |
|----------|----------|---------|---------|
| `VITE_API_BASE_URL` | ✅ | - | API base URL for frontend |
| `DEBUG` | - | ✅ | Django debug mode |
| `SECRET_KEY` | - | ✅ | Django secret key |
| `ALLOWED_HOSTS` | - | ✅ | Allowed hostnames |
| `CORS_ALLOWED_ORIGINS` | - | ✅ | Allowed CORS origins |

## 🎯 Next Steps

1. **Local Development:** Run `python run.py` and start coding
2. **Testing:** Run `python test_api.py` to verify integration
3. **Staging:** Test with Docker Compose locally
4. **Production:** Deploy using Docker to your server

## 📚 API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | Login user |
| POST | `/api/auth/register` | Register new user |
| GET | `/api/products/` | Get all products |
| GET | `/api/products/{id}/` | Get product details |
| POST | `/api/orders/` | Create order |
| GET | `/api/orders/{id}/` | Get order details |
| POST | `/api/payments/create` | Create payment |
| POST | `/api/payments/verify` | Verify payment |
| GET | `/api/admin/orders` | Get all orders (admin) |
| PUT | `/api/admin/orders/{id}/status` | Update order status |

## 🔐 Security Notes

- [ ] Change `SECRET_KEY` in production
- [ ] Set `DEBUG=False` in production
- [ ] Update `CORS_ALLOWED_ORIGINS` to your domain
- [ ] Use HTTPS in production
- [ ] Implement proper authentication/token system
- [ ] Add rate limiting
- [ ] Validate all user inputs
- [ ] Use environment variables for sensitive data

## 📞 Quick Commands

```bash
# Start local development
python run.py

# Test API integration
python test_api.py

# Run backend only
cd backend-django && python manage.py runserver

# Run frontend only
cd frontend-react && npm run dev

# Docker deployment
docker-compose up --build

# View backend logs
docker-compose logs -f backend

# Stop all containers
docker-compose down
```

---

**Ready to deploy? Follow the Docker Deployment section above!**
