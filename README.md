# Запуск корпоративного сервиса ведения документации с помощью MediaWiki
Яндекс Практикум | Курс "Системный Администратор" | Спринт-13  

## 1. Техническое описание проекта
<!-- # Техническое описание проекта -->
<details>
<summary>Развернуть</summary>
<!-- START_1. project_technical_description.md -->
<!-- # Техническое описание проекта -->

<!-- ### Техническое описание проекта -->

### Техническое описание проекта
Проект предусматривает развертывание корпоративного сервиса ведения документации с использованием приложения MediaWiki. 

Система должна функционировать на ОС Ubuntu 22.04 и поддерживать работу с PostgreSQL для хранения данных.  

Основной задачей является обеспечение доступности сервиса для начальной нагрузки в 40 пользователей через веб-интерфейс, использующий HTTP-протокол. 

Для балансировки нагрузки будет использоваться Nginx, а для мониторинга инфраструктуры — Zabbix.  

Также требуется обеспечить регулярное резервное копирование базы данных с использованием pg_dump.
<!-- END_1. project_technical_description.md -->
</details>

## 2. Задачи проекта
<!-- # Задачи проекта -->

<details>
<summary>Развернуть</summary>
<!-- START_2. project_objectives.md -->
<!-- # Задачи проекта -->

<!-- ### Задачи проекта -->

### Задачи проекта:

#### 1. Проектирование инфраструктуры:
Разработка схемы развертывания корпоративного сервиса документации на основе MediaWiki. Схема должна включать все ключевые компоненты (серверы, базы данных, балансировщики и вспомогательные сервисы) и описывать их взаимодействие.

#### 2. Запуск инфраструктуры:
Установка и настройка MediaWiki, PostgreSQL и вспомогательных сервисов (Nginx, Zabbix). Конфигурирование балансировки нагрузки и настройка нескольких экземпляров MediaWiki.

#### 3. Настройка резервного копирования и восстановления:
Создание и тестирование скриптов для резервного копирования файлов и баз данных. Определение расписания для регулярного создания резервных копий.

#### 4. Организация мониторинга:
Установка и настройка Zabbix для мониторинга доступности сервисов и состояния инфраструктуры. Настройка оповещений для быстрого реагирования на проблемы.

#### 5. Проверка отказоустойчивости:  
Проведение тестирования отказоустойчивости системы: проверка работы после отключения серверов, восстановления из резервных копий и репликации данных.
<!-- END_2. project_objectives.md -->
</details>

## 3. Схема приложения 

<!-- # Cхема приложения -->
<details>
<summary>Развернуть</summary>
<!-- START_3. app_deploy_schema_v4.md -->
<!-- # Cхема приложения -->

<!-- ### Cхема приложения -->
### Cхема приложения

### Компоненты:
1. **VM-0** — Сервисная ВМ (Администрирование и деплой)
   - Стек: Alpine Linux v3.20, Docker, GitHub, Terraform, Ansible, Python.
2. **VM-1 + VHDD-1** — Система мониторинга (Zabbix + PostgreSQL)
   - Стек: Ubuntu 22.04, Zabbix-Server, PostgreSQL.
3. **VM-2** — Прокси-сервер для запросов пользователей
   - Стек: Ubuntu 22.04, Nginx, PostgreSQL.
4. **(VM-3, VM-4)** — Серверы MediaWiki. Обработка запросов пользователей
   - Стек: Ubuntu 22.04, MediaWiki, Zabbix-agent.
5. **VM-5** — Прокси-сервер для баз данных
   - Стек: Ubuntu 22.04, HAProxy, Zabbix-agent.
6. **VM-6 + VSSD-1** — Primary БД
   - Стек: Ubuntu 22.04, PostgreSQL, Zabbix-agent.
7. **VM-7 + VHDD-2 + VHDD-3** — Standby БД (Репликация и резервное копирование)
   - Стек: Ubuntu 22.04, PostgreSQL, Zabbix-agent.

### Описание:
1. VM-0: Сервисная ВМ (Администрирование и деплой)
Администратор использует Docker-контейнеры и GitHub-репозиторий для автоматического развертывания, управления и запуска Python-скриптов на сервисной ВМ. ВМ служит точкой входа для управления всей системой.

