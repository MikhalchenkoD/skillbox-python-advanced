SELECT c.full_name, o.order_no FROM customer as c
    JOIN "order" o on c.customer_id = o.customer_id
    WHERE c.manager_id IS NULL