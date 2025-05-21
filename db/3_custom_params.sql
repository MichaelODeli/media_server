INSERT INTO config (parameter_name, parameter_value) VALUES ('filemanager.baseway', '/home/michael/server-side/storage/');
INSERT INTO config (parameter_name, parameter_value, test_value) VALUES ('filemanager.baseway', 'Z:/', TRUE);
INSERT INTO config (parameter_name, parameter_value) VALUES ('filemanager.depth', '3');
INSERT INTO config (parameter_name, parameter_value) VALUES ('server.local_ip', '192.168.0.33');
INSERT INTO config (parameter_name, parameter_value) VALUES ('filemanager.apache_storage_subdir', '/storage/');
INSERT INTO config (parameter_name, parameter_value) VALUES ('filemanager.update_interval', '1');
INSERT INTO config (parameter_name, parameter_value) VALUES ('apps.torrents.enabled', 'True');
INSERT INTO config (parameter_name, parameter_value) VALUES ('apps.torrents.qbittorrent_ip', '192.168.0.33');
INSERT INTO config (parameter_name, parameter_value) VALUES ('apps.torrents.qbittorrent_port', '8124');
INSERT INTO config (parameter_name, parameter_value) VALUES ('apps.torrents.qbittorrent_login', NULL);
INSERT INTO config (parameter_name, parameter_value) VALUES ('apps.torrents.qbittorrent_password', NULL);
INSERT INTO config (parameter_name, parameter_value) VALUES ('apps.weather.enabled', 'True');
INSERT INTO config (parameter_name, parameter_value) VALUES ('apps.weather.city', 'Екатеринбург');
INSERT INTO config (parameter_name, parameter_value) VALUES ('apps.drives_monitor.enabled', 'True');
INSERT INTO config (parameter_name, parameter_value) VALUES ('apps.system_monitor.enabled', 'True');
INSERT INTO config (parameter_name, parameter_value) VALUES ('apps.system_monitor.cpu_monitor', 'True');
INSERT INTO config (parameter_name, parameter_value) VALUES ('apps.system_monitor.ram_monitor', 'True');
INSERT INTO config (parameter_name, parameter_value) VALUES ('apps.system_monitor.swap_monitor', 'True');
INSERT INTO config (parameter_name, parameter_value) VALUES ('apps.system_monitor.network_speed', 'True');

INSERT INTO
  header_links (header_group_name, header_group_content)
VALUES
  (
    'Внешние утилиты',
    '{
    "Настройка сервера": [
        {
            "link_name": "Webmin",
            "link_href": "https://192.168.0.33:10000/"
        },
        {
            "link_name": "Параметры ПО",
            "link_href": "/settings?l=y"
        }
    ],
    "Торрент клиенты": [
        {
            "link_name": "qBittorrent",
            "link_href": "http://192.168.0.33:8124/"
        }
    ],
    "Wiki-ресурсы": [
        {
            "link_name": "Kiwix",
            "link_href": "http://192.168.0.33:789/"
        }
    ]
}'
  );

INSERT INTO
  header_links (header_group_name, header_group_content)
VALUES
  (
    'Медиа и файлы',
    '{
    "Плееры": [
        {
            "link_name": "Видеоплеер",
            "link_href": "/players/video?l=y"
        },
        {
            "link_name": "Аудиоплеер",
            "link_href": "/players/audio?l=y"
        }
    ],
    "Управление файлами": [
        {
            "link_name": "Файловый менеджер",
            "link_href": "/files?l=y"
        },
        {
            "link_name": "Управление торрентом",
            "link_href": "/torrents?l=y"
        }
    ]
}'
  );

INSERT INTO
  header_links (header_group_name, header_group_content)
VALUES
  (
    'Ведение учета',
    '{
    "Календари": [
        {
            "link_name": "Календарь",
            "link_href": "/calendar?l=y"
        },
        {
            "link_name": "To-do",
            "link_href": "/calendar/to-do?l=y"
        }
    ],
    "Финансы": [
        {
            "link_name": "Бюджет",
            "link_href": "/bugdet?l=y"
        },
        {
            "link_name": "Контроль подписок",
            "link_href": "/budget/subscriptions?l=y"
        }
    ]
}'
  );