FROM python:3.6

RUN pip install --upgrade pip 

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["sh", "run_wsgi.sh"]