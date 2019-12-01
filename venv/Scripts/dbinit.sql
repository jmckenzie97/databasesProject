CREATE DATABASE IF NOT EXISTS `petFinder` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `petFinder`;

CREATE TABLE IF NOT EXISTS `users` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `adopters` (
	`adopterid` int(11) NOT NULL AUTO_INCREMENT,
  	`age` int(3) NOT NULL,
  	`hometype` varchar(255) NOT NULL,
    `userid` int(11),
    PRIMARY KEY (`adopterid`),
    FOREIGN  KEY(`userid`) REFERENCES users(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `owners` (
	`ownerid` int(11) NOT NULL AUTO_INCREMENT,
  	`age` int(3) NOT NULL,
  	`familysize` int(5) NOT NULL,
    `userid` int(11),
    PRIMARY KEY (`ownerid`),
    FOREIGN KEY(`userid`) REFERENCES users(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `pets` (
	`petid` int(11) NOT NULL AUTO_INCREMENT,
	`pet` varchar(50) NOT NULL,
	`name` varchar(50) NOT NULL,
	`breed` varchar(50) NOT NULL,
	`weight` int(3) NOT NULL,
    `owner` int(11),
    PRIMARY KEY (`petid`),
    FOREIGN KEY (`owner`) REFERENCES owners(ownerID)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

