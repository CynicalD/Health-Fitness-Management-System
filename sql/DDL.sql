-- Drop tables if they already exist 
DROP TABLE IF EXISTS class_registration;
DROP TABLE IF EXISTS health_metric;
DROP TABLE IF EXISTS fitness_class;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS trainer;
DROP TABLE IF EXISTS member;

-- Member tabrle: stores gym members
CREATE TABLE member (
    member_id      SERIAL PRIMARY KEY,
    first_name     VARCHAR(50) NOT NULL,
    last_name      VARCHAR(50) NOT NULL,
    email          VARCHAR(255) NOT NULL UNIQUE,
    phone          VARCHAR(20),
    goal_description TEXT
);

-- Trainer table: stores trainers
CREATE TABLE trainer (
    trainer_id     SERIAL PRIMARY KEY,
    first_name     VARCHAR(50) NOT NULL,
    last_name      VARCHAR(50) NOT NULL,
    email          VARCHAR(255) NOT NULL UNIQUE,
    phone          VARCHAR(20),
    specialty      VARCHAR(100)
);

-- Room table: stores rooms where classes are held
CREATE TABLE room (
    room_id        SERIAL PRIMARY KEY,
    capacity       INTEGER NOT NULL CHECK (capacity > 0)
);

-- FitnessClass table: scheduled group classes
CREATE TABLE fitness_class (
    class_id       SERIAL PRIMARY KEY,
    class_name     VARCHAR(100) NOT NULL,
    trainer_id     INTEGER NOT NULL,
    room_id        INTEGER NOT NULL,
    start_time     TIMESTAMP NOT NULL,
    end_time       TIMESTAMP NOT NULL,
    capacity       INTEGER NOT NULL CHECK (capacity > 0),

    CONSTRAINT fk_fitness_class_trainer
        FOREIGN KEY (trainer_id) REFERENCES trainer(trainer_id),

    CONSTRAINT fk_fitness_class_room
        FOREIGN KEY (room_id) REFERENCES room(room_id)
);

-- ClassRegistration table: link between members and classes
CREATE TABLE class_registration (
    member_id      INTEGER NOT NULL,
    class_id       INTEGER NOT NULL,
    registered_at  TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_class_registration
        PRIMARY KEY (member_id, class_id),

    CONSTRAINT fk_class_registration_member
        FOREIGN KEY (member_id) REFERENCES member(member_id),

    CONSTRAINT fk_class_registration_class
        FOREIGN KEY (class_id) REFERENCES fitness_class(class_id)
);

-- HealthMetric table: recorded metrics for members
CREATE TABLE health_metric (
    metric_id          SERIAL PRIMARY KEY,
    member_id          INTEGER NOT NULL,
    recorded_at        TIMESTAMP NOT NULL DEFAULT NOW(),
    weight_kg          NUMERIC(5,2),
    resting_heart_rate INTEGER,

    CONSTRAINT fk_health_metric_member
        FOREIGN KEY (member_id) REFERENCES member(member_id)
);

-- =========================================
-- VIEW: class_overview
-- Shows each class with trainer, room, and current enrollment count
-- =========================================
CREATE OR REPLACE VIEW class_overview AS
SELECT
    fc.class_id,
    fc.class_name,
    fc.start_time,
    fc.end_time,
    fc.capacity,
    t.first_name AS trainer_first_name,
    t.last_name  AS trainer_last_name,
    r.room_id,
    r.capacity   AS room_capacity,
    COUNT(cr.member_id) AS enrolled_count
FROM fitness_class fc
JOIN trainer t ON fc.trainer_id = t.trainer_id
JOIN room r    ON fc.room_id = r.room_id
LEFT JOIN class_registration cr
    ON fc.class_id = cr.class_id
GROUP BY
    fc.class_id,
    fc.class_name,
    fc.start_time,
    fc.end_time,
    fc.capacity,
    t.first_name,
    t.last_name,
    r.room_id,
    r.capacity;

-- INDEX: idx_member_email
-- Speeds up lookups of members by email
CREATE INDEX IF NOT EXISTS idx_member_email
ON member (email);