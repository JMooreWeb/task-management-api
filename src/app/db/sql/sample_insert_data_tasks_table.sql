INSERT INTO public.tasks
(
    user_id,
    title,
    description,
    status,
    priority,
    due_at,
    started_at,
    completed_at,
    created_at,
    updated_at
)
VALUES

-- Tasks for admin
(
    (SELECT id FROM users WHERE username = 'admin'),
    'System configuration review',
    'Review system configuration and security settings',
    'in_progress',
    3,
    CURRENT_TIMESTAMP + INTERVAL '2 days',
    CURRENT_TIMESTAMP,
    NULL,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
),

-- Manager tasks
(
    (SELECT id FROM users WHERE username = 'manager'),
    'Review team workload',
    'Check assigned tasks and balance workload among team members',
    'pending',
    2,
    CURRENT_TIMESTAMP + INTERVAL '3 days',
    NULL,
    NULL,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
),

-- James Moore task
(
    (SELECT id FROM users WHERE username = 'jmoore'),
    'Verify property ownership records',
    'Cross-check parcel data and ownership documents in the system',
    'in_progress',
    2,
    CURRENT_TIMESTAMP + INTERVAL '5 days',
    CURRENT_TIMESTAMP,
    NULL,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
),

-- Sarah task
(
    (SELECT id FROM users WHERE username = 'sjohnson'),
    'Update property photos',
    'Upload latest property images and verify metadata',
    'pending',
    1,
    CURRENT_TIMESTAMP + INTERVAL '4 days',
    NULL,
    NULL,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
),

-- Michael task (completed)
(
    (SELECT id FROM users WHERE username = 'msmith'),
    'Database cleanup',
    'Remove duplicate parcel entries and normalize addresses',
    'completed',
    3,
    CURRENT_TIMESTAMP - INTERVAL '1 day',
    CURRENT_TIMESTAMP - INTERVAL '3 days',
    CURRENT_TIMESTAMP - INTERVAL '1 day',
    CURRENT_TIMESTAMP - INTERVAL '3 days',
    CURRENT_TIMESTAMP - INTERVAL '1 day'
),

-- Viewer task (read-only type)
(
    (SELECT id FROM users WHERE username = 'viewer1'),
    'Generate property report',
    'Compile property tax report for last quarter',
    'pending',
    1,
    CURRENT_TIMESTAMP + INTERVAL '7 days',
    NULL,
    NULL,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
),

-- Auditor task
(
    (SELECT id FROM users WHERE username = 'auditor1'),
    'Audit user activity logs',
    'Review authentication logs and system access records',
    'in_progress',
    2,
    CURRENT_TIMESTAMP + INTERVAL '6 days',
    CURRENT_TIMESTAMP,
    NULL,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
