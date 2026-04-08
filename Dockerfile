FROM python:3.10.14-bullseye

WORKDIR /app

# જરૂરી પેકેજિસ
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# પોર્ટ અને પાથ સેટ કરો
EXPOSE 7860
ENV PYTHONPATH=/app

# મહત્વનું: અહીં app.py રન કરો જેથી સર્વર ચાલુ રહે
CMD ["python", "app.py"]
