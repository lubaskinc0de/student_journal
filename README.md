<p align="center">
  <img width="200" height="200" src="https://github.com/user-attachments/assets/f6fc890b-4a40-461a-a8fc-5cbf5237e6af" />
</p>

# Описание
Специализированное приложение для ведения школьного дневника: 
календарь и заметки с функцией записи домашнего задания

Основные функции приложения:

1. Создание, редактирование и просмотр расписания уроков по дням недели 🗓️.

2. Создание, редактирование и просмотр личной информации ученика

3. Создание, редактирование и просмотр информации о преподавателях 🧑‍🏫.

4. Просмотр расписания в виде таблицы 📝.

5. Добавление оценок за уроки и расчет среднего балла по предметам в виде таблицы.

7. Отображение предстоящего домашнего задания в формате ToDo-списка ✅.

Технологический стек:

- Python 🐍
- SQLite 🗃️
- PyQt6 🖥️
- Qt-Designer 🛠️
- Adaptix
- Dishka

Миссия проекта:

Создать удобную платформу для ведения личного школьного дневника,
которая помогает школьникам эффективно организовывать своё расписание и задания. 
Это приложение способствует улучшению успеваемости путём структурирования учебной информации 
и предоставления полезных инструментов для её анализа и контроля 🎯.

**Разработано как проект для Я.Лицея**

# Установка проекта

### 1. Установить готовый бинарник

Вы можете найти готовые исполняемые файлы на странице [релизов](https://github.com/lubaskinc0de/student_journal/releases)
в репозитории. Просто скачайте и запустите (протестировано на Windows11, Windows10 и Arch Linux)

Если по какой-то причине вам не удается запустить бинарный файл, вы можете попробовать собрать приложение из исходного кода.

### 2. Сборка из исходного кода
*(все действия ниже выполняются в виртуальном окружении)*

**Требования**:
- cpython версии от ``3.11`` до ``3.12`` (было протестировано на python ``3.11.9``)
- возможно, у вас получится собрать проект на другой версии, но это не проверялось.

Чтобы собрать приложение из исходного кода, вам потребуется

1. установить проект и его зависимости
```cmd
pip install -e .
```

2. установить pyinstaller
```
pip install pyinstaller
```

3. собрать бинарник

```
pyinstaller student-journal.spec
```

Известные проблемы:

1. ``DLL load failed ...``
Ошибка была замечена преимущественно на Windows и связана с неправильной установкой самого Qt, в случае подобной ошибки рекомендуется установить PyQt6 версии 6.7.1
вместо указанной в проекте

```
pip uninstall pyqt6
pip install pyqt6==6.7.1
```

если это не помогло, стоит попробовать сделать это несколько раз в разных виртуальных окружениях, или просто запускать проект из исходного кода, как описано ниже.

2. ``no module named PyQt6.sip...``
Стоит сделать то же что и в
первом случае


# Запуск приложения без исполняемого файла 

В случае сборки из исходного кода, вы можете запустить приложение и без сборки его в исполняемый файл, для этого вам необходимо также установить проект со всеми его зависимостями и выполнить

```
student_journal run gui
```

команда student_journal будет доступна в том виртуальном окружении где установлен пакет приложения.

вы можете также просто запустить файл 
``student_journal/bootstrap/entrypoint/qt.py``

Некоторые замечания по поводу работы приложения:

1. Не забывайте нажать кнопку "Обновить". Например, вы можете открыть список предметов, потом добавить какой то предмет и снова открыть список предметов. Он не отобразится там сам, нужнох нажать кнопку "Обновить", также и с большинством других виджетов, изменения будут видны только после обновления, не забывайте про это. В будущем возможно внедрение авто-обновления виджетов.

2. Вы можете добавить урок на воскресенье, и будет отображена неделя с ним в расписании, но самого урока там не будет. Это не баг. Просто обычно в воскресенье уроки не проводятся, и поэтому в таблице он не будет отображаться, в будущем мы пересмотрим это решение для улучшения UX.

3. При добавлении урока не пытайтесь сразу добавить к нему домашнее задание - будет ошибка. Прикрепить задание можно в меню редактирования урока

4. Чтобы перейти в меню редактирования урока, откройте расписание, нужную неделю и кликните по уроку 2 раза ЛКМ

5. Чтобы работать с расписанием, сначала выберите месяц и год, потом в списке - выберите неделю, будут отображены только те недели, в которых есть уроки. Чтобы добавить первый урок - перейдите в Уроки -> Добавить урок

6. Часовой пояс устанавливается автоматически на основании системного при первом запуске.

7. Все данные приложения будут лежать по пути ваш_пользователь/student_journal

8. Чтобы начать сначала, удалите все данные приложения по пути

9. После заполнения тестовыми данными, уроки заполняются на текущий месяц и год

# Структура проекта

<p align="center">
  <img width="400" height="200" src="https://github.com/user-attachments/assets/5fb796c5-467d-41b3-9cbd-181e0cef5f15" />
</p>

## Domain (ядро)
- ``student_journal/domain``
- Содержит основные сущности приложения (без логики)

## Application (приложение)
- ``student_journal/application``
- Содержит основную бизнес логику приложения (``интеракторы``)
- Содержит интерфейсы для адаптеров (``common``)
- Содержит валидацию бизнес-данных (``invariants``)
- Содержит классы ошибок бизнес логики

## Adapters (адаптеры)
- ``student_journal/adapters``
- Содержит реализацию интерфейсов ``application``
- Содержит работу с БД ``db/gateway``
- Содержит схему бд ``db/schema``
- Содержит необходимые адаптеры для БД ``db/``
- Содержит ошибки уровня адаптеров
- Содержит компоненты работы с конфигами ``config.py``
- Содержит реализацию IdProvider ``id_provider.py``
- Содержит универсальный ErrorLocator ``error_locator.py``

## Presentation (представление)
- ``student_journal/presentation``
- Содержит в себе логику работы с представлением
- Содержит логику работы с Qt
- Содержит скомпилированные UI-классы ``ui/``
- Содержит необходимые приложению ресурсы ``resource/``
- Содержит виджеты приложения ``widget/``

## Bootstrap (сборка)
- ``student_journal/bootstrap``
- Отвечает за сборку и запуск приложения
- Содержит настройки di-контейнера (``di/``)
- Содержит точки входа в представления (``entrypoint/``)

## Tests (тесты)
- ``tests/``
- Тесты