# Используем базовый образ Ubuntu
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Обновляем пакеты и устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    git \
    gnupg \
    software-properties-common \
    curl \
    wget \
    unzip \
    python3 \
    python3-pip \
    bash-completion \
    sudo \
    openssh-client \
    sshpass \
    ansible

# Генерируем SSH-ключи для текущего пользователя (используя переменную $HOME)
RUN mkdir -p $HOME/.ssh && ssh-keygen -t ed25519 -f $HOME/.ssh/id_ed25519 -N ""

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

# Копируем бинарные файлы Yandex Cloud CLI в /usr/bin/
RUN cp -r ~/yandex-cloud/bin/* /usr/bin/

# Устанавливаем имя хоста
RUN echo "vm-1" > /etc/hostname

# Активируем bash-completion для текущей сессии bash
RUN echo "source /usr/share/bash-completion/bash_completion" >> ~/.bashrc

# Устанавливаем bash в качестве основной оболочки
CMD ["/bin/bash"]
