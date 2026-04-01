-- phpMyAdmin SQL Dump
-- version 6.0.0-dev+20250718.d42db65a1e
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 31, 2026 at 04:02 AM
-- Server version: 8.4.3
-- PHP Version: 8.3.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `custly`
--

-- --------------------------------------------------------

--
-- Table structure for table `urls`
--

CREATE TABLE `urls` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `slug` varchar(50) DEFAULT NULL,
  `url` text,
  `password` varchar(255) DEFAULT NULL,
  `expires_at` datetime DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `urls`
--

INSERT INTO `urls` (`id`, `user_id`, `slug`, `url`, `password`, `expires_at`, `created_at`, `updated_at`) VALUES
(9, 1, 'myweb', 'https://yazidyusuf.my.id', 'scrypt:32768:8:1$tWz3aOFw0kG4hdQC$11c96bbf89ca478da901b85958b8a2d146937d04ef425beea08e60e82321c1d3c3838ce3c09e4dbc8d2fd037ad01b97cad18ebba7db3c5d9a5daf4add83a9ebb', NULL, '2026-03-19 13:49:15', '2026-03-19 20:50:29'),
(10, 1, 'ano', 'https://yazidyusuf.my.id', NULL, '2026-03-19 21:07:00', '2026-03-19 13:53:42', '2026-03-19 21:06:26');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `created_at`) VALUES
(1, 'Yazid Yusuf', 'ziids1933@gmail.com', 'scrypt:32768:8:1$weqWBlmqX1sT6IIc$a224a3ee27e44d5d882fd7bb68c5c05a37dc2beecb184378e47d63ea6026f9a511a8c9cbaa5e91e9bdc1517538d43e94dc91758ffa7cc94027a1fb33000b3b7e', '2026-03-19 12:32:40'),
(2, 'DrelezTM', 'dreleztm@gmail.com', 'scrypt:32768:8:1$4GQc4FHdQJA9DKaL$f84d393469db0be3cce8cfb943bcf0662dfc3e71f93327dfe37f9e0b97133fe86cf5b541c6eef0e060b9d93c499ec84b76292c8ccd15fe0adfad9e12ca002194', '2026-03-19 13:34:51'),
(3, 'Yusuf Yazid', 'yusuf@gmail.com', 'scrypt:32768:8:1$BjeFKTfTRpwbTAuQ$230cc7b272ee983743cc40eeea111f7a0d89b62d6c6319ba9ca534a1e5201570f21e60f6a778fbbd5f466c167d5b9e1658c46749175db62c3a2284dcbcfd7656', '2026-03-31 03:33:23');

-- --------------------------------------------------------

--
-- Table structure for table `visitors`
--

CREATE TABLE `visitors` (
  `id` int NOT NULL,
  `url_id` int NOT NULL,
  `ip` varchar(45) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `os` varchar(50) DEFAULT NULL,
  `browser` varchar(50) DEFAULT NULL,
  `referrer` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `visitors`
--

INSERT INTO `visitors` (`id`, `url_id`, `ip`, `country`, `os`, `browser`, `referrer`, `created_at`) VALUES
(13, 9, '127.0.0.1', 'Local', 'Windows', 'Chrome', 'http://127.0.0.1:5000/myweb', '2026-03-19 20:49:44'),
(14, 9, '127.0.0.1', 'Local', 'Windows', 'Chrome', 'http://127.0.0.1:5000/myweb', '2026-03-19 20:50:36'),
(15, 9, '127.0.0.1', 'Local', 'Windows', 'Chrome', 'http://127.0.0.1:5000/myweb', '2026-03-19 20:53:09'),
(16, 10, '127.0.0.1', 'Local', 'Windows', 'Chrome', 'http://127.0.0.1:5000/', '2026-03-19 20:53:44'),
(18, 10, '127.0.0.1', 'Local', 'Windows', 'Chrome', 'http://127.0.0.1:5000/', '2026-03-19 21:06:28');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `urls`
--
ALTER TABLE `urls`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `visitors`
--
ALTER TABLE `visitors`
  ADD PRIMARY KEY (`id`),
  ADD KEY `url_id` (`url_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `urls`
--
ALTER TABLE `urls`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `visitors`
--
ALTER TABLE `visitors`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `visitors`
--
ALTER TABLE `visitors`
  ADD CONSTRAINT `visitors_ibfk_1` FOREIGN KEY (`url_id`) REFERENCES `urls` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
