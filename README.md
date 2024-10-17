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

- Cкрипт содержит в себе вызовы сторонних скриптов: 
  - [update_ansible_meta.py](python-scripts/update_ansible_meta.py) - Создание файла "ansible_meta.json" с мета-данными Ansible
  - [add_env_var.py](python-scripts/add_env_var.py) - Создание файла "terraform_vm_data.json" c данными ВМ

- Cкрипт содержит в себе вызовы функций из сторонних скриптов: 
  - [from data_handler_update_ansible_inventory](python-scripts/data_handler_update_ansible_inventory.py) import create_group_vars, get_vm_info - Обработка данных из "ansible_meta.json" и "terraform_vm_data.json"
  - **from [ansible_structure](python-scripts/ansible_structure.py) import dynamic_groups**


        # ansible_structure.py содержит словарь dynamic_groups
        # Он предназначен для выстраивания структуры групп, подгрупп и входящих в них ВМ.
        # Он уже настроен. Но, при необходимости, можно менять структуру файла inventory.yaml

        # Просмотреть список созданных через Terraform ВМ      
        ~/<имя репозитория>/<папка Terraform> terraform output 
        # Или в файле ~/<имя репозитория>/<папка Terraform>/terraform.tfstate

2. Pipeline по запуску playbook'ов playbook
   - Изменение имени хостов всех ВМ
            ansible-playbook playbook.yaml -i inventory.yaml --tags="change_hostname"

   - Монтирование внешних жестких дисков, инициализация LVM.  
      - Будут созданы: disk Partition, Physical Volume, Group Volume, Logical Volume, точка монтирования в /opt, запись в /etc/fstab для автомонтирования диска после перезапуска ВМ

            ansible-playbook playbook.yaml -i inventory.yaml --tags="mount_external_disks"

   - Размонтирование внешних жестких дисков, деинициализация LVM.  

            ansible-playbook playbook.yaml -i inventory.yaml --tags="unmount_external_disks"

   - Установка пакетов для postgresql  
            ansible-playbook playbook.yaml -i inventory.yaml --tags="setup_db_postgresql"


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
      ansible-playbook <название playbook>.yaml -i <название файла с inventory>.yaml --tags="<указать тег>"

        Пример:
        ansible-playbook mount_disks_playbook.yaml -i inventory.yaml --tags="moint_dir"


  </details> 

<!-- END_5.4. ansible_setup.md -->

</details>


### 5.5 Настройка PostgreSQL

<details>
<summary>Развернуть</summary>  

<!-- START_5.5. postgresql_setup.md -->
<!-- # Настройка PostgreSQL -->

#### Настройка PostgreSQL

1. Общие настройки для Primary и Standby PostgreSQL


   <details>
   <summary>Развернуть</summary> 
   
    - Установка postgresql

          # Обновление пакетов репозитория, установка postgresql, добавление в автозагрузку
          sudo apt update && sudo apt upgrade -y
          sudo apt install postgresql 
          sudo systemctl enable postgresql

          # Проверка установки: автозапуск и статус службы
          systemctl is-enabled postgresql
          systemctl status postgresql

   </details>  
  


2. Настройка Primary PostgreSQL


   <details>
   <summary>Развернуть</summary> 
   
    - Создание новой роли 

          # Создание новых пользователей: wikiuser (основной), syncuser (для репликации)
          sudo -u postgres createuser -P wikiuser
          sudo -u postgres createuser --replication -P syncuser
              - --replication - право на репликацию
          # Создание базы данных
          sudo su - postgres
          psql
          CREATE DATABASE my_wiki;
          # Назначение пользователю прав на базу данных
          sudo su - postgres
          psql
          GRANT ALL PRIVILEGES ON DATABASE my_wiki to wikiuser; 
          # Вывод списка пользоватей с правами
          psql
          \du
          # Вывод списка баз данных
          \l

    - Настройка сетевого подключения

          # Вывод информации о ip и NAT-ip
          # При использовании tailscale, указать NAT-ip оттуда
          ip addr show
          curl ifconfig.me

          # В конец файла /etc/postgresql/14/main/pg_hba.conf добавить параметры подключения для wikiuser (основной) и syncuser (для репликации)
          host my_wiki       wikiuser       10.10.0.0/16               scram-sha-256
          host my_wiki       wikiuser       100.64.1.35/32             scram-sha-256
          host my_wiki       wikiuser       77.137.79.100/32           scram-sha-256  
          host replication   syncuser       10.10.0.0/16               scram-sha-256  
          host replication   syncuser       100.64.1.35/32             scram-sha-256
          host replication   syncuser       77.137.79.100/32           scram-sha-256  

              - host my_wiki - база данных для поключения по сети
              - wikiuser - имя пользователя
              - 10.10.0.0/16 - из какой сети разрешено подлкючение
              - scram-sha-256 - авторизация по паролю

          # Настроить /etc/postgresql/14/main/postgresql.conf
          listen_addresses = '*'
          wal_level = replica
              - listen_addresses - какие адреса могут поключаться к БД      
              - wal_level - WAL это журнал транзакций, а wal_level определяет объём записываемых в него данных.  

          # Перезапустить сервис
          sudo systemctl restart postgresql 

          # в случае проблем с подключением проверить запросы на порт
          sudo ss -an4p |grep 5432
          # Посмотреть логи
          sudo tail -n 50 /var/log/postgresql/postgresql-*.log

          # Подключение к БД my_wiki
          sudo su - postgres
          psql --host 10.11.1.131 --username wikiuser --password --dbname my_wiki 
              - 10.11.1.131 - ip-адрес БД


    </details>  




