FROM python:3.10.11-slim
RUN apt update && apt install -y git
RUN cd /tmp/ \
&& git clone https://github.com/iu2frl/TelegramGPT.git \
&& cd /tmp/TelegramGPT \
&& dir -ls \
&& pip install -r ./requirements.txt
RUN cd /tmp/ \
&& git clone https://github.com/xtekky/gpt4free.git \
&& cd gpt4free \
&& pip install -r ./requirements.txt
RUN cp -R /tmp/gpt4free/g4f /tmp/TelegramGPT/
WORKDIR /tmp/TelegramGPT
ENTRYPOINT ["python", "./main.py"]
