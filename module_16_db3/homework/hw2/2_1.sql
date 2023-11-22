SELECT c.full_name, m.full_name, o.date, o.purchase_amount FROM customer AS c
    JOIN manager m on c.manager_id = m.manager_id
    JOIN "order" o on c.customer_id = o.customer_id