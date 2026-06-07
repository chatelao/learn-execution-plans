CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    price DECIMAL
);

INSERT INTO products (name, category, price)
SELECT
    'product' || i,
    CASE WHEN i % 2 = 0 THEN 'electronics' ELSE 'books' END,
    (random() * 100)::decimal
FROM generate_series(1, 1000) i;

-- Ensure an index on id exists (redundant since it's a PRIMARY KEY, but good for clarity)
CREATE INDEX IF NOT EXISTS idx_products_id ON products(id);
ANALYZE products;
