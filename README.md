# Alaska bear api testing
### Содержание репозитория
- код автотестов
- в файле test_cases.xlsx описаны тест-кейсы 

### Запуск тестов
1. Запускается командой в cmd из корневой папки

`pytest [--alluredir=<report dir>] [--baseurl=<url>]`

`<report dir>` - путь к папке с результатами для генерации allure отчета 

`<url>` - api url, например `http://localhost:9999`, по умолчанию `http://localhost:8099`

2. Генерация allure отчета

`allure serve <report dir>`

`<report dir>` - путь к папке с результатами

### Environment
- python 3.9
- зависимости от внешних пакетов собраны в requirements.txt
- allure 2.17.3
