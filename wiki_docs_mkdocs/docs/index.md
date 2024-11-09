# Launching a corporate documentation management service using MediaWiki

Dmitrii Kirsanov | [GitHub](https://github.com/vepsong/MediaWiki-Doc-Management-Service)

The project involves the deployment of a corporate documentation management service using the [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki) application.

<!-- ### Initial Project <span class="tooltip" onclick="showTooltip(event)">ToR<span class="tooltip-text">Term of Reference</span></span> -->

### Initial Project Term of Reference

The MediaWiki servers have to be running on ``Ubuntu 22.04 OS`` and must utilize ``PostgreSQL 14`` for data storage, including scheduled ``db_dump`` backups for data integrity.

Load balancing between the MediaWiki servers has to be managed by an ``Nginx proxy server`` to distribute incoming traffic efficiently.

System monitoring needs to be performed using ``Zabbix``, overseeing server performance metrics such as CPU, memory, disk usage, and database health to ensure system reliability and early issue detection.

As this is a pilot implementation, only ``40 users`` within the ``local network`` will access the MediaWiki service through its ``web interface`` over the ``HTTP protocol``.

### Project Objectives

#### Infrastructure Design
Development of a deployment scheme for the corporate documentation service based on MediaWiki.  
The scheme must include all key components (servers, databases, load balancers, and auxiliary services) and describe their interactions.

#### Infrastructure Deployment
Installation and configuration of MediaWiki, PostgreSQL, and auxiliary services (Nginx, Zabbix, etc.).

#### Failover Testing
Conducting system failover testing: verifying system functionality after server shutdowns, recovery from backups, and data replication checks.