2. VM-1 + VHDD-1: Система мониторинга (Zabbix + PostgreSQL)
Система мониторинга отвечает за контроль состояния всех компонентов инфраструктуры. Zabbix-сервер собирает и анализирует данные с серверов, а PostgreSQL хранит информацию мониторинга. Данные записываются на примонтированный жесткий диск (VHDD-1), чтобы избежать потерь данных в случае сбоя системы.

3. VM-2: Прокси-сервер для запросов пользователей
Nginx-прокси принимает входящие запросы пользователей, полученные через веб-интерфейс, и распределяет их между серверами MediaWiki (VM-3 и VM-4) в зависимости от нагрузки. Это обеспечивает балансировку нагрузки и доступность системы для пользователей.

4. Cерверы MediaWiki (VM-3, VM-4)
Эти серверы обрабатывают запросы пользователей, направленные на работу с документацией. Они также передают запросы к базам данных через прокси-сервер HAProxy (VM-5). Серверы MediaWiki поддерживаются агентами Zabbix для мониторинга состояния.

5. VM-5: Прокси-сервер для баз данных
HAProxy на VM-5 отвечает за распределение запросов от серверов MediaWiki к базам данных (Primary и Standby). Запросы на запись (write) направляются на Primary БД (VM-6), а запросы на чтение (read) могут отправляться как на Primary, так и на Standby БД (VM-7), в зависимости от нагрузки.

6. VM-6 + VSSD-1: Primary БД
Primary БД обрабатывает запросы (read/write), поступающие через HAProxy. Данные хранятся на выделенном виртуальном SSD-диске (VSSD-1) для повышения скорости работы и надежности хранения. VM-6 реплицирует данные на VM-7 для обеспечения отказоустойчивости.

7. VM-7 + VHDD-2 + VHDD-3: Standby БД
Standby БД получает реплицированные данные с Primary БД в асинхронном режиме, что обеспечивает отказоустойчивость и возможность восстановления данных в случае сбоя. Standby БД также может обрабатывать запросы на чтение. Резервное копирование данных осуществляется на VHDD-3 с помощью pg_dump  

[Ссылка на .drawio-файл](/project_documentation/mediafiles/3.%20app_deploy_schema_files_v4/3.%20app_deploy_schema_v4.drawio)  

![Схема развертываемого приложения](/project_documentation/mediafiles/3.%20app_deploy_schema_files_v4/3.%20app_deploy_schema_v4.svg)  



<!-- END_3. app_deploy_schema_v4.md -->
</details> 

## 4. Прототипирование в среде Docker

## 5. Развёртывание приложения в облачной инфраструктуры Yandex Cloud

<details>
<summary>Развернуть</summary> 

### 5.1. Настройка сервисной ВМ с помощью Docker

<details>
<summary>Развернуть</summary>   
<!-- START_5.1. service_vm_docker_setup.md -->
<!-- # Настройка сервисной ВМ с помощью Docker -->

#### Настройка сервисной ВМ с помощью Docker

