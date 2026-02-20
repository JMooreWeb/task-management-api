INSERT INTO public.roles (name, description)
VALUES
('admin', 'Full system access and administrative privileges'),
('manager', 'Manage users, tasks, and operations'),
('user', 'Standard application user'),
('viewer', 'Read-only access to data and reports'),
('auditor', 'Can review logs, history, and audit records')
ON CONFLICT (name) DO NOTHING;