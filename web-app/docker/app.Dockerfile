FROM php:8-fpm-alpine

LABEL maintainer="@obokaiwele <github.com/obokaiwele>"

# Install Postgres PDO driver
RUN apk --no-cache add postgresql-dev \
  && docker-php-ext-install pdo pdo_pgsql bcmath
