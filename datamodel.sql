-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema myDb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema myDb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `myDb` DEFAULT CHARACTER SET utf8 ;
USE `myDb` ;

-- -----------------------------------------------------
-- Table `myDb`.`Quiz`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myDb`.`Quiz` (
  `idQuiz` INT NOT NULL,
  `Navn` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idQuiz`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `myDb`.`Admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myDb`.`Admin` (
  `idAdmin` VARCHAR(45) NOT NULL,
  `Fornavn` VARCHAR(45) NULL,
  `Etternavn` VARCHAR(45) NULL,
  PRIMARY KEY (`idAdmin`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `myDb`.`Bruker`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myDb`.`Bruker` (
  `idBruker` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idBruker`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `myDb`.`Tema`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myDb`.`Tema` (
  `idTema` INT NOT NULL,
  `Navn` VARCHAR(45) NULL,
  PRIMARY KEY (`idTema`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `myDb`.`Sporsmal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myDb`.`Sporsmal` (
  `Quiz_idQuiz` INT NOT NULL,
  `idSporsmal` INT NOT NULL,
  `Tekst` MEDIUMTEXT NULL,
  `Tema_idTema` INT NOT NULL,
  PRIMARY KEY (`Quiz_idQuiz`, `idSporsmal`),
  INDEX `fk_Sporsmal_Tema1_idx` (`Tema_idTema` ASC) VISIBLE,
  INDEX `fk_Sporsmal_Quiz1_idx` (`Quiz_idQuiz` ASC) VISIBLE,
  CONSTRAINT `fk_Sporsmal_Tema1`
    FOREIGN KEY (`Tema_idTema`)
    REFERENCES `myDb`.`Tema` (`idTema`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Sporsmal_Quiz1`
    FOREIGN KEY (`Quiz_idQuiz`)
    REFERENCES `myDb`.`Quiz` (`idQuiz`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `myDb`.`Svar`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myDb`.`Svar` (
  `Sporsmal_Quiz_idQuiz` INT NOT NULL,
  `Sporsmal_idSporsmal` INT NOT NULL,
  `idSvar` INT NOT NULL,
  `Tekst` MEDIUMTEXT NULL,
  `isRiktig` TINYINT NULL,
  PRIMARY KEY (`Sporsmal_Quiz_idQuiz`, `Sporsmal_idSporsmal`, `idSvar`),
  INDEX `fk_Svar_Sporsmal1_idx` (`Sporsmal_Quiz_idQuiz` ASC, `Sporsmal_idSporsmal` ASC) VISIBLE,
  CONSTRAINT `fk_Svar_Sporsmal1`
    FOREIGN KEY (`Sporsmal_Quiz_idQuiz` , `Sporsmal_idSporsmal`)
    REFERENCES `myDb`.`Sporsmal` (`Quiz_idQuiz` , `idSporsmal`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `myDb`.`Bruker_has_Svar`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myDb`.`Bruker_has_Svar` (
  `Bruker_idBruker` VARCHAR(45) NOT NULL,
  `Svar_Sporsmal_Quiz_idQuiz` INT NOT NULL,
  `Svar_Sporsmal_idSporsmal` INT NOT NULL,
  `Svar_idSvar` INT NOT NULL,
  PRIMARY KEY (`Bruker_idBruker`, `Svar_Sporsmal_Quiz_idQuiz`, `Svar_Sporsmal_idSporsmal`, `Svar_idSvar`),
  INDEX `fk_Bruker_has_Svar1_Svar1_idx` (`Svar_Sporsmal_Quiz_idQuiz` ASC, `Svar_Sporsmal_idSporsmal` ASC, `Svar_idSvar` ASC) VISIBLE,
  INDEX `fk_Bruker_has_Svar1_Bruker1_idx` (`Bruker_idBruker` ASC) VISIBLE,
  CONSTRAINT `fk_Bruker_has_Svar1_Bruker1`
    FOREIGN KEY (`Bruker_idBruker`)
    REFERENCES `myDb`.`Bruker` (`idBruker`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Bruker_has_Svar1_Svar1`
    FOREIGN KEY (`Svar_Sporsmal_Quiz_idQuiz` , `Svar_Sporsmal_idSporsmal` , `Svar_idSvar`)
    REFERENCES `myDb`.`Svar` (`Sporsmal_Quiz_idQuiz` , `Sporsmal_idSporsmal` , `idSvar`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `myDb`.`Sporsmal_has_Admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myDb`.`Sporsmal_has_Admin` (
  `Sporsmal_Quiz_idQuiz` INT NOT NULL,
  `Sporsmal_idSporsmal` INT NOT NULL,
  `Admin_idAdmin` VARCHAR(45) NOT NULL,
  `Endringstid` DATETIME NULL,
  PRIMARY KEY (`Sporsmal_Quiz_idQuiz`, `Sporsmal_idSporsmal`, `Admin_idAdmin`),
  INDEX `fk_Sporsmal_has_Admin_Admin1_idx` (`Admin_idAdmin` ASC) VISIBLE,
  INDEX `fk_Sporsmal_has_Admin_Sporsmal1_idx` (`Sporsmal_Quiz_idQuiz` ASC, `Sporsmal_idSporsmal` ASC) VISIBLE,
  CONSTRAINT `fk_Sporsmal_has_Admin_Sporsmal1`
    FOREIGN KEY (`Sporsmal_Quiz_idQuiz` , `Sporsmal_idSporsmal`)
    REFERENCES `myDb`.`Sporsmal` (`Quiz_idQuiz` , `idSporsmal`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Sporsmal_has_Admin_Admin1`
    FOREIGN KEY (`Admin_idAdmin`)
    REFERENCES `myDb`.`Admin` (`idAdmin`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
