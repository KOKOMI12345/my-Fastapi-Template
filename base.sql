-- Active: 1695991712872@@127.0.0.1@3306

-- 这里面写网站需要用到的SQL语句和各种表项 --

CREATE DATABASE IF NOT EXISTS `furina`;

use furina;

CREATE TABLE IF NOT EXISTS user (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password BINARY(64) NOT NULL,
    salt BINARY(32) NOT NULL,
    email VARCHAR(255),
    avatarPath VARCHAR(255)
);



CREATE TABLE if NOT exists posts (
    id INTEGER PRIMARY KEY,
    author VARCHAR(255) NOT NULL,
    title TEXT,
    content TEXT,
    create_time DATETIME,
    update_time DATETIME,
    user_avatar TEXT,
    likes INTEGER DEFAULT 0
);

ALTER TABLE posts ADD UNIQUE INDEX idx_title_content (title(255), content(255));
ALTER TABLE `posts` ADD INDEX idx_author (author);
ALTER TABLE `user` ADD INDEX idx_username (username);
