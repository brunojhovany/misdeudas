FROM python:3

WORKDIR /usr/src/app

ENV FLASK_APP=app.py
ENV FLASK_ENV="development"
ENV FLASK_DEBUG="0",

ENV APP_SETTINGS="config.DevelopmentConfig"
ENV DATABASE_URL="postgresql://USERNAME:PASSWORD@0.0.0.0/misdeudas"
ENV JWTSECRET="FSA2324FAewrr-wer-wer.werf_wef2432qf"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]