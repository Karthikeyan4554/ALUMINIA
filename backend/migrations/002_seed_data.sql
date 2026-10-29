-- =========================================================================
-- ALUMNIA — SEED SCRIPT FOR SUPABASE / POSTGRESQL SQL EDITOR
-- Fictional realistic alumni, student demo account, mentorship, and opportunities
-- =========================================================================

-- Note: In Supabase, auth.users is managed by GoTrue. This script inserts
-- corresponding profile records into the public tables with realistic fictional data.

INSERT INTO users (id, email, hashed_password, role, is_active, is_verified)
VALUES 
    ('11111111-1111-1111-1111-111111111111', 'admin@alumnia.edu', '$2b$12$K1r.mZ7.Vw180X99pGq4.eEwO4n7F/K4Y0mG2J/6B4KkXQ/W9F9K', 'admin', true, true),
    ('22222222-2222-2222-2222-222222222222', 'student@alumnia.edu', '$2b$12$K1r.mZ7.Vw180X99pGq4.eEwO4n7F/K4Y0mG2J/6B4KkXQ/W9F9K', 'student', true, true),
    ('33333333-3333-3333-3333-333333333333', 'priya.sharma@alumni.edu', '$2b$12$K1r.mZ7.Vw180X99pGq4.eEwO4n7F/K4Y0mG2J/6B4KkXQ/W9F9K', 'alumni', true, true),
    ('44444444-4444-4444-4444-444444444444', 'marcus.vance@alumni.edu', '$2b$12$K1r.mZ7.Vw180X99pGq4.eEwO4n7F/K4Y0mG2J/6B4KkXQ/W9F9K', 'alumni', true, true),
    ('55555555-5555-5555-5555-555555555555', 'elena.rostova@alumni.edu', '$2b$12$K1r.mZ7.Vw180X99pGq4.eEwO4n7F/K4Y0mG2J/6B4KkXQ/W9F9K', 'alumni', true, true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO profiles (
    user_id, full_name, role, department, graduation_year, headline, bio, avatar_url, 
    current_company, current_job_title, industry, years_of_experience, mentorship_available
) VALUES
    ('11111111-1111-1111-1111-111111111111', 'Dr. Eleanor Vance', 'admin', 'Career Services', 2005, 'Dean of Alumni Affairs', 'Leading institutional initiatives.', 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80', 'University Administration', 'Dean', 'Higher Education', 18, false),
    ('22222222-2222-2222-2222-222222222222', 'Jordan Rivera', 'student', 'Computer Science', 2026, 'Final-Year CS Student | Aspiring ML Engineer', 'Undergraduate passionate about AI and distributed systems.', 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=300&auto=format&fit=crop&q=80', 'Apex University', 'Student Researcher', 'Software & Cloud', 0, false),
    ('33333333-3333-3333-3333-333333333333', 'Priya Sharma', 'alumni', 'Computer Science', 2021, 'Senior ML Engineer at Google', 'Working on multimodal AI systems and large language models.', 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=300&auto=format&fit=crop&q=80', 'Google', 'Senior ML Engineer', 'Artificial Intelligence', 5, true),
    ('44444444-4444-4444-4444-444444444444', 'Marcus Vance', 'alumni', 'Computer Science', 2019, 'Lead Full-Stack Architect at Stripe', 'Architecting resilient checkout pipelines and global APIs.', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&auto=format&fit=crop&q=80', 'Stripe', 'Lead Full-Stack Architect', 'FinTech', 7, true),
    ('55555555-5555-5555-5555-555555555555', 'Elena Rostova', 'alumni', 'Information Systems', 2018, 'Senior Product Manager at Microsoft', 'Azure developer platform strategy and client tooling.', 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=300&auto=format&fit=crop&q=80', 'Microsoft', 'Senior Product Manager', 'Software & Cloud', 8, true)
ON CONFLICT (user_id) DO NOTHING;
