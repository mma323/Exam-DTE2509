-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: 16. Apr, 2023 19:58 PM
-- Tjener-versjon: 10.11.2-MariaDB-1:10.11.2+maria~ubu2204
-- PHP Version: 8.1.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `myDb`
--
CREATE DATABASE IF NOT EXISTS `myDb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `myDb`;

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Admin`
--

CREATE TABLE `Admin` (
  `idAdmin` varchar(45) NOT NULL,
  `Fornavn` varchar(45) DEFAULT NULL,
  `Etternavn` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `Admin`
--

INSERT INTO `Admin` (`idAdmin`, `Fornavn`, `Etternavn`) VALUES
('admin_1', 'Navn', 'Navnesen'),
('admin_3', 'hei', 'heiesen');

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Bruker`
--

CREATE TABLE `Bruker` (
  `idBruker` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `Bruker`
--

INSERT INTO `Bruker` (`idBruker`) VALUES
('bruker_1');

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Bruker_has_Svar`
--

CREATE TABLE `Bruker_has_Svar` (
  `Bruker_idBruker` varchar(45) NOT NULL,
  `Svar_Sporsmal_Quiz_idQuiz` int(11) NOT NULL,
  `Svar_Sporsmal_idSporsmal` int(11) NOT NULL,
  `Svar_idSvar` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `Bruker_has_Svar`
--

INSERT INTO `Bruker_has_Svar` (`Bruker_idBruker`, `Svar_Sporsmal_Quiz_idQuiz`, `Svar_Sporsmal_idSporsmal`, `Svar_idSvar`) VALUES
('bruker_1', 12, 4, 4);

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Quiz`
--

CREATE TABLE `Quiz` (
  `idQuiz` int(11) NOT NULL,
  `Navn` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `Quiz`
--

INSERT INTO `Quiz` (`idQuiz`, `Navn`) VALUES
(12, 'NyQuiz');

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Sporsmal`
--

CREATE TABLE `Sporsmal` (
  `Quiz_idQuiz` int(11) NOT NULL,
  `idSporsmal` int(11) NOT NULL,
  `Tekst` mediumtext DEFAULT NULL,
  `Tema_idTema` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `Sporsmal`
--

INSERT INTO `Sporsmal` (`Quiz_idQuiz`, `idSporsmal`, `Tekst`, `Tema_idTema`) VALUES
(12, 4, 'hva er kvadratroten av 16', 1);

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Sporsmal_has_Admin`
--

CREATE TABLE `Sporsmal_has_Admin` (
  `Sporsmal_Quiz_idQuiz` int(11) NOT NULL,
  `Sporsmal_idSporsmal` int(11) NOT NULL,
  `Admin_idAdmin` varchar(45) NOT NULL,
  `Endringstid` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Svar`
--

CREATE TABLE `Svar` (
  `Sporsmal_Quiz_idQuiz` int(11) NOT NULL,
  `Sporsmal_idSporsmal` int(11) NOT NULL,
  `idSvar` int(11) NOT NULL,
  `Tekst` mediumtext DEFAULT NULL,
  `isRiktig` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `Svar`
--

INSERT INTO `Svar` (`Sporsmal_Quiz_idQuiz`, `Sporsmal_idSporsmal`, `idSvar`, `Tekst`, `isRiktig`) VALUES
(12, 4, 1, '1', 1),
(12, 4, 2, '2', 0),
(12, 4, 3, '3', 0),
(12, 4, 4, '4', 0);

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Tema`
--

CREATE TABLE `Tema` (
  `idTema` int(11) NOT NULL,
  `Navn` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `Tema`
--

INSERT INTO `Tema` (`idTema`, `Navn`) VALUES
(1, 'Sport'),
(2, 'Historie'),
(3, 'Matematikk');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Admin`
--
ALTER TABLE `Admin`
  ADD PRIMARY KEY (`idAdmin`);

--
-- Indexes for table `Bruker`
--
ALTER TABLE `Bruker`
  ADD PRIMARY KEY (`idBruker`);

--
-- Indexes for table `Bruker_has_Svar`
--
ALTER TABLE `Bruker_has_Svar`
  ADD PRIMARY KEY (`Bruker_idBruker`,`Svar_Sporsmal_Quiz_idQuiz`,`Svar_Sporsmal_idSporsmal`,`Svar_idSvar`),
  ADD KEY `fk_Bruker_has_Svar1_Svar1_idx` (`Svar_Sporsmal_Quiz_idQuiz`,`Svar_Sporsmal_idSporsmal`,`Svar_idSvar`),
  ADD KEY `fk_Bruker_has_Svar1_Bruker1_idx` (`Bruker_idBruker`);

--
-- Indexes for table `Quiz`
--
ALTER TABLE `Quiz`
  ADD PRIMARY KEY (`idQuiz`);

--
-- Indexes for table `Sporsmal`
--
ALTER TABLE `Sporsmal`
  ADD PRIMARY KEY (`Quiz_idQuiz`,`idSporsmal`),
  ADD KEY `fk_Sporsmal_Tema1_idx` (`Tema_idTema`),
  ADD KEY `fk_Sporsmal_Quiz1_idx` (`Quiz_idQuiz`);

--
-- Indexes for table `Sporsmal_has_Admin`
--
ALTER TABLE `Sporsmal_has_Admin`
  ADD PRIMARY KEY (`Sporsmal_Quiz_idQuiz`,`Sporsmal_idSporsmal`,`Admin_idAdmin`),
  ADD KEY `fk_Sporsmal_has_Admin_Admin1_idx` (`Admin_idAdmin`),
  ADD KEY `fk_Sporsmal_has_Admin_Sporsmal1_idx` (`Sporsmal_Quiz_idQuiz`,`Sporsmal_idSporsmal`);

--
-- Indexes for table `Svar`
--
ALTER TABLE `Svar`
  ADD PRIMARY KEY (`Sporsmal_Quiz_idQuiz`,`Sporsmal_idSporsmal`,`idSvar`),
  ADD KEY `fk_Svar_Sporsmal1_idx` (`Sporsmal_Quiz_idQuiz`,`Sporsmal_idSporsmal`);

--
-- Indexes for table `Tema`
--
ALTER TABLE `Tema`
  ADD PRIMARY KEY (`idTema`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Quiz`
--
ALTER TABLE `Quiz`
  MODIFY `idQuiz` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Begrensninger for dumpede tabeller
--

--
-- Begrensninger for tabell `Bruker_has_Svar`
--
ALTER TABLE `Bruker_has_Svar`
  ADD CONSTRAINT `fk_Bruker_has_Svar1_Bruker1` FOREIGN KEY (`Bruker_idBruker`) REFERENCES `Bruker` (`idBruker`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_Bruker_has_Svar1_Svar1` FOREIGN KEY (`Svar_Sporsmal_Quiz_idQuiz`,`Svar_Sporsmal_idSporsmal`,`Svar_idSvar`) REFERENCES `Svar` (`Sporsmal_Quiz_idQuiz`, `Sporsmal_idSporsmal`, `idSvar`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Begrensninger for tabell `Sporsmal`
--
ALTER TABLE `Sporsmal`
  ADD CONSTRAINT `fk_Sporsmal_Quiz1` FOREIGN KEY (`Quiz_idQuiz`) REFERENCES `Quiz` (`idQuiz`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_Sporsmal_Tema1` FOREIGN KEY (`Tema_idTema`) REFERENCES `Tema` (`idTema`) ON UPDATE CASCADE;

--
-- Begrensninger for tabell `Sporsmal_has_Admin`
--
ALTER TABLE `Sporsmal_has_Admin`
  ADD CONSTRAINT `fk_Sporsmal_has_Admin_Admin1` FOREIGN KEY (`Admin_idAdmin`) REFERENCES `Admin` (`idAdmin`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_Sporsmal_has_Admin_Sporsmal1` FOREIGN KEY (`Sporsmal_Quiz_idQuiz`,`Sporsmal_idSporsmal`) REFERENCES `Sporsmal` (`Quiz_idQuiz`, `idSporsmal`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Begrensninger for tabell `Svar`
--
ALTER TABLE `Svar`
  ADD CONSTRAINT `fk_Svar_Sporsmal1` FOREIGN KEY (`Sporsmal_Quiz_idQuiz`,`Sporsmal_idSporsmal`) REFERENCES `Sporsmal` (`Quiz_idQuiz`, `idSporsmal`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;