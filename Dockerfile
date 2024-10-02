# Используем базовый образ Alpine Linux
FROM alpine:latest

# Обновляем пакеты и устанавливаем зависимости
RUN apk update && apk add --no-cache \
    bash \
    bash-completion \
    curl \
    wget \
    git \
    unzip \
    python3 \
    py3-pip \
    gnupg \
    ca-certificates \
    sudo \
    openssh

# Генерируем SSH-ключи
RUN ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""

# Устанавливаем Terraform
RUN wget https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip && \
    unzip terraform_1.5.7_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform_1.5.7_linux_amd64.zip

# Устанавливаем Yandex Cloud CLI
RUN curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash

# Копируем бинарные файлы Yandex Cloud CLI в /usr/bin/
RUN cp -r ~/yandex-cloud/bin/* /usr/bin/

# Устанавливаем имя хоста
RUN echo "vm-1" > /etc/hostname


# Активируем bash-completion
RUN echo "source /usr/share/bash-completion/bash_completion" >> ~/.bashrc

# Устанавливаем bash в качестве основной оболочки
CMD ["/bin/bash"]
