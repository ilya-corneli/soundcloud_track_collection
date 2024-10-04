# soundcloud_track_collection
###Установка необходимых библиотек:
pip install beautifulsoup4 requests
pip install selenium

### Скачивание и установка ChromeDriver:
Перейдите на страницу загрузки ChromeDriver: https://chromedriver.chromium.org/downloads
Найдите версию ChromeDriver, которая соответствует версии Chromium вашего Brave (или ближайшую к ней).
Скачайте zip-архив для вашей операционной системы (Windows, Mac, Linux).
Установка ChromeDriver:
Распакуйте скачанный архив.
Внутри будет файл chromedriver (или chromedriver.exe в Windows).

Скопируйте файл chromedriver.exe в папку, которая находится в переменной окружения PATH.
Это может быть, например, C:\Windows или C:\Windows\System32.
Либо, добавьте путь к папке с chromedriver.exe в переменную PATH.
Нажмите Win + R, введите sysdm.cpl и нажмите Enter.
Перейдите на вкладку "Дополнительно", нажмите "Переменные среды".
В разделе "Системные переменные" найдите переменную "Path" и нажмите "Изменить".
Нажмите "Создать" и добавьте путь к папке с chromedriver.exe.
Нажмите "ОК" во всех окнах.

Важно:
Замените r"C:\Windows\System32\chromedriver-win64\chromedriver-win64\chromedriver.exe" на фактический путь к вашему файлу chromedriver.exe.

Замените https://soundcloud.com/ilyacorneli/likes на URL вашей страницы с лайками.
