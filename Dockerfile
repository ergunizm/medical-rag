#React Frontend
FROM node:18-alpine AS build-react

WORKDIR /app/react-front

COPY react-front/package*.json ./
RUN npm install

COPY react-front/ ./
RUN npm run build

#FastAPI Backend
FROM pytorch/pytorch

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./data /code/data

COPY --from=build-react /app/react-front/build /code/react-front/build

#Uygulamayı başlat
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]