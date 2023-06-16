FROM python:3.11.3
WORKDIR /usr/src/backend

COPY ./ /usr/src/backend

RUN pip install poetry
RUN poetry install

EXPOSE 8000

WORKDIR /usr/src/backend/mia
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]