CREATE TABLE incidents (
    record_id SERIAL PRIMARY KEY,
    record_type VARCHAR(50) NOT NULL CHECK (record_type IN ('incident', 'knowledge_article', 'history')),
    number VARCHAR(50) UNIQUE,  -- Only applicable for incidents/knowlege base
    title VARCHAR(255),  -- For knowledge articles
    short_description TEXT,  -- For incidents
    description TEXT,
    priority INT CHECK (priority BETWEEN 1 AND 5),  -- Only for incidents
    state VARCHAR(50),  -- Only for incidents
    assigned_to VARCHAR(100),  -- Only for incidents
    content TEXT,  -- Only for knowledge articles
    action VARCHAR(255),  -- Only for history
    old_value TEXT,  -- Only for history
    new_value TEXT,  -- Only for history
    updated_by VARCHAR(100),  -- Only for history
    created_by VARCHAR(100),  -- For knowledge articles
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



INSERT INTO incidents (record_type, number, short_description, description, priority, state, assigned_to, created_at)
VALUES 
('incident', 'INC1001', 'User cannot log in', 'The user is unable to log into their account due to incorrect credentials.', 2, 'New', 'john.doe', NOW()),
('incident', 'INC1002', 'Laptop not booting', 'The laptop does not start after pressing the power button.', 1, 'In Progress', 'jane.smith', NOW()),
('incident', 'INC1003', 'Slow application performance', 'The CRM application is running extremely slow for all users.', 3, 'New', 'mike.brown', NOW()),
('incident', 'INC1004', 'Email delivery failure', 'Emails sent to external domains are bouncing back.', 2, 'Open', 'susan.lee', NOW());

INSERT INTO incidents (record_type, number, title, content, created_by, created_at)
VALUES 
('knowledge_article', 'KB001', 'How to reset your password', 'Follow these steps to reset your password in case you forget it.', 'admin', NOW()),
('knowledge_article', 'KB002', 'Setting up VPN Access', 'Guide to setting up VPN access for remote work.', 'network_team', NOW()),
('knowledge_article', 'KB003', 'Troubleshooting Wi-Fi Issues', 'Steps to diagnose and fix common Wi-Fi connectivity issues.', 'support_team', NOW()),
('knowledge_article', 'KB004', 'How to configure email on mobile', 'Guide on setting up corporate email on Android and iOS devices.', 'helpdesk', NOW());

INSERT INTO incidents (record_type, number, action, old_value, new_value, updated_by, updated_at)
VALUES 
('history', 'INC1005', 'State changed', 'New', 'In Progress', 'john.doe', NOW()),
('history', 'INC1006', 'Priority updated', '1', '2', 'jane.smith', NOW()),
('history', 'INC1007', 'Assigned to changed', 'mike.brown', 'david.wilson', 'mike.brown', NOW()),
('history', 'INC1008', 'State changed', 'Open', 'Resolved', 'susan.lee', NOW());


select * from incidents;

delete from  incidents;



