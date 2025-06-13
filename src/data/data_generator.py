import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class StudentDataGenerator:
    def __init__(self, n_students=1000, n_courses=50):
        self.n_students = n_students
        self.n_courses = n_courses
        self.course_difficulties = np.random.normal(0.5, 0.15, n_courses)
        self.course_difficulties = np.clip(self.course_difficulties, 0.1, 0.9)
        
    def generate_student_profiles(self):
        """Generate student profiles with academic interests and career goals."""
        interests = ['Computer Science', 'Mathematics', 'Physics', 'Biology', 
                    'Chemistry', 'Engineering', 'Business', 'Arts', 'Psychology']
        
        career_goals = ['Software Engineer', 'Data Scientist', 'Research Scientist',
                       'Business Analyst', 'Medical Professional', 'Artist', 
                       'Teacher', 'Entrepreneur']
        
        data = {
            'student_id': range(1, self.n_students + 1),
            'gpa': np.random.normal(3.0, 0.5, self.n_students),
            'study_hours': np.random.normal(20, 5, self.n_students),
            'interest_area': np.random.choice(interests, self.n_students),
            'career_goal': np.random.choice(career_goals, self.n_students),
            'semester': np.random.randint(1, 9, self.n_students)
        }
        
        return pd.DataFrame(data)
    
    def generate_course_data(self):
        """Generate course information."""
        departments = ['CS', 'MATH', 'PHYS', 'BIO', 'CHEM', 'ENG', 'BUS', 'ART', 'PSYCH']
        course_types = ['Core', 'Elective', 'Advanced', 'Introductory']
        
        data = {
            'course_id': range(1, self.n_courses + 1),
            'course_name': [f'Course_{i}' for i in range(1, self.n_courses + 1)],
            'department': np.random.choice(departments, self.n_courses),
            'course_type': np.random.choice(course_types, self.n_courses),
            'credits': np.random.choice([3, 4], self.n_courses),
            'difficulty': self.course_difficulties
        }
        
        return pd.DataFrame(data)
    
    def generate_enrollment_data(self, student_profiles, course_data):
        """Generate course enrollment and performance data."""
        enrollments = []
        
        for student_id in student_profiles['student_id']:
            # Each student takes 4-6 courses per semester
            n_courses = np.random.randint(4, 7)
            courses = np.random.choice(course_data['course_id'], n_courses, replace=False)
            
            for course_id in courses:
                # Generate grade based on student GPA and course difficulty
                student_gpa = student_profiles.loc[student_profiles['student_id'] == student_id, 'gpa'].values[0]
                course_difficulty = course_data.loc[course_data['course_id'] == course_id, 'difficulty'].values[0]
                
                # Base grade on GPA and course difficulty with some randomness
                grade = (student_gpa * (1 - course_difficulty) + np.random.normal(0, 0.2)) * 4
                grade = np.clip(grade, 0, 4)
                
                enrollments.append({
                    'student_id': student_id,
                    'course_id': course_id,
                    'grade': grade,
                    'semester': np.random.randint(1, 9)
                })
        
        return pd.DataFrame(enrollments)
    
    def generate_all_data(self):
        """Generate all necessary datasets."""
        student_profiles = self.generate_student_profiles()
        course_data = self.generate_course_data()
        enrollment_data = self.generate_enrollment_data(student_profiles, course_data)
        
        return {
            'student_profiles': student_profiles,
            'course_data': course_data,
            'enrollment_data': enrollment_data
        }

if __name__ == "__main__":
    # Example usage
    generator = StudentDataGenerator()
    data = generator.generate_all_data()
    
    # Save data to CSV files
    data['student_profiles'].to_csv('data/student_profiles.csv', index=False)
    data['course_data'].to_csv('data/course_data.csv', index=False)
    data['enrollment_data'].to_csv('data/enrollment_data.csv', index=False) 