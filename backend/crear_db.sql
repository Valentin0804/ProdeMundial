-- Ejecutar en MySQL como root
CREATE DATABASE IF NOT EXISTS prode_mundial
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'prode_user'@'localhost' IDENTIFIED BY 'tu_password_aqui';
GRANT ALL PRIVILEGES ON prode_mundial.* TO 'prode_user'@'localhost';
FLUSH PRIVILEGES;
