import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

class AcademicRecommender:
    def __init__(self):
        self.student_profiles = None
        self.course_data = None
        self.enrollment_data = None
        self.user_course_matrix = None
        self.course_similarity_matrix = None
        
    def load_data(self, student_profiles_path, course_data_path, enrollment_data_path):
        """Load the necessary data files."""
        self.student_profiles = pd.read_csv(student_profiles_path)
        self.course_data = pd.read_csv(course_data_path)
        self.enrollment_data = pd.read_csv(enrollment_data_path)
        
    def prepare_user_course_matrix(self):
        """Create a user-course matrix for collaborative filtering."""
        # Create pivot table of student-course grades
        self.user_course_matrix = self.enrollment_data.pivot(
            index='student_id',
            columns='course_id',
            values='grade'
        ).fillna(0)
        
    def calculate_course_similarity(self):
        """Calculate similarity between courses using content-based features."""
        # Prepare course features
        course_features = pd.get_dummies(
            self.course_data[['department', 'course_type']]
        )
        
        # Add numerical features
        course_features['credits'] = self.course_data['credits']
        course_features['difficulty'] = self.course_data['difficulty']
        
        # Calculate similarity matrix
        self.course_similarity_matrix = cosine_similarity(course_features)
        
    def get_course_recommendations(self, student_id, n_recommendations=5, exclude_courses=None):
        """Get course recommendations for a specific student."""
        if self.user_course_matrix is None:
            self.prepare_user_course_matrix()
        if self.course_similarity_matrix is None:
            self.calculate_course_similarity()
            
        # Get student's course history
        student_courses = self.user_course_matrix.loc[student_id]
        taken_courses = student_courses[student_courses > 0].index
        
        # Add courses to exclude
        if exclude_courses:
            taken_courses = taken_courses.union(pd.Index(exclude_courses))
        
        # Get student profile
        student_profile = self.student_profiles[
            self.student_profiles['student_id'] == student_id
        ].iloc[0]
        
        # Calculate recommendation scores
        scores = []
        for course_id in self.course_data['course_id']:
            if course_id in taken_courses:
                continue
                
            # Content-based score
            course_info = self.course_data[
                self.course_data['course_id'] == course_id
            ].iloc[0]
            
            # Match with student's interest area
            interest_score = 1.0 if course_info['department'] in student_profile['interest_area'] else 0.5
            
            # Consider course difficulty and student's GPA
            difficulty_score = 1.0 - abs(course_info['difficulty'] - (student_profile['gpa'] / 4.0))
            
            # Collaborative filtering score
            similar_courses = self.course_similarity_matrix[course_id - 1]
            cf_score = np.mean([
                student_courses[course_idx + 1] * similar_courses[course_idx]
                for course_idx in range(len(similar_courses))
            ])
            
            # Combine scores
            final_score = (interest_score * 0.4 + difficulty_score * 0.3 + cf_score * 0.3)
            scores.append((course_id, final_score))
        
        # Sort and return top recommendations
        recommendations = sorted(scores, key=lambda x: x[1], reverse=True)[:n_recommendations]
        
        # Get detailed course information for recommendations
        recommended_courses = []
        for course_id, score in recommendations:
            course_info = self.course_data[
                self.course_data['course_id'] == course_id
            ].iloc[0]
            recommended_courses.append({
                'course_id': course_id,
                'course_name': course_info['course_name'],
                'department': course_info['department'],
                'credits': course_info['credits'],
                'confidence_score': score
            })
            
        return recommended_courses
    
    def get_study_plan(self, student_id, target_career):
        """Generate a study plan based on career goals."""
        student_profile = self.student_profiles[
            self.student_profiles['student_id'] == student_id
        ].iloc[0]
        
        # Define career paths and required courses
        career_paths = {
            'Software Engineer': ['CS', 'MATH'],
            'Data Scientist': ['CS', 'MATH', 'STAT'],
            'Research Scientist': ['PHYS', 'MATH', 'CS'],
            'Business Analyst': ['BUS', 'MATH', 'CS'],
            'Medical Professional': ['BIO', 'CHEM'],
            'Artist': ['ART'],
            'Teacher': ['PSYCH', 'EDU'],
            'Entrepreneur': ['BUS', 'CS']
        }
        
        required_departments = career_paths.get(target_career, [])
        
        # Get recommended courses for each semester
        study_plan = []
        current_semester = student_profile['semester']
        used_courses = set()  # Track courses already in the study plan
        
        for semester in range(current_semester, 9):
            # Get recommendations for this semester
            recommendations = self.get_course_recommendations(
                student_id,
                n_recommendations=10,  # Get more recommendations to filter from
                exclude_courses=list(used_courses)
            )
            
            # Filter recommendations based on career path and not used before
            relevant_courses = [
                course for course in recommendations
                if course['department'] in required_departments
                and course['course_id'] not in used_courses
            ]
            
            # Add to study plan (limit to 4 courses per semester)
            semester_courses = relevant_courses[:4]
            study_plan.append({
                'semester': semester,
                'courses': semester_courses
            })
            
            # Update used courses
            used_courses.update(course['course_id'] for course in semester_courses)
            
        return study_plan

if __name__ == "__main__":
    # Example usage
    recommender = AcademicRecommender()
    recommender.load_data(
        'data/student_profiles.csv',
        'data/course_data.csv',
        'data/enrollment_data.csv'
    )
    
    # Get recommendations for a student
    student_id = 1
    recommendations = recommender.get_course_recommendations(student_id)
    print("\nCourse Recommendations:")
    for course in recommendations:
        print(f"- {course['course_name']} ({course['department']}) - Score: {course['confidence_score']:.2f}")
    
    # Get study plan
    study_plan = recommender.get_study_plan(student_id, 'Software Engineer')
    print("\nStudy Plan:")
    for semester in study_plan:
        print(f"\nSemester {semester['semester']}:")
        for course in semester['courses']:
            print(f"- {course['course_name']} ({course['department']})") 