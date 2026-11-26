INSERT INTO products (product_id, product_cost) VALUES ('P101',100000), ('P102',50000) ON CONFLICT (product_id) DO NOTHING;

-- INSERT INTO products (product_id, product_cost) VALUES ('P101',100000), ('P102',50000) ON CONFLICT (product_id) DO UPDATE SET product_cost = EXCLUDED.product_cost;
