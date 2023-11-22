SELECT c.full_name FROM customer as c
    WHERE NOT EXISTS(
        SELECT 1 FROM "order" as o
            WHERE o.customer_id == c.customer_id
        )