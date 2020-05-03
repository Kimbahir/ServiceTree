FROM python:latest
RUN mkdir -p /src
WORKDIR /src
COPY ./requirements.txt .
COPY ./run-flask.py .
COPY ./app ./app/
COPY ./output ./output/
COPY ./data ./data/
RUN ls app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD ["run-flask.py"]
EXPOSE 8000