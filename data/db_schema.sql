-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema forum_system_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `forum_system_db` ;
USE `forum_system_db` ;

-- -----------------------------------------------------
-- Table `forum_system_db`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `is_private` TINYINT(4) NOT NULL,
  `is_locked` TINYINT(4) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_system_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `is_admin` TINYINT(4) NOT NULL,
  `avatar_url` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_name_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 16;


-- -----------------------------------------------------
-- Table `forum_system_db`.`categories_has_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`categories_has_users` (
  `category_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `has_right_access` TINYINT(4) NOT NULL,
  PRIMARY KEY (`category_id`, `user_id`),
  INDEX `fk_categories_has_users_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_categories_has_users_categories1_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_categories_has_users_categories1`
    FOREIGN KEY (`category_id`)
    REFERENCES `forum_system_db`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_categories_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_system_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_system_db`.`conversations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`conversations` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(90) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_system_db`.`conversations_has_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`conversations_has_users` (
  `conversation_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`conversation_id`, `user_id`),
  INDEX `fk_conversations_has_users_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_conversations_has_users_conversations1_idx` (`conversation_id` ASC) VISIBLE,
  CONSTRAINT `fk_conversations_has_users_conversations1`
    FOREIGN KEY (`conversation_id`)
    REFERENCES `forum_system_db`.`conversations` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_conversations_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_system_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_system_db`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`messages` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `conversation_id` INT(11) NOT NULL,
  `sender_id` INT(11) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  PRIMARY KEY (`id`),
  INDEX `fk_messages_conversations1_idx` (`conversation_id` ASC) VISIBLE,
  INDEX `fk_messages_users1_idx` (`sender_id` ASC) VISIBLE,
  CONSTRAINT `fk_messages_conversations1`
    FOREIGN KEY (`conversation_id`)
    REFERENCES `forum_system_db`.`conversations` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_messages_users1`
    FOREIGN KEY (`sender_id`)
    REFERENCES `forum_system_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 9;


-- -----------------------------------------------------
-- Table `forum_system_db`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`topics` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `content` TEXT NOT NULL,
  `category_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `is_locked` TINYINT(4) NOT NULL,
  `best_reply_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_topics_categories_idx` (`category_id` ASC) VISIBLE,
  INDEX `fk_topics_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_topics_best_reply` (`best_reply_id` ASC) VISIBLE,
  CONSTRAINT `fk_topics_best_reply`
    FOREIGN KEY (`best_reply_id`)
    REFERENCES `forum_system_db`.`replies` (`id`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_categories`
    FOREIGN KEY (`category_id`)
    REFERENCES `forum_system_db`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_system_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 13;


-- -----------------------------------------------------
-- Table `forum_system_db`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`replies` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(255) NOT NULL,
  `topic_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  PRIMARY KEY (`id`),
  INDEX `fk_replies_topics1_idx` (`topic_id` ASC) VISIBLE,
  INDEX `fk_replies_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_replies_topics1`
    FOREIGN KEY (`topic_id`)
    REFERENCES `forum_system_db`.`topics` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_system_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_system_db`.`votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`votes` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `reply_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `type_vote` ENUM('up', 'down') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `users_id_UNIQUE` (`user_id` ASC, `reply_id` ASC) VISIBLE,
  INDEX `fk_votes_replies1_idx` (`reply_id` ASC) VISIBLE,
  INDEX `fk_votes_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_votes_replies1`
    FOREIGN KEY (`reply_id`)
    REFERENCES `forum_system_db`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_votes_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_system_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
