CREATE TABLE IF NOT EXISTS public.users
(
    -- 🔑 Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 🔐 Authentication
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,

    -- 👤 Profile Info
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(25),

    -- 🧾 Account Status
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,

    -- 🔐 Security Tracking
    last_login TIMESTAMP,
    last_password_change TIMESTAMP,
    failed_login_attempts INTEGER DEFAULT 0,
    account_locked_until TIMESTAMP,

    -- 🕒 Audit Fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 🗑️ Soft Delete
    deleted_at TIMESTAMP,

    -- 🔎 Optional metadata
    notes TEXT
);

CREATE TABLE IF NOT EXISTS public.roles
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200),
    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.user_roles
(
    user_id UUID NOT NULL,
    role_id UUID NOT NULL,

    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Prevent duplicates (same user + same role)
    CONSTRAINT user_roles_pkey PRIMARY KEY (user_id, role_id),

    CONSTRAINT user_roles_user_id_fkey
        FOREIGN KEY (user_id)
        REFERENCES public.users (id)
        ON DELETE CASCADE,

    CONSTRAINT user_roles_role_id_fkey
        FOREIGN KEY (role_id)
        REFERENCES public.roles (id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_user_roles_user_id ON public.user_roles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_roles_role_id ON public.user_roles(role_id);

-- Create new role
INSERT INTO public.roles (name, description) VALUES 
	('admin','Full access'), 
	('user','Standard access');

-- Assign a user to a role
INSERT INTO public.user_roles (user_id, role_id) VALUES 
	('<user-uuid>', '<role-uuid>');


CREATE TABLE IF NOT EXISTS public.tasks
(
    -- 🔑 Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 🔗 Owner of the task
    user_id UUID NOT NULL,

    -- 🧾 Task Details
    title VARCHAR(200) NOT NULL,
    description TEXT,

    -- ⚙️ Task State
    status VARCHAR(50) DEFAULT 'pending',   -- pending, in_progress, completed, cancelled
    priority INTEGER DEFAULT 0,             -- 0=low, 1=medium, 2=high, 3=urgent

    -- 📅 Scheduling
    due_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,

    -- 🕒 Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,

    -- 🔗 Foreign Key
    CONSTRAINT tasks_user_id_fkey
        FOREIGN KEY (user_id)
        REFERENCES public.users (id)
        ON DELETE CASCADE
);



CREATE TYPE task_status AS ENUM ('pending','in_progress','completed','cancelled');


CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_at ON tasks(due_at);

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_set_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

