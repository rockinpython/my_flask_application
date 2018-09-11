FROM python:3.6.4-alpine3.7

COPY * /wheelhouse/

EXPOSE 5000

WORKDIR /wheelhouse


RUN pip install --upgrade \
    -f /wheelhouse \
    -r /wheelhouse/requirements.txt \
    servicehost

CMD src/servicehost
