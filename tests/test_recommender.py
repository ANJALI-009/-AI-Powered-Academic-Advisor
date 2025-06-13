import unittest
import pandas as pd
import numpy as np
from src.data.data_generator import StudentDataGenerator
from src.models.recommender import AcademicRecommender

class TestAcademicRecommender(unittest.TestCase):
    def setUp(self):
        """Set up test data and recommender system."""
        # Generate small test dataset
        self.generator = StudentDataGenerator(n_students=10, n_courses=20)
        self.data = self.generator.generate_all_data()
        
        # Save test data
        self.data['student_profiles'].to_csv('data/test_student_profiles.csv', index=False)
        self.data['course_data'].to_csv('data/test_course_data.csv', index=False)
        self.data['enrollment_data'].to_csv('data/test_enrollment_data.csv', index=False)
        
        # Initialize recommender
        self.recommender = AcademicRecommender()
        self.recommender.load_data(
            'data/test_student_profiles.csv',
            'data/test_course_data.csv',
            'data/test_enrollment_data.csv'
        )
    
    def test_data_generation(self):
        """Test if data generation works correctly."""
        self.assertEqual(len(self.data['student_profiles']), 10)
        self.assertEqual(len(self.data['course_data']), 20)
        self.assertTrue(len(self.data['enrollment_data']) > 0)
    
    def test_recommendations(self):
        """Test if recommendations are generated correctly."""
        student_id = 1
        recommendations = self.recommender.get_course_recommendations(student_id)
        
        # Check if recommendations are returned
        self.assertTrue(len(recommendations) > 0)
        
        # Check if recommendations have required fields
        for course in recommendations:
            self.assertIn('course_id', course)
            self.assertIn('course_name', course)
            self.assertIn('department', course)
            self.assertIn('credits', course)
            self.assertIn('confidence_score', course)
    
    def test_study_plan(self):
        """Test if study plan generation works correctly."""
        student_id = 1
        target_career = 'Software Engineer'
        study_plan = self.recommender.get_study_plan(student_id, target_career)
        
        # Check if study plan is generated
        self.assertTrue(len(study_plan) > 0)
        
        # Check if each semester has courses
        for semester in study_plan:
            self.assertIn('semester', semester)
            self.assertIn('courses', semester)
            self.assertTrue(len(semester['courses']) > 0)
    
    def test_course_similarity(self):
        """Test if course similarity calculation works."""
        self.recommender.calculate_course_similarity()
        self.assertIsNotNone(self.recommender.course_similarity_matrix)
        self.assertEqual(
            self.recommender.course_similarity_matrix.shape,
            (20, 20)  # 20 courses x 20 courses
        )
    
    def test_user_course_matrix(self):
        """Test if user-course matrix is created correctly."""
        self.recommender.prepare_user_course_matrix()
        self.assertIsNotNone(self.recommender.user_course_matrix)
        self.assertEqual(
            self.recommender.user_course_matrix.shape,
            (10, 20)  # 10 students x 20 courses
        )

if __name__ == '__main__':
    unittest.main() 