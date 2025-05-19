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


--Event: habit_logging for adding habits to log at midnight i.e. start of the day

create event habit_logging
on schedule 
    every 1 day 
    starts current_date + interval 1 day
do
    insert into user_logs (user_habit_id,status)
    select user_habit_id,'skipped' from user_habits where is_active = TRUE;

--Procedure: streak_total_points_update Updates streak count and calculates total_points

DELIMITER $$

CREATE PROCEDURE streak_total_points_update()
BEGIN
    DECLARE user_id INT;
    DECLARE user_done INT DEFAULT 0;
    DECLARE total_points DECIMAL(12,2) DEFAULT 0;
    DECLARE habit_count INT DEFAULT 0;
    DECLARE i INT DEFAULT 0;
    DECLARE user_habit_id INT;
    DECLARE status ENUM('done', 'skipped', 'not done');
    DECLARE points DECIMAL(12,2) DEFAULT 0;

    DECLARE user_cursor CURSOR FOR SELECT user_id, total_points FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET user_done = 1;
    
    CREATE TEMPORARY TABLE temp_data (
        user_habit_id INT, 
        status ENUM('done', 'skipped', 'not done'), 
        points DECIMAL(12,2)
    );
    
    OPEN user_cursor;

    user_loop: LOOP
        FETCH user_cursor INTO user_id, total_points;
        IF user_done THEN
            LEAVE user_loop;
        END IF;
        
        DELETE FROM temp_data;
        INSERT INTO temp_data (user_habit_id, status, points)
        SELECT ul.user_habit_id, ul.status, ul.points
        FROM user_logs ul 
        JOIN user_habits uh ON ul.user_habit_id = uh.user_habit_id
        WHERE ul.log_date = CURDATE() AND uh.user_id = user_id;
        
        SET i = 0;
        SELECT COUNT(*) INTO habit_count FROM temp_data;
        
        WHILE i < habit_count DO
            SELECT user_habit_id, status, points 
            INTO user_habit_id, status, points 
            FROM temp_data 
            ORDER BY user_habit_id 
            LIMIT i, 1;
            
            SET total_points = total_points + points;
            
            IF status = 'done' THEN
                UPDATE user_habits 
                SET current_streak = current_streak + 1 
                WHERE user_habit_id = user_habit_id;
            ELSE
                UPDATE user_habits 
                SET current_streak = 0 
                WHERE user_habit_id = user_habit_id;
            END IF;
            
            SET i = i + 1;
        END WHILE;
        
        IF total_points < 0 THEN
            SET total_points = 0;
        END IF;
        
        UPDATE users 
        SET total_points = total_points 
        WHERE user_id = user_id;
    END LOOP user_loop;

    CLOSE user_cursor;
END$$

DELIMITER ;

--Event: streak_update_event calls streak_total_points_update before midnight i.e. end of the day

DELIMITER $$

CREATE EVENT streak_update_event
ON SCHEDULE EVERY 1 DAY
STARTS TIMESTAMP(CURDATE()) + INTERVAL 23 HOUR + INTERVAL 59 MINUTE
DO
BEGIN
    CALL streak_total_points_update();
END$$

DELIMITER ;


