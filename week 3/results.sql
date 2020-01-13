use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product

-- 2. Выбрать названия всех автоматизированных складов
SELECT name FROM store WHERE is_automated=1;

-- 3. Посчитать общую сумму в деньгах всех продаж
SELECT SUM(total) FROM sale;

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
SELECT DISTINCT(store_id) from sale;

-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
select s.store_id from store as s left join sale as p on s.store_id = p.store_id where p.store_id is null;

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
select product_id, avg(total/quantity) from sale group by product_id;

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select p.name from sale s inner join product p on p.product_id = s.product_id group by s.product_id having count(distinct s.store_id) = 1;

-- 8. Получить названия всех складов, с которых продавался только один продукт
select store.name from sale s inner join store on store.store_id = s.store_id group by s.store_id having count(distinct s.product_id) = 1;

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * from sale where total=(select MAX(total) FROM sale);

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select date from sale group by date order by sum(total) desc, date limit 1;
