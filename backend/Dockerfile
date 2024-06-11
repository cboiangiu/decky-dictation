FROM ghcr.io/steamdeckhomebrew/holo-base:latest

RUN pacman -Sydd --noconfirm --dbpath /var/lib/pacman python-pip git wget unzip

RUN pip3 install vosk --target=/vosk

RUN git clone https://github.com/ideasman42/nerd-dictation.git

RUN cd nerd-dictation && wget https://alphacephei.com/kaldi/models/vosk-model-small-en-us-0.15.zip && unzip vosk-model-small-en-us-0.15.zip && rm vosk-model-small-en-us-0.15.zip

ENTRYPOINT [ "/backend/entrypoint.sh" ]