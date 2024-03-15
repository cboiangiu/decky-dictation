FROM ghcr.io/steamdeckhomebrew/holo-base:latest

RUN pacman -Sydd --noconfirm --dbpath /var/lib/pacman python-pip git

RUN pip3 install vosk --target=/vosk

RUN git clone https://github.com/ideasman42/nerd-dictation.git

ENTRYPOINT [ "/backend/entrypoint.sh" ]