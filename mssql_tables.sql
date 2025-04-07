-- Users table
CREATE TABLE users (
    id INT PRIMARY KEY IDENTITY(1,1),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(100) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    level INT DEFAULT 1,
    experience INT DEFAULT 0,
    coins INT DEFAULT 100,
    streak INT DEFAULT 0,
    last_login_date DATETIME,
    avatar_url VARCHAR(255),
    is_active BIT DEFAULT 1,
    is_verified BIT DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- Courses table
CREATE TABLE courses (
    id INT PRIMARY KEY IDENTITY(1,1),
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    image_url VARCHAR(255),
    order_index INT NOT NULL,
    is_locked BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- Topics table
CREATE TABLE topics (
    id INT PRIMARY KEY IDENTITY(1,1),
    course_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    order_index INT NOT NULL,
    is_locked BIT DEFAULT 1,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- Lessons table
CREATE TABLE lessons (
    id INT PRIMARY KEY IDENTITY(1,1),
    topic_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL, -- 'lesson', 'quiz', 'coding'
    content TEXT,
    order_index INT NOT NULL,
    xp_reward INT DEFAULT 10,
    coins_reward INT DEFAULT 5,
    estimated_time_minutes INT DEFAULT 10,
    FOREIGN KEY (topic_id) REFERENCES topics(id),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- Quiz questions table
CREATE TABLE quiz_questions (
    id INT PRIMARY KEY IDENTITY(1,1),
    lesson_id INT NOT NULL,
    question TEXT NOT NULL,
    explanation TEXT,
    order_index INT NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- Quiz options table
CREATE TABLE quiz_options (
    id INT PRIMARY KEY IDENTITY(1,1),
    question_id INT NOT NULL,
    option_text TEXT NOT NULL,
    is_correct BIT DEFAULT 0,
    order_index INT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES quiz_questions(id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- Coding challenges table
CREATE TABLE coding_challenges (
    id INT PRIMARY KEY IDENTITY(1,1),
    lesson_id INT NOT NULL,
    instructions TEXT NOT NULL,
    initial_code TEXT,
    solution_code TEXT NOT NULL,
    expected_output TEXT,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- User progress table
CREATE TABLE user_progress (
    id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT NOT NULL,
    lesson_id INT NOT NULL,
    is_completed BIT DEFAULT 0,
    score INT,
    completed_at DATETIME,
    attempts INT DEFAULT 0,
    last_attempt_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (lesson_id) REFERENCES lessons(id),
    CONSTRAINT UC_UserLesson UNIQUE (user_id, lesson_id),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- Achievements table
CREATE TABLE achievements (
    id INT PRIMARY KEY IDENTITY(1,1),
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(50) NOT NULL,
    condition_type VARCHAR(50) NOT NULL, -- 'lesson_completed', 'streak', 'quiz_score', etc.
    condition_value INT NOT NULL, -- value to compare against condition
    xp_reward INT DEFAULT 25,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- User achievements table
CREATE TABLE user_achievements (
    id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT NOT NULL,
    achievement_id INT NOT NULL,
    earned_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (achievement_id) REFERENCES achievements(id),
    CONSTRAINT UC_UserAchievement UNIQUE (user_id, achievement_id),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- User activity table
CREATE TABLE user_activity (
    id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT NOT NULL,
    activity_type VARCHAR(50) NOT NULL, -- 'lesson_completed', 'achievement', 'level_up', etc.
    activity_data NVARCHAR(MAX), -- JSON data about the activity
    xp_earned INT DEFAULT 0,
    coins_earned INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id),
    created_at DATETIME DEFAULT GETDATE()
);

-- Daily goals table
CREATE TABLE daily_goals (
    id INT PRIMARY KEY IDENTITY(1,1),
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    goal_type VARCHAR(50) NOT NULL, -- 'lessons', 'coding', 'quiz', 'xp'
    target_value INT NOT NULL,
    xp_reward INT DEFAULT 20,
    coins_reward INT DEFAULT 10,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- User daily goals table
CREATE TABLE user_daily_goals (
    id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT NOT NULL,
    goal_id INT NOT NULL,
    progress INT DEFAULT 0,
    is_completed BIT DEFAULT 0,
    goal_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (goal_id) REFERENCES daily_goals(id),
    CONSTRAINT UC_UserGoalDate UNIQUE (user_id, goal_id, goal_date),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE coding_challenges (
    id INT PRIMARY KEY IDENTITY(1,1),
    lesson_id INT NOT NULL,
    instructions TEXT NOT NULL,
    initial_code TEXT,
    solution_code TEXT NOT NULL,
    expected_output TEXT,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);
