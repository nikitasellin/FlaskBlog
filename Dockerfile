FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY app/requirements.txt ./
RUN pip install -r requirements.txt
