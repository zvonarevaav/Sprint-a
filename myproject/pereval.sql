-- Создание таблицы pereval_added, если она еще не существует
CREATE TABLE IF NOT EXISTS "public"."pereval_added" (
    "id" SERIAL PRIMARY KEY
);

-- Создание таблицы пользователей, если она еще не существует
CREATE TABLE IF NOT EXISTS "public"."users" (
    "id" SERIAL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "name" VARCHAR(255) NOT NULL,
    "phone" VARCHAR(20),
    "date_joined" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Изменение структуры таблицы pereval_added
ALTER TABLE IF EXISTS "public"."pereval_added"
ADD COLUMN "user_id" INT REFERENCES "public"."users"("id"),
ADD COLUMN "beautyTitle" VARCHAR(255),
ADD COLUMN "title" VARCHAR(255),
ADD COLUMN "other_titles" VARCHAR(255),
ADD COLUMN "connect" TEXT,
ADD COLUMN "add_time" TIMESTAMP;

-- Создание таблицы координат, если она еще не существует
CREATE TABLE IF NOT EXISTS "public"."coords" (
    "id" SERIAL PRIMARY KEY,
    "latitude" FLOAT NOT NULL,
    "longitude" FLOAT NOT NULL,
    "height" INT NOT NULL
);

-- Добавление связи с таблицей координат
ALTER TABLE IF EXISTS "public"."pereval_added"
ADD COLUMN "coord_id" INT REFERENCES "public"."coords"("id");

-- Добавление уровней сложности перевалов
ALTER TABLE IF EXISTS "public"."pereval_added"
ADD COLUMN "winter_level" VARCHAR(50),
ADD COLUMN "summer_level" VARCHAR(50),
ADD COLUMN "autumn_level" VARCHAR(50),
ADD COLUMN "spring_level" VARCHAR(50);

-- Создание таблицы изображений перевалов, если она еще не существует
CREATE TABLE IF NOT EXISTS "public"."pereval_images" (
    "id" SERIAL PRIMARY KEY,
    "pereval_id" INT REFERENCES "public"."pereval_added"("id"),
    "image_url" TEXT NOT NULL
);

-- Удаление полей raw_data и images, если они существуют
ALTER TABLE IF EXISTS "public"."pereval_added"
DROP COLUMN IF EXISTS "raw_data",
DROP COLUMN IF EXISTS "images";
