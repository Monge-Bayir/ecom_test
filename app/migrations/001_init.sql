CREATE TABLE IF NOT EXISTS grades (
  id BIGSERIAL PRIMARY KEY,
  grade_date DATE NOT NULL,
  group_number TEXT NOT NULL,
  full_name TEXT NOT NULL,
  grade SMALLINT NOT NULL CHECK (grade BETWEEN 2 AND 5),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_grades_full_name ON grades (full_name);
CREATE INDEX IF NOT EXISTS idx_grades_grade ON grades (grade);
CREATE UNIQUE INDEX IF NOT EXISTS uq_grade_fact
ON grades (grade_date, group_number, full_name, grade);