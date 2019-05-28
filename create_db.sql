-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema pet_adoption
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema pet_adoption
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pet_adoption` DEFAULT CHARACTER SET utf8 ;
USE `pet_adoption` ;

-- -----------------------------------------------------
-- Table `pet_adoption`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pet_adoption`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(256) NULL,
  `last_name` VARCHAR(256) NULL,
  `email` VARCHAR(256) NULL,
  `password` VARCHAR(256) NULL,
  `user_level` INT NULL DEFAULT 0,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pet_adoption`.`animals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pet_adoption`.`animals` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(256) NULL,
  `type` VARCHAR(256) NULL,
  `breed` VARCHAR(256) NULL,
  `color` VARCHAR(45) NULL,
  `file_name` VARCHAR(256) NULL,
  `file_location` VARCHAR(256) NULL,
  `location` VARCHAR(256) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_animals_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_animals_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `pet_adoption`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pet_adoption`.`appointments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pet_adoption`.`appointments` (
  `animal_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `date` DATETIME NULL,
  PRIMARY KEY (`animal_id`, `user_id`),
  INDEX `fk_animals_has_users_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_animals_has_users_animals1_idx` (`animal_id` ASC) VISIBLE,
  CONSTRAINT `fk_animals_has_users_animals1`
    FOREIGN KEY (`animal_id`)
    REFERENCES `pet_adoption`.`animals` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_animals_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `pet_adoption`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
