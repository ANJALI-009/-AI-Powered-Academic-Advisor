# AI-Powered Academic Advisor

An intelligent academic advising system that provides personalized course recommendations and study plans for students based on their academic performance, interests, and career goals.

## Features

- Student profile analysis
- Course recommendations based on interests and performance
- Personalized study plans
- Interactive web interface
- Real-time recommendations

## Deployment Instructions

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your forked repository
6. Set the main file path as `src/streamlit_app.py`
7. Click "Deploy"

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
streamlit run src/streamlit_app.py
```

## Project Structure

```
├── src/
│   ├── data/
│   │   └── data_generator.py
│   ├── models/
│   │   └── recommender.py
│   ├── main.py
│   └── streamlit_app.py
├── data/
│   ├── student_profiles.csv
│   ├── course_data.csv
│   └── enrollment_data.csv
├── requirements.txt
└── README.md
```

## Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- NumPy

