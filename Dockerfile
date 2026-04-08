FROM python:3.10.14-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 7860
# પાયથોન પાથ સેટ કરો
ENV PYTHONPATH=/app
# સીધું એજન્ટ રન કરો
CMD ["python", "inference.py"]
