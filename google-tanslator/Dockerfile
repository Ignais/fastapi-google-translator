FROM python:3.10
# 
WORKDIR /google-tanslator

# 
COPY requirements.txt requirements.txt

#
RUN pip install --upgrade pip -r requirements.txt

EXPOSE 8000

COPY ./ /google-tanslator/

COPY . .

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--port", "8000", "--reload"]


