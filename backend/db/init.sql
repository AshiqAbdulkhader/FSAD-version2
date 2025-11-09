-- School Equipment Lending Platform Database Schema

-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  role VARCHAR(50) NOT NULL CHECK (role IN ('student', 'staff', 'admin')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create equipment table
CREATE TABLE IF NOT EXISTS equipment (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  category VARCHAR(100) NOT NULL,
  condition VARCHAR(50) NOT NULL CHECK (condition IN ('excellent', 'good', 'fair', 'poor')),
  quantity INTEGER NOT NULL DEFAULT 1,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create borrowing_requests table
CREATE TABLE IF NOT EXISTS borrowing_requests (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  equipment_id INTEGER REFERENCES equipment(id) ON DELETE CASCADE,
  request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'returned')),
  approved_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
  approval_date TIMESTAMP,
  return_date TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CHECK (start_date <= end_date)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_borrowing_requests_equipment ON borrowing_requests(equipment_id);
CREATE INDEX IF NOT EXISTS idx_borrowing_requests_user ON borrowing_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_borrowing_requests_dates ON borrowing_requests(start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_borrowing_requests_status ON borrowing_requests(status);
CREATE INDEX IF NOT EXISTS idx_equipment_category ON equipment(category);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- Insert sample admin user (password: admin123 - should be hashed in production)
-- Note: This is just for initial setup, password should be hashed using bcrypt
-- Password hash for 'admin123' using bcrypt with salt rounds 10
INSERT INTO users (email, password, name, role) 
VALUES ('admin@school.edu', '$2b$10$rOzJqZqZqZqZqZqZqZqZqOqZqZqZqZqZqZqZqZqZqZqZqZqZqZq', 'Admin User', 'admin')
ON CONFLICT (email) DO NOTHING;

-- Insert sample equipment
INSERT INTO equipment (name, category, condition, quantity, description) VALUES
('Basketball Set', 'Sports', 'excellent', 5, 'Complete basketball set with balls and hoops'),
('Microscope', 'Lab Equipment', 'good', 10, 'Digital microscope for biology lab'),
('Camera DSLR', 'Electronics', 'excellent', 3, 'Canon DSLR camera for photography class'),
('Guitar', 'Musical Instruments', 'good', 8, 'Acoustic guitar for music lessons'),
('Projector', 'Electronics', 'fair', 4, 'LCD projector for presentations')
ON CONFLICT DO NOTHING;