3. Настройка Standby PostgreSQL


   <details>
   <summary>Развернуть</summary> 

    - Настройка репликации

          # Настроить /etc/postgresql/14/main/postgresql.conf
          hot_standby = on

    - Копирование БД с Primary PostgreSQL

          # Остановка сервиса
          sudo systemctl stop postgresql
          # Удаление старой БД
          sudo -u postgres rm -rf /var/lib/postgresql/14/main/
          # Запуск сервиса
          sudo systemctl start postgresql
          sudo systemctl restart postgresql   
          # Создание backup'a
          sudo -u postgres pg_basebackup -h 10.11.1.131 -D /var/lib/postgresql/14/main -U syncuser -P -v -R
              - h MAIN_IP — адрес главного сервера
              - D — папка, куда нужно положить backup
              - U — пользователь для подключения
              - P — запрашивает ввод пароля
              - v — выводит подробный лог выполнения команды
              - R — создаёт в папке с базами данных файл standby.signal. Это маркер для сервера PostgreSQL, что нужно запуститься в резервном режиме


   </details>  

3. Проверка репликации

   <details>
   <summary>Развернуть</summary>  
      
    - Настройка репликации

          # Создание тестовой БД на Primary PostgreSQL  
          sudo -u postgres createdb replica_test 

          # Проверка тестовой БД на Standby PostgreSQL  
          sudo su - postgres
          psql
          \l

   </details> 


4. Проверка параметров репликации

   <details>
   <summary>Развернуть</summary>  
      
    - Настройка репликации

          # Просмотр параметров репликации
          sudo su - postgres
          psql
          \x
          SELECT * FROM pg_stat_replication;


   </details> 


5. Настройка внешних жестких дисков

   <details>
   <summary>Развернуть</summary>  
      
    - Монтирование дисков

      <details>
      <summary>Развернуть</summary>  

          # p.s. для добавления доп. жесткого диска к ВМ cloudshell
          vm attach <название ВМ>

          # Отобразить инфо о дисках и разделах:
          lsblk -f

          # Разметка диска новыми разделами (partition): fdisk /dev/<название устройства>
          fdisk /dev/<название устройства>
          (напр.: $ sudo fdisk /dev/vdb)
              # Открывается консоль "fdisk" 
              - g — создание таблицы разделов gpt
              - n — Создание раздела диска (partition) > указать номер раздела (обычно 1) > enter (вопрос про секторы)
              - w — сохр. изменения и выйти
          
          # Инициализация Physical Volume
          lsblk -f
          pvcreate /dev/<название раздела>
          (напр.: $ sudo pvcreate /dev/vdb1)

          # Создание VG (Volume Group)
          # vgs - проверка, что VG создан
          vgcreate <название группы томов> /dev/<название раздела>
          (напр.: $ sudo vgcreate vg-db-storage /dev/vdb1)

          # Cоздание LV (Logical Volume)
          # lvs - проверка, что LV создан
          lvcreate -n <название LV> -l <кол-во extents (можно посмотреть vgdisplay <название VG>)> <название VG>
              - vgdisplay <название VG> — проверить кол-во PE (physical extents)
          (напр.: $ sudo lvcreate -n lv-db -l 5119 vg-db-storage)

          # Форматирование LV и создание файловой системы ext4
          mkfs.ext4 /dev/<название VG>/<название LV>
          (напр.: sudo mkfs.ext4 /dev/vg-db-storage/lv-db)

          # Создание точки монтирования
          mkdir /opt/<название директории>/
          (напр.: sudo mkdir /opt/db_mount/)

          # Монтирование LV
          mount /dev/<название VG>/<название LV> <точка монтирования>
          (напр.: sudo mount /dev/vg-db-storage/lv-db /opt/db_mount/)

          # Добавлление LV в автомонтирование /etc/fstab 
          # cat /etc/fstab или mount -a - проверка автомонтирования
          echo "/dev/<название VG>/<название LV> ext4 defaults 0 0" | sudo tee -a /etc/fstab
          (напр.: sudo echo "/dev/vg-db-storage/lv-db /opt/db_mount/ ext4 defaults 0 0" | sudo tee -a /etc/fstab)

      </details> 


    - Размонтирование дисков

      <details>
      <summary>Развернуть</summary>  

          # Просмотреть path точки монтирования
          lsblk -f
          
          # Размонтирование директории
          umount <path>
          (напр.: sudo umount /opt/db_mount)

          # Удаление LV (Logical Volume)
          # lvdisplay — просмотр LV 
          lvremove <path>
          (напр.: sudo lvremove /dev/vg-db-storage/lv-db)

          # Удаление VG (Volume Group)
          # vgdisplay — просмотр VG 
          vgremove <название VG>
          (напр.: sudo vgremove vg-db-storage)

          # Удаление partition (и вместе с ним PV (Physical Volume))
          # fdisk -l или lsblk -f — просмотр partition
          fdisk <path> 
              - p — просмотр сущ. разделов (partition)
              - d — удалить раздел > указать номер раздела
              - w — сохр. изменения и выйти

      </details> 

   </details> 


