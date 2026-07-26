# 📈 Stock Market Prediction

An AI-powered Stock Market Prediction Platform built using **Spring Boot**, **FastAPI**, **Machine Learning**, and **PostgreSQL**.

## 🚀 Project Overview

This project predicts short-term stock price movements by combining technical indicators with machine learning models. It follows a microservice architecture where the Java backend handles business logic and APIs, while a Python ML service performs data processing, model training, and predictions.

---

## 🏗️ Architecture

```
                    React Frontend (Coming Soon)
                              │
                              ▼
                    Spring Boot Backend
                         (backend)
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
       PostgreSQL Database            FastAPI ML Service
                                          (ml-service)
                                                │
                                                ▼
                                  Machine Learning Models
                                                │
                                                ▼
                                   Yahoo Finance Historical Data
```

---

## 📂 Project Structure

```
stock-market-prediction
│
├── backend/          # Spring Boot Backend
├── ml-service/       # FastAPI ML Service
├── .gitignore
└── README.md
```

---

## ✨ Features

### Backend (Spring Boot)
- REST APIs
- Prediction APIs
- Historical Data APIs
- PostgreSQL Integration
- Flyway Database Migration
- Service Layer Architecture

### ML Service (FastAPI)
- Historical Data Collection
- Feature Engineering
- Technical Indicators
- Model Training
- Stock Price Prediction
- Prediction History
- Model Evaluation

---

## 📊 Technical Indicators

- SMA (20, 50, 200)
- EMA (12, 26)
- RSI (14)
- MACD
- MACD Signal
- MACD Histogram
- Bollinger Bands
- ATR
- +DI
- -DI
- DX
- ADX

---

## 🤖 Machine Learning

Current Model:

- Random Forest Regressor

Future Models:

- XGBoost
- LightGBM
- CatBoost

---

## 🛠 Tech Stack

### Backend

- Java 21
- Spring Boot
- Maven
- PostgreSQL
- Flyway

### Machine Learning

- Python
- FastAPI
- Pandas
- NumPy
- Scikit-Learn
- SQLAlchemy
- APScheduler
- yfinance

### Frontend (Upcoming)

- React
- TypeScript

---

## 🔮 Future Enhancements

- React Dashboard
- Live Stock Prices
- Authentication
- Portfolio Management
- Docker Deployment
- Kubernetes Deployment
- CI/CD Pipeline
- Cloud Deployment

---

## 👨‍💻 Author

**Naresh N**

GitHub: https://github.com/nareshn-01
