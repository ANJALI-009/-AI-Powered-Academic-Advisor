import streamlit as st
import pandas as pd
from models.recommender import AcademicRecommender

st.set_page_config(page_title="AI-Powered Academic Advisor", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.big-font {
    font-size:32px !important;
    font-weight: bold;
}
.section-title {
    font-size:24px !important;
    color: #4F8BF9;
    margin-top: 2em;
    margin-bottom: 0.5em;
}
.recommend-card {
    background: #f7fafd;
    border-radius: 10px;
    padding: 1em;
    margin-bottom: 1em;
    box-shadow: 0 2px 8px rgba(79,139,249,0.07);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-font">🎓 AI-Powered Academic Advisor</div>', unsafe_allow_html=True)
st.write("Empowering students with personalized course and study plan recommendations based on their performance, interests, and career goals.")

# Load data
def load_data():
    students = pd.read_csv('data/student_profiles.csv')
    return students

def get_recommender():
    recommender = AcademicRecommender()
    recommender.load_data(
        'data/student_profiles.csv',
        'data/course_data.csv',
        'data/enrollment_data.csv'
    )
    return recommender

students = load_data()
recommender = get_recommender()

# Sidebar - Select student
st.sidebar.header("Select Student")
student_id = st.sidebar.selectbox(
    "Student ID",
    students['student_id'],
    format_func=lambda x: f"ID {x} - {students.loc[students['student_id']==x, 'interest_area'].values[0]}"
)

student_profile = students[students['student_id'] == student_id].iloc[0]

# Student Profile
st.markdown('<div class="section-title">Student Profile</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric("GPA", f"{student_profile['gpa']:.2f}")
col2.metric("Study Hours/Week", f"{student_profile['study_hours']:.1f}")
col3.metric("Interest Area", student_profile['interest_area'])
col4.metric("Career Goal", student_profile['career_goal'])
st.write(f"**Current Semester:** {student_profile['semester']}")

# Recommendations
st.markdown('<div class="section-title">Recommended Courses</div>', unsafe_allow_html=True)
recommendations = recommender.get_course_recommendations(student_id)
rec_cols = st.columns(2)
for i, course in enumerate(recommendations):
    with rec_cols[i % 2]:
        st.markdown(f"""
        <div class='recommend-card'>
        <b>{course['course_name']}</b> <br>
        <span style='color:#4F8BF9'>{course['department']}</span> | Credits: {course['credits']}<br>
        <b>Confidence:</b> {course['confidence_score']:.2f}
        </div>
        """, unsafe_allow_html=True)

# Study Plan
st.markdown('<div class="section-title">Personalized Study Plan</div>', unsafe_allow_html=True)
study_plan = recommender.get_study_plan(student_id, student_profile['career_goal'])
for semester in study_plan:
    st.subheader(f"Semester {semester['semester']}")
    if semester['courses']:
        for course in semester['courses']:
            st.markdown(f"- **{course['course_name']}** ({course['department']}) | Credits: {course['credits']} | Confidence: {course['confidence_score']:.2f}")
    else:
        st.write("No new recommended courses for this semester.")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit | AI Academic Advisor") 