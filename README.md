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
<!-- START_2. project_objectives.md -->
<!-- # Задачи проекта -->

<!-- ### Задачи проекта -->

Задачи проекта:
Проектирование инфраструктуры:
Разработка схемы развертывания корпоративного сервиса документации на основе MediaWiki. Схема должна включать все ключевые компоненты (серверы, базы данных, балансировщики и вспомогательные сервисы) и описывать их взаимодействие.

Запуск инфраструктуры:
Установка и настройка MediaWiki, PostgreSQL и вспомогательных сервисов (Nginx, Zabbix). Конфигурирование балансировки нагрузки и настройка нескольких экземпляров MediaWiki.

Настройка резервного копирования и восстановления:
Создание и тестирование скриптов для резервного копирования файлов и баз данных. Определение расписания для регулярного создания резервных копий.

Организация мониторинга:
Установка и настройка Zabbix для мониторинга доступности сервисов и состояния инфраструктуры. Настройка оповещений для быстрого реагирования на проблемы.

Проверка отказоустойчивости:
Проведение тестирования отказоустойчивости системы: проверка работы после отключения серверов, восстановления из резервных копий и репликации данных.
<!-- END_2. project_objectives.md -->

## 3. Схема приложения 

<!-- # Cхема приложения -->
<details>
<summary>Развернуть</summary>
<!-- START_2.3. app_deploy_schema_v4.md -->
<!-- # Cхема приложения -->

<!-- ### Cхема приложения -->
### Cхема приложения

### Компоненты:
1. **VM-0** — Сервисная ВМ (Администрирование и деплой)
   - Стек: Alpine Linux, Docker, GitHub, Terraform, Ansible, Python.
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

VM-7 + VHDD-2 + VHDD-3: Standby БД
Standby БД получает реплицированные данные с Primary БД в асинхронном режиме, что обеспечивает отказоустойчивость и возможность восстановления данных в случае сбоя. Standby БД также может обрабатывать запросы на чтение. Резервное копирование данных осуществляется на VHDD-3 с помощью pg_dump  

[Ссылка на .drawio-файл](/project_documentation/mediafiles/2.3.%20app_deploy_schema_files_v4/2.3.%20app_deploy_schema_v4.drawio)  

![Схема развертываемого приложения](/project_documentation/mediafiles/2.3.%20app_deploy_schema_files_v4/2.3.%20app_deploy_schema_v4.svg)   



<!-- END_2.3. app_deploy_schema_v4.md -->
</details> 

## 4. Прототипирование в среде Docker


## 5. Разработка с использованием облачной инфораструктуры Yandex Cloud


## 6. Развёртывание приложения

