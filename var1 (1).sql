create database var1;

--
-- Структура таблицы `materials`
--

CREATE TABLE `materials` (
  `material_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `unit` varchar(20) NOT NULL,
  `stock_quantity` decimal(10,2) NOT NULL DEFAULT '0.00',
  `type_id` int NOT NULL,
  `price_per_unit` decimal(10,2) DEFAULT '0.00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `materials`
--

INSERT INTO `materials` (`material_id`, `name`, `unit`, `stock_quantity`, `type_id`, `price_per_unit`) VALUES
(1, 'Материальный', 'шт', '10.00', 1, '0.00'),
(2, 'Стир', 'м', '2.00', 1, '0.00'),
(3, 'коль', 'метры', '10.00', 1, '20.00');

-- --------------------------------------------------------

--
-- Структура таблицы `material_suppliers`
--

CREATE TABLE `material_suppliers` (
  `material_id` int NOT NULL,
  `supplier_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `material_suppliers`
--

INSERT INTO `material_suppliers` (`material_id`, `supplier_id`) VALUES
(1, 1),
(2, 1),
(3, 1),
(1, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `material_types`
--

CREATE TABLE `material_types` (
  `type_id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `defect_percentage` double NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `material_types`
--

INSERT INTO `material_types` (`type_id`, `name`, `defect_percentage`) VALUES
(1, 'Ледяной', 0);

-- --------------------------------------------------------

--
-- Структура таблицы `products`
--

CREATE TABLE `products` (
  `product_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text,
  `coefficient` double NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `products`
--

INSERT INTO `products` (`product_id`, `name`, `description`, `coefficient`) VALUES
(1, 'Мат', 'Расписан\r\n', 1);

-- --------------------------------------------------------

--
-- Структура таблицы `product_materials`
--

CREATE TABLE `product_materials` (
  `product_id` int NOT NULL,
  `material_id` int NOT NULL,
  `quantity` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `product_materials`
--

INSERT INTO `product_materials` (`product_id`, `material_id`, `quantity`) VALUES
(1, 1, '5.00');

-- --------------------------------------------------------

--
-- Структура таблицы `suppliers`
--

CREATE TABLE `suppliers` (
  `supplier_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `contact_info` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `suppliers`
--

INSERT INTO `suppliers` (`supplier_id`, `name`, `contact_info`) VALUES
(1, 'Батов', '89166196292'),
(2, 'Полина', '89123123891\r\n');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `materials`
--
ALTER TABLE `materials`
  ADD PRIMARY KEY (`material_id`),
  ADD KEY `type_id` (`type_id`);

--
-- Индексы таблицы `material_suppliers`
--
ALTER TABLE `material_suppliers`
  ADD PRIMARY KEY (`material_id`,`supplier_id`),
  ADD KEY `supplier_id` (`supplier_id`);

--
-- Индексы таблицы `material_types`
--
ALTER TABLE `material_types`
  ADD PRIMARY KEY (`type_id`);

--
-- Индексы таблицы `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- Индексы таблицы `product_materials`
--
ALTER TABLE `product_materials`
  ADD PRIMARY KEY (`product_id`,`material_id`),
  ADD KEY `material_id` (`material_id`);

--
-- Индексы таблицы `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`supplier_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `materials`
--
ALTER TABLE `materials`
  MODIFY `material_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `material_types`
--
ALTER TABLE `material_types`
  MODIFY `type_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `supplier_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `materials`
--
ALTER TABLE `materials`
  ADD CONSTRAINT `materials_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `material_types` (`type_id`);

--
-- Ограничения внешнего ключа таблицы `material_suppliers`
--
ALTER TABLE `material_suppliers`
  ADD CONSTRAINT `material_suppliers_ibfk_1` FOREIGN KEY (`material_id`) REFERENCES `materials` (`material_id`),
  ADD CONSTRAINT `material_suppliers_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`supplier_id`);

--
-- Ограничения внешнего ключа таблицы `product_materials`
--
ALTER TABLE `product_materials`
  ADD CONSTRAINT `product_materials_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`),
  ADD CONSTRAINT `product_materials_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `materials` (`material_id`);
COMMIT;