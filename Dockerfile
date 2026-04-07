FROM python:3.10.14-bullseye

WORKDIR /app

# 1. જરૂરી સિસ્ટમ લાઈબ્રેરીઓ (જો જરૂર હોય તો)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 2. Requirements ઇન્સ્ટોલ કરો
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. આખો કોડ કોપી કરો
COPY . .

# 4. પોર્ટ એક્સપોઝ કરો (Meta અને Hugging Face માટે જરૂરી)
EXPOSE 7860

# 5. સીધું inference.py રન કરો
# આનાથી 'if __name__ == "__main__": main()' વાળો બ્લોક આપોઆપ રન થશે
CMD ["python", "inference.py"]
