FROM python:3.10.6

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /DisneyPlus

COPY ./requirements.txt /DisneyPlus/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /DisneyPlus/backend/requirements.txt

COPY . /DisneyPlus/backend/

CMD  ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
