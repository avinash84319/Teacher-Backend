FROM python:3.11-buster

RUN pip install poetry==1.8.3

COPY . .

RUN poetry install

RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

RUN mkdir -p /usr/local/gcloud && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
    && /usr/local/gcloud/google-cloud-sdk/install.sh

ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

RUN gcloud auth activate-service-account --key-file=gcpkey.json --project=teacherstudent-431416

EXPOSE 5000

ENTRYPOINT ["poetry", "run", "flask", "--app", "server" , "run", "--host=0.0.0.0"]


