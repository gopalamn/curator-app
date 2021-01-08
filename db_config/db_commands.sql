create table users (
user_id integer not null auto_increment,
email varchar(128) not null unique,
username varchar(32),
password_hash varchar(128),
firstname varchar(32),
lastname varchar(32),
profile_pic text,
profile_pic_key text,
primary key(user_id),
index(email),
index(username)
)Engine=Innodb default charset utf8;

create table individual_book_posts (
book_post_id integer not null auto_increment,
book_api_id varchar(32) not null,
user_id integer not null,
title varchar(128) not null,
cover_img text,
link text,
created_time datetime not null,
primary key(book_post_id),
foreign key(user_id) references users(user_id) on update cascade on delete cascade
)Engine=Innodb default charset utf8;