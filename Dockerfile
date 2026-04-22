FROM python:3.11-slim

# Dependências de sistema para pygame (mesmo sem display)
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libsdl2-2.0-0 \
    pkg-config \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p populations

# Variáveis padrão para modo headless (sem janela)
ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=dummy
ENV SDL_RENDER_DRIVER=software
ENV PYTHONUNBUFFERED=1

CMD ["bash"]
