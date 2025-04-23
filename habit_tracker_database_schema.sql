--Habit_Tracker datbase creation
DROP DATABASE IF EXISTS Habit_Tracker;
CREATE DATABASE Habit_Tracker;

--Creating Habit_Tracker datbase schema
USE Habit_Tracker;

create table users( 
                user_id int auto_increment,
                username varchar(50) unique not null,
                password_hash varchar(255) not null,
                total_points decimal(12,2) default 0,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at datetime default current_timestamp,
                updated_at datetime default current_timestamp on update current_timestamp,
                constraint pk_users primary key (user_id)
);

create table habits( 
                habit_id int auto_increment,
                habit_name varchar(50) unique not null,
                habit_description varchar(500),
                points_per_day int default 10,
                constraint pk_habits primary key (habit_id)
);

create table user_habits( 
                user_habit_id int auto_increment,
                user_id int,
                habit_id int,
                start_date datetime default current_timestamp,
                updated_at datetime default current_timestamp on update current_timestamp,
                frequency ENUM('daily','weekly','monthly') not null,
                goal varchar(100),
                is_active boolean default TRUE ,
                current_streak int default 0,
                constraint fk_user_id_user_habits foreign key (user_id) references users(user_id) on delete cascade,
                constraint fk_habit_id_user_habits foreign key (habit_id) references habits(habit_id) on delete cascade,
                constraint pk_user_habits primary key (user_habit_id)
);

create table user_logs(
                user_habit_id int ,
                log_date date default current_date,
                status ENUM('not done','skipped','done') default 'skipped',
                points decimal(12,2) default -1,
                constraint fk_user_habit_id_user_logs foreign key (user_habit_id) references user_habits(user_habit_id) on delete cascade,
                constraint pk_user_logs primary key (user_habit_id,log_date)
);

set global event_scheduler=on;

--Creating Events 

create event habit_logging
on schedule 
    every 1 day 
    starts current_date + interval 1 day
do
    insert into user_logs (user_habit_id,status)
    select user_habit_id,'skipped' from user_habits where is_active = TRUE;



