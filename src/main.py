import argparse
from data.data_generator import StudentDataGenerator
from models.recommender import AcademicRecommender

def generate_data():
    """Generate sample data for the system."""
    print("Generating sample data...")
    generator = StudentDataGenerator()
    data = generator.generate_all_data()
    
    # Save data to CSV files
    data['student_profiles'].to_csv('data/student_profiles.csv', index=False)
    data['course_data'].to_csv('data/course_data.csv', index=False)
    data['enrollment_data'].to_csv('data/enrollment_data.csv', index=False)
    print("Data generation complete!")

def get_recommendations(student_id):
    """Get course recommendations for a student."""
    recommender = AcademicRecommender()
    recommender.load_data(
        'data/student_profiles.csv',
        'data/course_data.csv',
        'data/enrollment_data.csv'
    )
    
    # Get student profile
    student_profile = recommender.student_profiles[
        recommender.student_profiles['student_id'] == student_id
    ].iloc[0]
    
    print(f"\nStudent Profile:")
    print(f"ID: {student_id}")
    print(f"GPA: {student_profile['gpa']:.2f}")
    print(f"Study Hours per Week: {student_profile['study_hours']:.1f}")
    print(f"Interest Area: {student_profile['interest_area']}")
    print(f"Career Goal: {student_profile['career_goal']}")
    print(f"Current Semester: {student_profile['semester']}")
    
    # Get course recommendations
    recommendations = recommender.get_course_recommendations(student_id)
    print("\nCourse Recommendations:")
    for course in recommendations:
        print(f"- {course['course_name']} ({course['department']})")
        print(f"  Credits: {course['credits']}")
        print(f"  Confidence Score: {course['confidence_score']:.2f}")
    
    # Get study plan
    study_plan = recommender.get_study_plan(student_id, student_profile['career_goal'])
    print(f"\nStudy Plan for {student_profile['career_goal']}:")
    for semester in study_plan:
        print(f"\nSemester {semester['semester']}:")
        for course in semester['courses']:
            print(f"- {course['course_name']} ({course['department']})")
            print(f"  Credits: {course['credits']}")
            print(f"  Confidence Score: {course['confidence_score']:.2f}")

def main():
    parser = argparse.ArgumentParser(description='AI-Powered Academic Advisor')
    parser.add_argument('--generate-data', action='store_true',
                      help='Generate sample data')
    parser.add_argument('--student-id', type=int,
                      help='Student ID to get recommendations for')
    
    args = parser.parse_args()
    
    if args.generate_data:
        generate_data()
    
    if args.student_id:
        get_recommendations(args.student_id)
    elif not args.generate_data:
        parser.print_help()

if __name__ == "__main__":
    main() 