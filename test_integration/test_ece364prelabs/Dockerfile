# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV INPUT_ORG=PurdueECE364
ENV INPUT_PATTERN=^prelabs-.*$
ENV INPUT_CREATED_AFTER='01/01/2022 00:00:00'
ENV INPUT_CREATED_BEFORE='01/06/2022 00:00:00'

# Install pip requirements
COPY requirements.txt /
RUN python -m pip install -r /requirements.txt

COPY . /


# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "/main.py"]
