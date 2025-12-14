CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'user', 'team_lead'))
);


CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    team_lead_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,

    CONSTRAINT fk_team_lead
        FOREIGN KEY (team_lead_id)
        REFERENCES users(id)
        ON DELETE SET NULL
);


CREATE TABLE team_members (
    id SERIAL PRIMARY KEY,
    team_id INT NOT NULL,
    user_id INT NOT NULL,

    CONSTRAINT fk_team
        FOREIGN KEY (team_id)
        REFERENCES teams(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    team_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL CHECK (status IN ('to_do', 'in_progress', 'review', 'done')),
    priority VARCHAR(20) NOT NULL CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    due_date DATE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_task_team
        FOREIGN KEY (team_id)
        REFERENCES teams(id)
        ON DELETE CASCADE
);