6. Перенос БД на внешний жесткий диск

   <details>
   <summary>Развернуть</summary>  
      
    - Перенос Primary PostgreSQL на внешний жеский диск

          # Остановка сервиса
          sudo systemctl stop postgresql

          # Копирование БД в новую директорию
          <!-- sudo cp -R /var/lib/postgresql/14/main /opt/db_mount/ -->
          sudo rsync -arv /var/lib/postgresql/14/main /opt/db_mount/
          
          # "Спрятать" старую БД
          sudo mv /var/lib/postgresql/14/main /var/lib/postgresql/14/main.bak

          # Копирование прав доступа со старой директории на новую
          sudo chown --reference=/var/lib/postgresql/14/main /opt/db_mount/
          sudo chmod --reference=/var/lib/postgresql/14/main /opt/db_mount/
          sudo chown -R postgres:postgres /opt/db_mount/main

          # Проверка прав доступа
          sudo ls -l /var/lib/postgresql/14/main
          sudo ls -l /opt/db_mount/


          # Настройка файла конфигурации /etc/postgresql/14/main/postgresql.conf
          data_directory = '/opt/db_mount/14/main'

          <!-- # Настройка прав доступа к директории
          sudo chown -R postgres:postgres /opt/db_mount/
          sudo chmod -R 700 /opt/db_mount/ -->

          # Запуск сервиса
          sudo systemctl start postgresql
          # Перезапуск сервиса
          sudo systemctl restart postgresql
          # Проверка настроек
          sudo pg_lsclusters
          # Проверка установки: автозапуск и статус службы
          systemctl is-enabled postgresql
          systemctl status postgresql



   </details> 



7. Основные команды для работы с PostgreSQL  

   <details>
   <summary>Развернуть</summary>  
      
      # Вход в аккаунт postgres
      sudo -i -u postgres
      # Открытие консоли postgres
      psql
      # Выход из консоли
      \q
      # Выход из оболочки пользователя
      Ctrl+D
      # Просмотр статуса подключения
      \conninfo
      # Список БД
      \l
      # Подключение к БД
      \c <имя БД>
      # Просмотр списка ролей (пользователей)
      \du
      # Создать новую роль
      createuser --interactive
      # Создать новую БД
      createdb <имя БД>

      # Работа в консоли БД postgres подразумевает, что в linux существует такой же акк
      # После создания новой БД выходим из акк postgres > создаем в linux нового пользователя с именем БД > переключаемся на него > подключаемся к консоли
      sudo adduser <имя пользователя linux>
      sudo -i -u <имя созданного пользователя linux>
      psql

   </details> 

<!-- END_5.5. postgresql_setup.md -->

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

   - Содержит вызовы:
      - [update_ansible_meta.py](python-scripts/update_ansible_meta.py) - Создание файла "ansible_meta.json" с мета-данными Ansible
      - [add_env_var.py](python-scripts/add_env_var.py) - Создание файла "terraform_vm_data.json" c данными ВМ

    - Cкрипт содержит в себе вызовы сторонних скриптов: 
        - [update_ansible_meta.py](python-scripts/update_ansible_meta.py) - Создание файла "ansible_meta.json" с мета-данными Ansible
        - [add_env_var.py](python-scripts/add_env_var.py) - Создание файла "terraform_vm_data.json" c данными ВМ

    - Cкрипт содержит в себе вызовы функций из сторонних скриптов: 
        - [from data_handler_update_ansible_inventory](python-scripts/data_handler_update_ansible_inventory.py) import create_group_vars, get_vm_info - Обработка данных из "ansible_meta.json" и "terraform_vm_data.json"
    - **from [ansible_structure](python-scripts/ansible_structure.py) import dynamic_groups**

          # ansible_structure.py содержит словарь dynamic_groups
          # Он предназначен для выстраивания структуры групп, подгрупп и входящих в них ВМ.
          # Он уже настроен. Но, при необходимости, можно менять структуру файла inventory.yaml

          # Просмотреть список созданных через Terraform ВМ      
          ~/<имя репозитория>/<папка Terraform> terraform output 
          # Или в файле ~/<имя репозитория>/<папка Terraform>/terraform.tfstate

#### Вспомогательные

1. utils.py - Хранилище общих и частоиспользуемых функций
2. update_readme.py - Загрузка данных из /project_documentation и обновление README.md

<!-- END_10. python_scripts_short_description.md -->
</details>