1. [Настройка Docker для развёртывания сервисной ВМ](/Solution/3.1.%20service_vm_docker_setup.md "Docker setup for deploying a service VM")
    
    <!-- START SERVICE VM DOCKER SETUP -->
	<!-- # Настройка [Docker](https://www.docker.com/ "Официальный сайт Docker") для развёртывания сервисной ВМ -->
	
	<details>
	<summary>Развернуть</summary>   
	
	1. Скачать и установить [Docker-desktop](https://www.docker.com/products/docker-desktop/ "Скачать Docker-desktop")
	2. Установить расширение [vscode Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
	3. Cкачать Dockerfile из репозитория GitHub
	4. Создание образа ОС Alpine Linux с необходимыми пакетами и зависимостями из инструкций [Dockerfile](/Dockerfile "Ссылка на Dockerfile")
	    1. **docker build -t mediawiki_service_alpine .**
	        - docker build - создает Docker-образ
	        - -t mediawiki_service_alpine - произвольное имя образа
	        - . - контекст сборки (где искать Dockerfile). В данном случае — в текущей директории
	5. Запуск контейнера на основе созданного образа "mediawiki_service_ubuntu_22.04"
	    1. **docker run -it mediawiki_service_alpine bash**
	
	6. Добавить запущенный Docker-контейнер в vscode workspace для удобста работы
	
	    ![Открытие Docker-контейнера в vscode](/Solution/Mediafiles/3.1.%20Service_VM_Docker_setup.gif)
	
	</details>  
<!-- END SERVICE VM DOCKER SETUP -->






2. Клонирование git-репозитория на созданную ВМ (в каталог ~)


3. [Подготовительная работа](/Solution/3.3.%20preparatory_tasks.md)

	<!-- START PREPARATORY TASKS -->
	<!-- Запуск Python-скрипта [**add_env_var.py**](python-scripts/add_env_var.py) для автоматической установки переменных окружения -->
	
	<details>
	<summary>Развернуть</summary>  
	
	1. Создание файла с данными для аутентификации в Yandex Cloud — **yc_meta.json**
	
	       В ~/<имя репозитория>/credentials создать yc_meta.json и наполнить его данными из web-консоли Yandex Cloud
	       
	       Для примера использовать ~/<имя репозитория>/credentials/templates/yc_meta_EXAMPLE.json
	
	2. [Создание файла конфигурации провайдера](https://yandex.cloud/ru/docs/ydb/terraform/install "Провайдер устанавливает соединение с YDB и предоставляет API-методы.") — **.terraformrc**
	
	       В ~/<имя репозитория>/credentials создать .terraformrc и наполнить его данными из документации Yandex Cloud
	
	       Для примера можно использовать ~/<имя репозитория>/credentials/templates/.terraformrc_EXAMPLE
	
	    [Ссылка на документацию](https://yandex.cloud/ru/docs/ydb/terraform/install)
	
	3. Настройка профиля Yandex Cloud CLI  (если не был настроен ранее)
	
	       # Начало настройки профиля
	       yc init
	
	       # Продолжение настройки согласно сообщениям командной строки
	
	       # Проверка настроек профиля Yandex Cloud CLI
	       yc config list
	
	</details>
<!-- END PREPARATORY TASKS --> 	

4. [Запуск конвеера](/Solution/4.3.%20start_pipeline.md). Автоматический запуск и инициализация Yandex Cloud, Terrraform

	<!-- START START PIPELINE -->
	<details>
	<summary>Развернуть</summary>  
	
	1. Запуск Python-скрипта [**add_env_var.py**](python-scripts/add_env_var.py) для автоматической установки переменных окружения
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
	    
	</details>
	
	
	
	
<!-- END START PIPELINE -->

5. [Настройка Ansible](/Solution/5.%20Ansible%20setup.md) с помощью pyton-скриптов  
Ansible — инструмент для автоматической конфигурации инфраструктуры
    
	<!-- START ANSIBLE SETUP -->
	<!-- # Настройка Ansible для автоматической конфигурации сервиса -->
	
	<details>
	<summary>Развернуть</summary>   
	
	
	1. Запуск Python-скрипта [**update_ansible_inventory.py**](python-scripts/update_ansible_inventory.py) для автоматического и динамического формирования inventory.yaml
	
	- Cкрипт содержит в себе вызовы скриптов: 
	  - [get_terraform_vm_data.py](python-scripts/get_terraform_vm_data.py) 
	  - [update_ansible_meta.py](python-scripts/update_ansible_meta.py)
	       
	        # update_ansible_inventory.py содержит словарь dynamic_groups
	        # Он предназначен для выстраивания структуры групп, подгрупп и входящих в них ВМ.
	        # Он уже настроен. Но, при необходимости, можно менять структуру файла inventory.yaml
	
	        # Просмотреть список созданных через Terraform ВМ      
	        ~/<имя репозитория>/<папка Terraform> terraform output 
	        # Или в файле ~/<имя репозитория>/<папка Terraform>/terraform.tfstate
	
	2. Запуск playbook
	   - Установка стандартных пакетов на все ВМ
	
	         ansible-playbook playbook.yaml -i inventory.yaml --tags="install_default_packages" 
	
	
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
	               
	
	        
	
	
	
	2. dsadsadsadsa
	
	</details>
<!-- END ANSIBLE SETUP -->
