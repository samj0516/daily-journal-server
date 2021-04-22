CREATE TABLE `Entries` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `date` VARCHAR NOT NULL,
    `concept` TEXT NOT NULL, 
    `entry` TEXT NOT NULL, 
    `mood_id` INTEGER NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

CREATE TABLE `Mood` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`label`	TEXT NOT NULL
);


INSERT INTO `Mood` VALUES (null, "Happy");
INSERT INTO `Mood` VALUES (null, "Excited");
INSERT INTO `Mood` VALUES (null, "Content");
INSERT INTO `Mood` VALUES (null, "Confused");
INSERT INTO `Mood` VALUES (null, "Sad");
INSERT INTO `Mood` VALUES (null, "Nervous");
INSERT INTO `Mood` VALUES (null, "Confident");
INSERT INTO `Mood` VALUES (null, "Enlightened");
INSERT INTO `Mood` VALUES (null, "Whelmed");

SELECT *
    FROM Mood;

INSERT INTO 'Entries' VALUES (null, "04-13-2021", "React", "This shit is hard!", 9)

ALTER TABLE `Entries`
    ADD `instructor_id` INTEGER NOT NULL
    FOREIGN KEY(`instructor_id`) REFERENCES `Instructor`(`id`);

DROP TABLE `Entries`;

CREATE TABLE `Entries` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `date` VARCHAR NOT NULL,
    `concept` TEXT NOT NULL, 
    `entry` TEXT NOT NULL, 
    `mood_id` INTEGER NOT NULL,
    `instructor_id` INTEGER NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
    FOREIGN KEY(`instructor_id`) REFERENCES `Instructor`(`id`)
);

CREATE TABLE 'Instructors' (
    'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'first_name' TEXT NOT NULL
);

INSERT INTO `Instructors` VALUES (null, 'Jisie');
INSERT INTO `Instructors` VALUES (null, 'Scott');
INSERT INTO `Instructors` VALUES (null, 'Adam');
INSERT INTO `Instructors` VALUES (null, 'Hannah');
INSERT INTO `Instructors` VALUES (null, 'Sage');
INSERT INTO `Instructors` VALUES (null, 'Aja');
INSERT INTO `Instructors` VALUES (null, 'Bryan');

INSERT INTO `Entries` VALUES (null, "04-13-2021", "React", "This shit is hard!", 9, 1)
INSERT INTO `Entries` VALUES (null, "03-09-2021", "Capstone", "I can't stop fiddling with the stylsheet!", 2, 5)

SELECT * FROM Entries;