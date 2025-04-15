-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema forum_system_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema forum_system_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `forum_system_db` ;
USE `forum_system_db` ;

-- -----------------------------------------------------
-- Table `forum_system_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `is_admin` TINYINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_name_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_system_db`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `is_private` TINYINT NOT NULL,
  `is_locked` TINYINT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_system_db`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`topics` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `content` TEXT(1000) NOT NULL,
  `categories_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `is_locked` TINYINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_topics_categories_idx` (`categories_id` ASC) VISIBLE,
  INDEX `fk_topics_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_topics_categories`
    FOREIGN KEY (`categories_id`)
    REFERENCES `forum_system_db`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_system_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_system_db`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`replies` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(45) NULL,
  `topics_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `text_UNIQUE` (`text` ASC) VISIBLE,
  INDEX `fk_replies_topics1_idx` (`topics_id` ASC) VISIBLE,
  INDEX `fk_replies_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_replies_topics1`
    FOREIGN KEY (`topics_id`)
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
-- Table `forum_system_db`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `text` TEXT(1000) NOT NULL,
  `sender_id` INT NOT NULL,
  `receiver_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_messages_users1_idx` (`sender_id` ASC) VISIBLE,
  INDEX `fk_messages_users2_idx` (`receiver_id` ASC) VISIBLE,
  INDEX `idx_messages_sender_id_receiver_id` (`sender_id` ASC, `receiver_id` ASC) VISIBLE,
  CONSTRAINT `fk_messages_users1`
    FOREIGN KEY (`sender_id`)
    REFERENCES `forum_system_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_messages_users2`
    FOREIGN KEY (`receiver_id`)
    REFERENCES `forum_system_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_system_db`.`votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`votes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `reply_id` INT NOT NULL,
  `users_id` INT NOT NULL,
  `type_vote` ENUM('up', 'down') NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_votes_replies1_idx` (`reply_id` ASC) VISIBLE,
  INDEX `fk_votes_users1_idx` (`users_id` ASC) VISIBLE,
  UNIQUE INDEX `users_id_UNIQUE` (`users_id` ASC, `reply_id` ASC) VISIBLE,
  CONSTRAINT `fk_votes_replies1`
    FOREIGN KEY (`reply_id`)
    REFERENCES `forum_system_db`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_votes_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `forum_system_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_system_db`.`categories_has_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_db`.`categories_has_users` (
  `categories_id` INT NOT NULL,
  `users_id` INT NOT NULL,
  `has_right_access` TINYINT NOT NULL,
  PRIMARY KEY (`categories_id`, `users_id`),
  INDEX `fk_categories_has_users_users1_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_categories_has_users_categories1_idx` (`categories_id` ASC) VISIBLE,
  CONSTRAINT `fk_categories_has_users_categories1`
    FOREIGN KEY (`categories_id`)
    REFERENCES `forum_system_db`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_categories_has_users_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `forum_system_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
