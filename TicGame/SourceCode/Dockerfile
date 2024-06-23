FROM python:3.9

WORKDIR /TicTac
COPY . /TicTac

RUN pip install Flask
RUN pip install pymongo

EXPOSE 27017

CMD ["python", "Source.py"]