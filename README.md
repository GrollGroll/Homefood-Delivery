<div id="header" align="center">
  <img src="/logo.png" width="200"/>

# Домашний Шеф

Проект "Домашний Шеф" представляет собой платформу для заказа и доставки домашней еды, где пользователи могут размещать свои заказы на приготовление блюд.

## Суть проекта

1. **Размещение заказа**: Пользователи могут размещать заказы на приготовление конкретных блюд, указывая предпочтения и дополнительные требования.

2. **Подбор повара**: Заказы видны зарегистрированным пользователям, которые умеют готовить. Повара могут принимать заказы, которые соответствуют их навыкам и предпочтениям.

3. **Приготовление и упаковка**: Повар готовит выбранные блюда согласно заказу, упаковывает и готовит к доставке.

4. **Доставка и оплата**: После получения еды заказчик осуществляет оплату. Это гарантирует прозрачность и защиту интересов обеих сторон.

5. **Личные повара**: В дальнейшем платформа предлагает возможность выбора личного повара для постоянных клиентов, упрощая процесс заказа и повышая удовлетворение от обслуживания.

6. **Сообщения и отзывы**: Клиенты могут общаться с поваром через личные сообщения, уточнять детали заказа и оставлять отзывы о качестве услуг.

Проект "Домашний Шеф" нацелен на предоставление доступной и качественной домашней еды для клиентов, а также создание возможностей для домохозяек и любителей готовить зарабатывать на своем умении.

## Реализация

<details> 
<summary> Архитектура и компоненты сервера </summary>


1. **API сервер (FastAPI)**
   - **Регистрация и авторизация**: Пользователи могут зарегистрироваться и войти в систему. Разделение на типы пользователей: заказчик и повар.
   - **Создание заказа**: Заказчики могут создавать заказы, указывая детали блюда, предпочтительное время доставки и другую информацию.
   - **Просмотр и отклик на заказ**: Повар может просматривать доступные заказы и откликаться на них. Заказчик выбирает повара из откликнувшихся.
   - **Управление заказами**: Заказчики могут отслеживать статус своих заказов, а повара — управлять принятыми заказами.
   - **Система рейтингов и отзывов**: Заказчики могут оставлять отзывы и рейтинги после получения заказа.
   - **Планирование и подписка**: Возможность создания повторяющихся заказов и подписки на регулярные поставки еды.
   - **Личные сообщения**: Введение системы личных сообщений для прямой коммуникации между заказчиками и поварами.

2. **База данных (PostgreSQL)**

   - **Пользователи**: Таблицы для хранения информации о пользователях (регистрация, авторизация, типы пользователей).
   - **Заказы**: Таблицы для хранения информации о заказах (детали блюда, статус, заказчик, повар).
   - **Рейтинги и отзывы**: Таблицы для хранения отзывов и рейтингов.
   - **История заказов**: Таблицы для хранения истории заказов и транзакций.
   - **Планирование заказов**: Таблицы для хранения информации о повторяющихся заказах и подписках.

3. **Сообщения и асинхронная обработка (Kafka)**

   - **Очередь заказов**: Использование Kafka для обработки заказов и уведомлений (например, новые заказы, отклики поваров).
   - **Уведомления**: Асинхронные уведомления пользователям о статусах заказов (создан, принят, готов, доставлен).
   - **Логирование и аналитика**: Сбор данных для логирования и аналитики через Kafka.

4. **Контейнеризация и развертывание (Docker)**

   - **API сервер**: Контейнеризация FastAPI приложения.
   - **База данных**: Контейнеризация PostgreSQL.
   - **Kafka**: Контейнеризация Kafka брокера и необходимых компонентов.
   - **Оркестрация**: Использование Docker Compose или Kubernetes для управления контейнерами и их зависимостями.
</details>

<details> 
<summary> Логика работы сервера </summary>

1. **Регистрация и авторизация**

   - Пользователь регистрируется на платформе, указывая свои данные и выбирая тип пользователя (заказчик или повар).
   - Данные пользователя сохраняются в PostgreSQL.
   - Пользователь авторизуется и получает токен доступа для дальнейших действий.

2. **Создание заказа**

   - Заказчик создает новый заказ через API, указывая детали блюда, предпочтительное время доставки и другую информацию.
   - Данные заказа сохраняются в PostgreSQL и отправляются в очередь Kafka для обработки.
    
3. **Просмотр и отклик на заказ**

   - Повар просматривает доступные заказы через API.
   - Повар откликается на интересующий заказ, и его отклик сохраняется в PostgreSQL.
   - Заказчик получает уведомление о новых откликах через Kafka.

4. **Выбор повара и подтверждение заказа**

   - Заказчик просматривает отклики и выбирает повара.
   - Заказ обновляется в PostgreSQL, и повар получает уведомление о принятии заказа через Kafka.

5. **Управление заказами**

   - Повар обновляет статус заказа (готовится, готов, доставлен) через API.
   - Заказчик получает уведомления о каждом изменении статуса через Kafka.

6. **Рейтинги и отзывы**

   - После получения заказа заказчик оставляет отзыв и рейтинг через API.
   - Отзыв и рейтинг сохраняются в PostgreSQL и доступны для просмотра другим пользователям.

7. **Планирование и подписка**

   - Заказчик может создавать повторяющиеся заказы или подписываться на регулярные поставки еды.
   - Данные о планируемых заказах сохраняются в PostgreSQL и обрабатываются через асинхронные задачи с использованием Kafka.


</details>

## План реализации

FastAPI хэндлеры:


- [ ] Регистрация и авторизация
- [ ] Создание заказа
- [ ] Просмотр и отклик на заказ
- [ ] Управление заказами
- [ ] Система рейтингов и отзывов
- [ ] Планирование и подписка
- [ ] Личные сообщения
- [ ] Управление заказами


База данных:


- [ ] Пользователи
- [ ] Заказы
- [ ] Рейтинги и отзывы
- [ ] История заказов
- [ ] Планирование заказов


Kafka:


- [ ] Очередь заказов
- [ ] Уведомления
- [ ] Логирование и аналитика
