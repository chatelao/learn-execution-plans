CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    supplier_id INTEGER REFERENCES suppliers(id),
    price DECIMAL
);

-- Insert enough data to encourage Hash Join
INSERT INTO suppliers (name, city)
SELECT 'Supplier ' || i, 'City ' || (i % 10)
FROM generate_series(1, 100) s(i);

INSERT INTO products (name, supplier_id, price)
SELECT 'Product ' || i, (i % 100) + 1, (i * 1.5)
FROM generate_series(1, 1000) s(i);

ANALYZE suppliers;
ANALYZE products;
