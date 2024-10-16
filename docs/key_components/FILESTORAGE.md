# Структура файлового хранилища
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


## Пояснения по структуре БД.
### Описание расположения файла
В таблице `filestorage_files` есть несколько колонок, описывающее местонахождение файла:
- `category_id` (int) - идентификатор категории
- `type_id` (int) - идентификатор типа
- `filename` (text) - название файла с расширением
- `way` (text) - путь до файла (по умолчанию - `/`)
- `is_absolute_way` (bool) - указатель, является ли указанный путь абсолютным или относительным (по отношению к **baseway**)
Если файл находится без подпапок в стандартной для этого категории и типа папке, то в поле `way` указывается символ `/`. Если же файл находится в дополнительной подпапке после `filetype`, то они все указываются в этом поле, с добавлением символа `/` в начале и в конце (напр. `/2021/02/31/`). 
Если же указать `is_absolute_way = True`, то `way` может быть любым.

### Поиск и подпапки
В родительской папке **filetype** может быть сколь угодно подпапок, в поиске они все равно будут фигурировать под типом **filetype**.   
Например, если в папке **filetype** находится файл по пути `filetype/2021/02/31/DSC0001.jpg`, то в поиске его можно будет найти лишь по имени файла, а не по дополнительным атрибутам.   
Такое поведение будет исправлено в будущем.