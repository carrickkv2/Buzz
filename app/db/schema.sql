CREATE TABLE machines (
    id SERIAL NOT NULL,
    name VARCHAR NOT NULL,
    nominal_power INTEGER NOT NULL,
    type VARCHAR NOT NULL,
    description VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (id)
)