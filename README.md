# Запуск корпоративного сервиса ведения документации с помощью MediaWiki
Яндекс Практикум | Курс "Системный Администратор" | Спринт-13  

## 1. Технические требования к проекту
1. ОС сервисов проекта: ОС: Ubuntu 22.04
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
[1. Создание схемы развертываемого приложения](Solution/1.%20App%20deployment%20schema.md)  
2. Создание руководства по восстановлению инфраструктуры в случае аварии  
3. Настройка репозитория Git (для обеспечения IaC)  
4. Настройка Terraform для развёртывания ВМ  
5. Настройка Ansible для конфигурации ВМ (MediaWiki, PostgreSQL, pg_dump, Nginx Zabbix и пр.)  
6. Проверка отказоустойчивости системы 

## 3. Решение
1. Создание схемы развертываемого приложения  
    1. Вариант N1
    


