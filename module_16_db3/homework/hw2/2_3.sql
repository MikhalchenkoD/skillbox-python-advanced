SELECT c.full_name, m.full_name, o.order_no FROM customer as c
    JOIN "order" o on c.customer_id = o.customer_id
    JOIN manager m on m.manager_id = c.manager_id
    WHERE c.city != m.city