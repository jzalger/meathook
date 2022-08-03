FROM python:3.9-alpine
RUN pip install pipenv
RUN mkdir -p /run/meathook/
COPY meathook_web /run/meathook_web/
ADD Pipfile.lock /run/
ADD Pipfile /run/
COPY deploy /run/
WORKDIR /run
RUN pipenv install --system --deploy --ignore-pipfile
EXPOSE 5100
ENTRYPOINT ["sh", "entrypoint.sh"]
