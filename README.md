# Разработка приостановлена.

# home_server

## Описание приложения
### Структура файлового хранилища
В приложении принята следующая структура файлового хранилища
```
baseway/
├── category/
│   ├── filetype/
│   │   └── filename.mp4
│   └── filetype/
│       └── filename.csv
└── category/
    ├── filetype/
    │   └── filename.mp3
    └── filetype/
        └── filename.html
```
- **baseway** - основной путь, в котором будет находиться библиотека файлов
- **category** - категория файлов (apps/videos/photos)
- **filetype** - подкатегория файла (вид приложения/год съемки видео/место снятия фотографий)
- **filename** - название файлов

## Порядок ручной установки
### 1. Клонируйте репозиторий на свой компьютер/сервер.
### 2. Установите зависимости приложения.
### 3. Подготовьте файловое хранилище.
### 4. Подготовьте базу данных и файловое хранилище.
Откройте [файл](create_database_and_storage.py), введите параметры в начале файла и запустите выполнение файла. После выполнения файла, в Вашей БД и файловой системе будет создано все необходимое для работы приложения. 
### 5. Настройте автозапуск приложения при запуске системы.
