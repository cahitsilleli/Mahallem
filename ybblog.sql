-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 28 May 2022, 22:05:34
-- Sunucu sürümü: 10.4.24-MariaDB
-- PHP Sürümü: 7.4.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `ybblog`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `booking`
--

CREATE TABLE `booking` (
  `id` int(11) NOT NULL,
  `owner_id` text NOT NULL,
  `username` text NOT NULL,
  `year` text NOT NULL,
  `month` text NOT NULL,
  `day` text NOT NULL,
  `problem` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Tablo döküm verisi `booking`
--

INSERT INTO `booking` (`id`, `owner_id`, `username`, `year`, `month`, `day`, `problem`) VALUES
(13, '11', 'ali_ayşe', '2022', 'Mayıs', '7', 'elektrik yok');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `masters`
--

CREATE TABLE `masters` (
  `id` int(11) NOT NULL,
  `type` text CHARACTER SET utf8mb4 NOT NULL,
  `store` text CHARACTER SET utf8mb4 NOT NULL,
  `phone_number` text CHARACTER SET utf8mb4 NOT NULL,
  `city` text CHARACTER SET utf8mb4 NOT NULL,
  `district` text CHARACTER SET utf8mb4 NOT NULL,
  `street` text CHARACTER SET utf8mb4 NOT NULL,
  `address` text CHARACTER SET utf8mb4 NOT NULL,
  `name` text CHARACTER SET utf8mb4 NOT NULL,
  `surname` text CHARACTER SET utf8mb4 NOT NULL,
  `username` text CHARACTER SET utf8mb4 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `masters`
--

INSERT INTO `masters` (`id`, `type`, `store`, `phone_number`, `city`, `district`, `street`, `address`, `name`, `surname`, `username`) VALUES
(11, 'Tesisatçı', 'Kardeşler Tesisat', '05066695444', 'Aydın', 'Nazilli', 'kurtuluş', 'kurtuluş mahallesi 2020 sokak numara 10/c', 'Cahit', 'Silleli', 'cahit_silleli'),
(14, 'Boyacı', 'Samatya Boyacısı', '05542345432', 'Aydın', 'Koçarlı', 'Sardunya', 'Sardunya Mahallesi 321.Sokak numara 10/c', 'Mustafa Cem', 'Buğu', 'cem_bugu'),
(15, 'Elektrikçi', 'Farketmez Elektronik', '05067942564', 'Aydın', 'Köşk', 'Çarpışma', 'Çarpışma Mahallesi 154.Sokak Numara 190/c', 'Soner', 'Aktaş', 'sonerkts'),
(16, 'Tamirci', 'Kemal Paşa Tamirhanesi', '05562343464', 'Aydın', 'Kuşadası', 'Atatürk', 'Atatürk Mahallesi 1253.Sokak No:123/c', 'Cafer', 'Karabulut', 'cafer_karabulut'),
(17, 'Tamirci', 'Kurtuluş Tamirhanesi', '05585782852', 'Aydın', 'Çine', 'Kocabaş', 'Kocabaş Mahallesi 1923.Sokak Numara 226/c', 'Öznur', 'Elbaş', 'oznur_elbas'),
(18, 'Boyacı', 'Erbaş Boya', '05594582765', 'Aydın', 'Köşk', 'Kuzguncuk', 'Kuzguncuk Mahallesi 194.Sokak No:27/c', 'Mustafa Oğuz', 'Erbaş', 'oguz_erbas');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `surname` text NOT NULL,
  `email` text NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL,
  `phone_number` text NOT NULL,
  `city` text NOT NULL,
  `district` text NOT NULL,
  `street` text NOT NULL,
  `address` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Tablo döküm verisi `users`
--

INSERT INTO `users` (`id`, `name`, `surname`, `email`, `username`, `password`, `phone_number`, `city`, `district`, `street`, `address`) VALUES
(10, 'Cahit', 'Silleli', 'cahitsilleli@gmail.com', 'cahit_silleli', '$5$rounds=535000$g6.b/cgu1/B3I6yN$DcNA/2M2lc3rSP6OaGQl4BWsk0jGQusdoOEqDLujlJ.', '05066695444', 'Aydın', 'Didim', 'Altınkum', 'Altınkum mahallesi 2020 sokak numara 10 daire 2'),
(11, 'Selin', 'Süleler', 'selin_süleler@gmail.com', 'selin_sllr', '$5$rounds=535000$6ktJ9Ih1ja74/jS1$PDwD/igg8k3RyNgBcCYwzAJXitFN5h7zNXg1F751u/9', '05545687740', 'Aydın', 'İncirliova', 'Yaprak', 'Yaprak mahallesi 1020 sokak numara 10 daire 5'),
(12, 'Mustafa Cem', 'Buğu', 'mustafacembugu@gmail.com', 'cem_bugu', '$5$rounds=535000$eIuMprNziyt5Y4E4$Qk/btvf0d3eRJqCHl1j3QxvG5hoAFUQgvqrK182v953', '05066523245', 'Aydın', 'Koçarlı', 'Telli', 'Telli mahallesi 123. Sokak Numara 4 Daire 2'),
(13, 'Soner', 'Aktaş', 'soneraktas@gmail.com', 'sonerkts', '$5$rounds=535000$593HyvYho9OAx/gG$6kJ2ftSnSfrYSW0B2GOIcI3SAasehZEeAKVjzmH0iK3', '05068438233', 'Aydın', 'Bozdoğan', 'karabacak', 'Karabacak Mahallesi 564. Sokak Numara 10 Daire 7'),
(14, 'Cafer', 'Karabulut', 'caferkarabulut@gmail.com', 'cafer_karabulut', '$5$rounds=535000$zxaWVjq9eiN4UbIQ$KKCc4fDCUx7m55/JHtV9ObunvgnVg0AdSdTlGjc5SJC', '05562343464', 'Aydın', 'Kuşadası', 'Atatürk', 'Atatürk Mahallesi 1881.sokak  no:188 daire:1'),
(15, 'Öznur', 'Elbaş', 'oznurelbas@gmail.com', 'oznur_elbas', '$5$rounds=535000$Z0/Ldpz2jrrh8pvc$A4B8EuN2okGT8nrNQCA8.ZCOCtxPaoAcW64x5HmE.m5', '05585782852', 'Aydın', 'Çine', 'Karabaş', 'Karabaş Mahallesi 1927.Sokak No:25 Daire:22'),
(16, 'Mustafa Oğuz', 'Erbaş', 'mustafaoguzerbas@gmail.com', 'oguz_erbas', '$5$rounds=535000$Jzq4adFr1/NTvB8v$X41GO0/wbR3zrgV1J5kzHYaYr6FPduCc7HO6EX6n6c0', '05594582765', 'Aydın', 'Karacasu', 'Yalın', 'Yalın Mahallesi 189.Sokak No:19 Daire:10'),
(17, 'alisss', 'ayşe', 'ali_ayşe@gmail.com', 'ali_ayşe', '$5$rounds=535000$RNDGTvRzOMqqKykl$bHr17rtqDC448iMh9KWSb1lQHocBOEFlMw8Mf22FRs7', '123125125125', 'Aydın', 'Çine', 'kahraman', 'asdasfasdasf');

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `masters`
--
ALTER TABLE `masters`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `booking`
--
ALTER TABLE `booking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Tablo için AUTO_INCREMENT değeri `masters`
--
ALTER TABLE `masters`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- Tablo için AUTO_INCREMENT değeri `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
