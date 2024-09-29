# Запуск корпоративного сервиса ведения документации с помощью MediaWiki
Яндекс Практикум | Курс "Системный Администратор" | Спринт-13  

## 1. Технические требования к проекту
1. ОС сервисов проекта: Ubuntu 22.04
2. Необходимые библиотеки и фреймворки:
    1. MediaWiki (php)
    2. PostgreSQL — для хранения данных MediaWiki
    3. pg_dump — для регулярного резервного копирования базы данных
3. Планируемая нагрузка (количество клиентов): 40
4. Интерфейс взаимодействия с пользователем (HTTP-сервис): веб-интерфейс MediaWiki
5. Вспомогательные сервисы:
    1. Nginx — для балансировки нагрузки и обработки HTTP-запросов;
    2. Zabbix — для мониторинга состояния сервиса и инфраструктуры
    3. Ansible — для автоматизации настройки серверов и управления конфигурацией инфраструктуры
    4. Terraform — для автоматизированного создания и управления ВМ (серверами)
    5. Python — для автоматизации рутинных процессов
## 2. Задачи
[1. Создание схемы развертываемого приложения](Solution/2.1.%20App%20deployment%20schema.md "App deployment schema")  
2. Создание руководства по восстановлению инфраструктуры в случае аварии  
3. Настройка репозитория Git (для обеспечения IaC)  
[4. Настройка Docker для развёртывания сервисной ВМ](Solution/4.%20Docker%20setup%20for%20deploying%20a%20service%20VM.md "Docker setup for deploying a service VM")  
[5. Настройка Terraform для развёртывания ВМ](Solution/5.%20Terraform%20configuration%20for%20VM%20deployment.md "Terraform configuration for VM deployment")  
6. Настройка Ansible для конфигурации ВМ (MediaWiki, PostgreSQL, pg_dump, Nginx Zabbix и пр.)  
7. Проверка отказоустойчивости системы  

## 3. Деплой
[1. Настройка Docker для развёртывания сервисной ВМ](Solution/3.1.%20Docker%20setup%20for%20deploying%20a%20service%20VM.md "Docker setup for deploying a service VM")  
2. Клонирование репозитория в корневой каталог пользователя  
3. Настройка облачного провайдера Yandex Cloud для работы с Terraform
    1. [Установка и настройка Yandex Cloud CLI](Solution/3.3.1.%20YС%20CLI%20installation&configuration.md)  
    2. [Настройка сервисного аккаунта Yandex Cloud](Solution/3.3.2.%20YC%20service%20account%20configuration.md)  




