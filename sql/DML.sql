-- Samle data for gym_management

-- Clear existing data if exsit
DELETE FROM class_registration;
DELETE FROM health_metric;
DELETE FROM fitness_class;
DELETE FROM room;
DELETE FROM trainer;
DELETE FROM member;

-- Insert members
INSERT INTO member (first_name, last_name, email, phone, goal_description)
VALUES
    ('John',  'Doe',      'john.doe@example.com',   '555-1111', 'Lose 5kg and improve cardio'),
    ('George ', 'Washington',      'goerge.washington@revolution.com',  '555-2222', 'Build strength and muscle'),
    ('John A',  'Macdonald',    'johna.macdonald@independence.com', '555-3333', 'Train for marathon'),
    ('Abraham', 'Lincoln',     'abraham.lincoln@civilwar.com', '555-4444', 'General fitness'),
    ('Bob',   'Martin',   'bob.martin@example.com', '555-5555', 'Improve flexibility');

-- Insert trainers
INSERT INTO trainer (first_name, last_name, email, phone, specialty)
VALUES
    ('Laura',   'Smith',   'laura.smith@gym.com',   '555-6001', 'Strength Training'),
    ('David',   'Dude',  'david.wilson@gym.com',  '555-6002', 'Cardio & HIIT'),
    ('Sponge',   'Bob',   'sponge.bob@gym.com',   '555-6003', 'Yoga & Mobility');

-- insert rooms
INSERT INTO room (capacity)
VALUES
    (20),  -- room_id = 1
    (15),  -- room_id = 2
    (30);  -- room_id = 3

-- Insert fitness classes
-- Assume trainer_ids start at 1 and rooms at 1 based on inserts above
INSERT INTO fitness_class (class_name, trainer_id, room_id, start_time, end_time, capacity)
VALUES
    ('Morning Yoga',       3, 1, '2025-01-10 08:00', '2025-01-10 09:00', 15),
    ('Evening HIIT',       2, 2, '2025-01-10 18:00', '2025-01-10 19:00', 15),
    ('Lunchtime Strength', 1, 3, '2025-01-11 12:00', '2025-01-11 13:00', 20),
    ('Saturday Cardio',    2, 1, '2025-01-12 10:00', '2025-01-12 11:00', 20),
    ('Beginner Yoga',      3, 2, '2025-01-13 09:00', '2025-01-13 10:00', 10);

-- Insert class registrations
-- member_ids will be 1..5 in order of insertion above
-- class_ids will be 1..5 in order of insertion above
INSERT INTO class_registration (member_id, class_id, registered_at)
VALUES
    (1, 1, '2025-01-05 10:00'),
    (2, 1, '2025-01-05 10:05'),
    (3, 2, '2025-01-06 09:00'),
    (4, 3, '2025-01-07 14:30'),
    (5, 4, '2025-01-08 16:00'),
    (1, 2, '2025-01-06 09:15'),
    (2, 3, '2025-01-07 15:00'),
    (3, 5, '2025-01-09 11:00');

-- Insert health metrics
INSERT INTO health_metric (member_id, recorded_at, weight_kg, resting_heart_rate)
VALUES
    (1, '2025-01-01 09:00', 82.5, 72),
    (1, '2025-01-08 09:00', 81.8, 70),
    (2, '2025-01-02 10:00', 65.0, 68),
    (3, '2025-01-03 11:00', 90.2, 78),
    (4, '2025-01-04 12:00', 70.5, 65),
    (5, '2025-01-05 13:00', 75.3, 74);