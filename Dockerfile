# Using the Alpine Linux base image
FROM alpine:latest

# Updating packages and installing dependencies
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
    openssh \
    sshpass \
    ansible  

# Generating SSH keys
RUN ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""

# Installing Terraform
RUN wget https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip && \
    unzip terraform_1.5.7_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform_1.5.7_linux_amd64.zip

# Installing Yandex Cloud CLI
RUN curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash

# Copying Yandex Cloud CLI binary files to /usr/bin/
RUN cp -r ~/yandex-cloud/bin/* /usr/bin/

# Activating bash-completion
RUN echo "source /usr/share/bash-completion/bash_completion" >> ~/.bashrc

# Setting bash as the default shell.
CMD ["/bin/bash"]
