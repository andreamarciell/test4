# STEP 1 – BUILD FRONTEND
FROM node:18 as frontend-builder
WORKDIR /app
COPY frontend/ ./frontend
WORKDIR /app/frontend
RUN npm install && npm run build

# STEP 2 – BACKEND + STATIC MERGE
FROM python:3.11-slim
WORKDIR /app

COPY backend/ ./backend
COPY --from=frontend-builder /app/frontend/dist ./frontend_dist

RUN pip install --upgrade pip
RUN pip install -r backend/requirements.txt
RUN python -m spacy download it_core_news_sm

EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
