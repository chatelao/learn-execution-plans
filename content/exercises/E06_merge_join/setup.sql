CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total_amount DECIMAL
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER,
    quantity INTEGER,
    price DECIMAL
);

-- Indices on join keys favor Merge Join if sorted
CREATE INDEX idx_orders_id ON orders(id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);

-- Insert data
INSERT INTO orders (customer_id, order_date, total_amount)
SELECT (i % 50) + 1, CURRENT_DATE - (i % 100), i * 10.0
FROM generate_series(1, 200) s(i);

INSERT INTO order_items (order_id, product_id, quantity, price)
SELECT (i % 200) + 1, (i % 30) + 1, (i % 5) + 1, (i * 2.5)
FROM generate_series(1, 1000) s(i);

-- Ensure data is gathered
ANALYZE orders;
ANALYZE order_items;