1. Скачивание и установка [Docker-desktop](https://www.docker.com/products/docker-desktop/ "Скачать Docker-desktop")
2. Установка расширения [vscode Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
3. Скачивание Dockerfile из репозитория [GitHub](https://github.com/vepsong/YP-sp13_MediaWiki)
4. Создание образа ОС Alpine Linux с необходимыми пакетами и зависимостями из инструкций [Dockerfile](/Dockerfile "Ссылка на Dockerfile")
    
       docker build -t mediawiki_service_alpine .

       # - docker build - создает Docker-образ
       # - -t mediawiki_service_alpine - произвольное имя образа
       # - . - контекст сборки (где искать Dockerfile). В данном случае — в текущей директории

5. Запуск контейнера на основе созданного образа "Alpine Linux:latest"

       docker run --hostname vm-0-service --name mediawiki_service_alpine-container -it mediawiki_service_alpine bash

       # - --hostname <имя хоста> - произвольное название ВМ
       # - --name <имя контейнера> - произвольное имя контейнера
       # - it <название image> - Название image из которого будет собран контейнер
       # - bash - оболочка

6. Добавление запущенного Docker-контейнера в vscode workspace для удобства работы

    ![Открытие Docker-контейнера в vscode](/project_documentation/mediafiles/5.%20app_deploy_in_yandex_cloud/5.1.%20service_vm_docker_setup.gif)



<!-- END_5.1. service_vm_docker_setup.md -->
</details> 

### 5.2. Подготовительная работа

<details>
<summary>Развернуть</summary> 

<!-- START_5.2. preparatory_tasks.md -->
<!-- Подготовительная работа -->

#### Подготовительная работа

1. Клонирование [git-репозитория](https://github.com/vepsong/YP-sp13_MediaWiki) на созданную ВМ (в каталог ~)

2. Создание файла с данными для аутентификации в Yandex Cloud — **yc_meta.json**

       В ~/<имя репозитория>/credentials создать yc_meta.json и наполнить его данными из web-консоли Yandex Cloud
       
       Для примера использовать ~/<имя репозитория>/credentials/templates/yc_meta_EXAMPLE.json

3. [Создание файла конфигурации провайдера](https://yandex.cloud/ru/docs/ydb/terraform/install "Провайдер устанавливает соединение с YDB и предоставляет API-методы.") — **.terraformrc**

       В ~/<имя репозитория>/credentials создать .terraformrc и наполнить его данными из документации Yandex Cloud

       Для примера можно использовать ~/<имя репозитория>/credentials/templates/.terraformrc_EXAMPLE

    [Ссылка на документацию](https://yandex.cloud/ru/docs/ydb/terraform/install)

4. Настройка профиля Yandex Cloud CLI  (если не был настроен ранее)

       # Начало настройки профиля
       yc init

       # Продолжение настройки согласно сообщениям командной строки

       # Проверка настроек профиля Yandex Cloud CLI
       yc config list
<!-- END_5.2. preparatory_tasks.md -->

</details> 



### 5.3. Запуск конвеера. Автоматический запуск и инициализация Yandex Cloud, Terrraform

<details>
<summary>Развернуть</summary> 

<!-- START_5.3. start_pipeline.md -->
<!-- Запуск конвеера -->

#### Запуск конвеера

1. Запуск Python-скрипта [**add_env_var.py**](python-scripts/add_env_var.py) для автоматической установки переменных окружения  

- После выполнения скрипта **обязательно перезапустить терминал**  

2. Запуск Python-скрипта [**start_pipeline.py**](python-scripts/start_pipeline.py.py)


- Cкрипт содержит в себе вызовы скриптов: 
  - [yc_service_account_configuration.py](python-scripts/yc_service_account_configuration.py) для автоматической настройки аккаунта Yandex Cloud

  - [terraform_init.py](python-scripts/terraform_init.py) для автоматической установки провайдера для работы с YDB

  - [update_terraform_meta.py](python-scripts/update_terraform_meta.py) для автоматического формирования terraform_meta.txt  

      - Файлы с публичными и приватными SSH-ключами создаются в папке ~/.ssh автоматически при сборке образа и запуске нового контейнера

      - Если необходимо использовать те, же ключи, что и на другой, уже развернутой ВМ, то их нужно оттуда вручную скопировать на новую ВМ и запустить скрипт

      - Файлы main.tf, output.tf, providers.tf, terraform.tfstate уже сконфигурированы. Ничего менять не нужно

3. Дополнительная информация

- Основные команды для работы с Terraform  
  Выполнять из директории с файлами Terraform
  
  <details>
  <summary>Развернуть</summary>  
      
      # Проверка синтаксиса всех файлов формата tf 
      terraform validate
               
      # Планирование и проверка того, что будет сделано Terraform  
      terraform plan

      # Начало работы и деплоя Terraform. 
      terraform apply -auto-approve

      # Cинхронизация состояния ресурсов с облачным провайдером (обновится файл terraform.tfstate)
      terraform refresh

      # Удаление всех созданных ресурсов
      terraform destroy -auto-approve

      # Остановка созданных ресурсов
      # Получение списка ВМ
      yc compute instance list
      # Остановка нужной ВМ
      yc compute instance stop --id <instance-id> 

      # Пересоздание ресурса
      # terraform taint помечает ресурс как "поврежденный"
      terraform taint 'yandex_compute_instance.group<НОМЕР ГРУППЫ>["vm-<НОМЕР ВМ>"]'
  </details>




<!-- END_5.3. start_pipeline.md -->
</details>


### 5.4 Настройка Ansible

<details>
<summary>Развернуть</summary>  

<!-- START_5.4. ansible_setup.md -->
<!-- # Настройка Ansible для автоматической конфигурации сервиса -->

#### Настройка Ansible для автоматической конфигурации сервиса

1. Запуск Python-скрипта [**update_ansible_inventory.py**](python-scripts/update_ansible_inventory.py) для автоматического и динамического формирования inventory.yaml

- Cкрипт содержит в себе вызовы скриптов: 
  - [update_ansible_meta.py](python-scripts/update_ansible_meta.py)

- Cкрипт читает данные из автоматически создаваемого Terraform файла: 
  - terraform.tfstate

        # update_ansible_inventory.py содержит словарь dynamic_groups
        # Он предназначен для выстраивания структуры групп, подгрупп и входящих в них ВМ.
        # Он уже настроен. Но, при необходимости, можно менять структуру файла inventory.yaml

        # Просмотреть список созданных через Terraform ВМ      
        ~/<имя репозитория>/<папка Terraform> terraform output 
        # Или в файле ~/<имя репозитория>/<папка Terraform>/terraform.tfstate

2. Запуск playbook
   - Установка стандартных пакетов на все ВМ

         ansible-playbook playbook.yaml -i inventory.yaml --tags="install_default_packages" 

   - Установка и настройка zabbix-server, zabbix-agent, keepalived в группe хостов "proxy_and_monitoring" (vm-2, vm-3)

         ansible-playbook playbook.yaml -i inventory.yaml --tags="install_zabbix_agent_and_proxy"  


3. Дополнительная информация

- Основные команды для работы с Ansible  
  Выполнять из директории с файлами Ansible
  
  <details>
  <summary>Развернуть</summary>  
      
      # Проверка синтаксиса и доступности облачных ресурсов
      ansible all -m ping -i inventory.yaml  

      # Установка или обновление коллекции
      ansible-galaxy collection install <имя коллекции>  

      # Список установленных коллекций
      ansible-galaxy collection list  

      # Создание роли (исп. для разграничения задач, которые будут выполняться в рамках playbook)
      ansible-galaxy init <название роли>

      # Список используемых ролей
      ansible-galaxy role list  

      # Запуск playbook
      ansible-playbook playbook.yaml -i inventory.yaml --tags="<указать тэг>>"  

  </details> 

<!-- END_5.4. ansible_setup.md -->

</details>
</details>

## 6. Краткое описание python-скриптов

<details>
<summary>Развернуть</summary>


<!-- START_10. python_scripts_short_description.md -->
#### Краткое описание python-скриптов

#### Основные
1. add_env_var.py - Добавление переменных окружения **(после выполнения обязательно перезапустить терминал)**
   - Добавленные переменные окружения используются во всех последующих скриптах
   - Содержит вызовы:
      - utils.py - Хранилище общих и частоиспользуемых функций 

2. start_pipeline.py - Конвеер автоматического запуска и инициализации Yandex Cloud, Terrraform
   - Содержит вызовы:
      - utils.py - Хранилище общих и частоиспользуемых функций 
      - yc_service_account_configuration.py - Создание и настройка сервисного аккаунта Yandex Cloud
      - terraform_init.py - Инициализация Terraform
      - update_terraform_meta.py - Актуализация meta-данных Terraform для передачи на создаваемые ВМ
3. update_ansible_inventory.py - Автоматическое формирование inventory.yaml для Ansible

       # update_ansible_inventory.py содержит словарь dynamic_groups
       # Он предназначен для выстраивания и изменения структуры групп, подгрупп и входящих в них ВМ.

       # Просмотреть список созданных через Terraform ВМ      
       ~/<имя репозитория>/<папка Terraform> terraform output 
       # Или в файле ~/<имя репозитория>/<папка Terraform>/terraform.tfstate

   - Содержит вызовы:
      - update_ansible_meta.py - Создание файла "ansible_meta.json" с мета-данными Ansible

      - Cкрипт читает данные из автоматически создаваемого Terraform файла: 
         - terraform.tfstate

#### Вспомогательные

1. utils.py - Хранилище общих и частоиспользуемых функций
2. update_readme.py - Загрузка данных из /project_documentation и обновление README.md

<!-- END_10. python_scripts_short_description.md -->
</details>