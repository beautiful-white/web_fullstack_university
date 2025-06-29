# Структура папок для изображений ресторанов

## Общая структура
```
static/restaurants/images/
├── restaurant_1/          # Папка для ресторана с ID = 1
│   ├── main.jpg          # Главное изображение ресторана
│   ├── gallery_1.jpg     # Изображения галереи
│   ├── gallery_2.jpg
│   ├── menu_1.jpg        # Изображения меню
│   └── menu_2.jpg
├── restaurant_2/          # Папка для ресторана с ID = 2
│   ├── main.jpg
│   ├── gallery_1.jpg
│   └── menu_1.jpg
└── restaurant_3/          # Папка для ресторана с ID = 3
    ├── main.jpg
    └── gallery_1.jpg
```

## Правила именования файлов

### Главное изображение:
- `main.jpg` - главное изображение ресторана (интерьер)

### Галерея:
- `gallery_1.jpg`, `gallery_2.jpg`, `gallery_3.jpg` и т.д.
- Дополнительные фотографии интерьера ресторана

### Меню:
- `menu_1.jpg`, `menu_2.jpg`, `menu_3.jpg` и т.д.
- Фотографии блюд и меню ресторана

## Поддерживаемые форматы
- JPG/JPEG
- PNG
- WebP

## Рекомендуемые размеры
- Главное изображение: 800x600px
- Галерея: 600x400px
- Меню: 500x400px

## Как добавить изображения для нового ресторана

1. Создайте папку `restaurant_X` где X - ID ресторана
2. Поместите изображения в эту папку с правильными именами
3. В админ панели используйте пути вида:
   - Главное: `/static/restaurants/images/restaurant_X/main.jpg`
   - Галерея: `/static/restaurants/images/restaurant_X/gallery_1.jpg`
   - Меню: `/static/restaurants/images/restaurant_X/menu_1.jpg`

## Примеры путей для ресторана с ID = 1:
- Главное изображение: `/static/restaurants/images/restaurant_1/main.jpg`
- Галерея: `/static/restaurants/images/restaurant_1/gallery_1.jpg`
- Меню: `/static/restaurants/images/restaurant_1/menu_1.jpg` 