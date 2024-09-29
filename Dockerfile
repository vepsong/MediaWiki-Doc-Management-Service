# Используем базовый образ Ubuntu
FROM ubuntu:22.04

# Обновляем пакеты и устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    git \ 
    gnupg \
    software-properties-common \
    curl \
    wget \
    git \
    unzip \
    python3 \
    python3-pip \
    bash-completion

# Добавляем HashiCorp GPG ключ
RUN wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null

# Проверка ключа (необязательная)
RUN gpg --no-default-keyring \
    --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
    --fingerprint

# Добавляем официальный репозиторий HashiCorp для установки Terraform
RUN echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/hashicorp.list

# Обновляем пакеты и устанавливаем Terraform
RUN apt-get update && apt-get install -y terraform

# Устанавливаем Yandex Cloud CLI
RUN curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash

# Активируем bash-completion для текущей сессии bash
RUN echo "source /usr/share/bash-completion/bash_completion" >> ~/.bashrc

# Открываем bash по умолчанию
CMD ["/bin/bash"]
