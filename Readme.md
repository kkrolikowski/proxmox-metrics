# Proxmox Metrics

Proxmox Metrics is a tool designed to work with Proxmox notifications facility and Prometheus. This tool recieves data from proxmox and collects them in Mongo database.
Those data are gathered by prometheus in the form of metrics.

![Proxmox Metrics architecture diagram](/doc/assets/proxmox-metrics-arch.png)

## Environment variables

| Variable           | Default | Description                                           |
| ------------------ | ------- | ----------------------------------------------------- |
| MONGO_URL          | -       | MongoDB connection string                             |
| MONGO_COLLECTION   | -       | Database collection where metrics data will be stored |
| MONGO_TIMEOUT      | 5       | MongoDB connection timeout value                      |
| MONGO_HISTORY_DAYS | 7       | Control how old data will be tructated                |
| LOG_LEVEL          | INFO    | Log level                                             |

> There's no need to maintain long history in metrics data. Proxmox Metrics service picks only the latest data on prometheus request

## Application endpoints

| Method | URI      | Description                                                              |
| ------ | -------- | ------------------------------------------------------------------------ |
| POST   | /backups | Endpoint used by Proxmox notifications system to send backup status data |
| GET    | /metrics | Endpoint for Prometheus service for metrics data retrieval               |
| GET    | /        | Dummy endpoint used in Kubernetest to determine if application is ready  |

## Proxmox notifications

In order to use this service, you need to setup proxmox notifications to send data to Proxmox Metrics service.

### Configuration

At the Datacenter level (click on **Datacenter** on the left menu) go to **Notifications** and then under the **Notification targets** click **Add** and select **Webhook** option.
Following window should appear. Below example contains proper webhook configuration with expected payload.

![Proxmox notifixation target window](/doc/assets/notification-targets.png)

Make sure, that Notification Matchers has active **webhook** entry with selected ProxmoxMetrics webhook.

![Proxmox notifications matchers window](/doc/assets/notification-matchers.png)

Ensure, that **global notifications settins** option is selected in backup job settings

![Proxmox backup settins with notifications tab](/doc/assets/backup-job-notification.png)

From now on every completed backup job will execute defined webhook action along with default email message.

## Docker compose

Quick guide how to run this project with included docker compose file.

### Prerequisites

This guide assumes that you have configured proxmox metrics webhook in proxmox notification targets.

### Running a project

1. Clone this repo
2. Adjust .env file to meet your desired configuration
3. In the main repository folder issue a command: `docker compose up`
4. Run backup job and wait for completed status.
5. Wait 5-10 min. and issue: http://your-docker-host:3000/ to enter grafana interface

> **IMPORTANT:** If you change MONGO_INITDB_DATABASE variable, remember to adjust settings in `docker/cfg/mongo/init.js` accordingly.

## Grafana dashboard

> **INFO** Default grafana login and password is: admin / admin

![Grafana dashboard adding](/doc/assets/grafana-dashboard-add.png)

In the following form upload a template json from `docker/cfg/grafana/grafana-dashboard.json` file. Only thing you need to choose is prometheus datasource.