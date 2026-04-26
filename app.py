import streamlit as st
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Mentor - Personalized Learning Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f0f6ff 0%, #fafbff 50%, #f5f0ff 100%);
    }
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
    }
    .section-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .success-badge {
        background-color: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }
    .warning-badge {
        background-color: #f59e0b;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'subject' not in st.session_state:
    st.session_state.subject = ''
if 'level' not in st.session_state:
    st.session_state.level = 'Beginner'
if 'diagnostic_questions' not in st.session_state:
    st.session_state.diagnostic_questions = []
if 'diagnostic_answers' not in st.session_state:
    st.session_state.diagnostic_answers = {}
if 'evaluation' not in st.session_state:
    st.session_state.evaluation = None
if 'learning_path' not in st.session_state:
    st.session_state.learning_path = None
if 'completed_milestones' not in st.session_state:
    st.session_state.completed_milestones = set()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'quiz_results' not in st.session_state:
    st.session_state.quiz_results = None
if 'quiz_history' not in st.session_state:
    st.session_state.quiz_history = []
if 'tutor_sessions' not in st.session_state:
    st.session_state.tutor_sessions = 0

# ============================================
# AI MOCK FUNCTIONS
# ============================================

def get_diagnostic_questions(subject, level):
    """Generate diagnostic questions"""
    questions = [
        {
            "id": 1,
            "question": f"What is the most fundamental concept in {subject} that every {level} should master first?",
            "hint": "Think about the core building blocks"
        },
        {
            "id": 2,
            "question": f"Describe a real-world application where {subject} plays a crucial role.",
            "hint": "Connect theory to practical scenarios"
        },
        {
            "id": 3,
            "question": f"What aspect of {subject} do you find most difficult to understand?",
            "hint": "Be specific about your struggle points"
        },
        {
            "id": 4,
            "question": f"Explain {subject} in your own words to someone with no technical background.",
            "hint": "Simplicity is key here"
        },
        {
            "id": 5,
            "question": "What's your primary motivation for learning this subject?",
            "hint": "Your goals help personalize the learning path"
        }
    ]
    return questions

def evaluate_answers(subject, level, answers):
    """Evaluate user answers"""
    score = random.randint(60, 95)
    
    strengths = [
        'Understanding of basic concepts',
        'Practical application thinking',
        'Problem-solving approach',
        'Technical vocabulary'
    ][:3]
    
    weaknesses = [
        f'Advanced {subject} concepts',
        'Code optimization techniques',
        'Edge case handling'
    ]
    
    recommendations = [
        f'Practice daily coding exercises in {subject}',
        f'Review {weaknesses[0]} fundamentals',
        'Build a small project applying core concepts'
    ]
    
    assessed_level = level
    if score >= 85 and level != 'Advanced':
        assessed_level = 'Intermediate' if level == 'Beginner' else 'Advanced'
    
    return {
        "score": score,
        "assessedLevel": assessed_level,
        "summary": f"You show a {'strong' if score >= 80 else 'decent'} understanding of {subject}.",
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations
    }

def get_learning_path(subject, level, weaknesses):
    """Generate learning path"""
    milestones = [
        {
            "id": 1,
            "title": f"{subject} Fundamentals",
            "description": f"Master the core concepts of {subject}",
            "difficulty": "Beginner",
            "estimatedHours": 8,
            "topics": ["Core Concepts", "Basic Syntax", "Foundations"]
        },
        {
            "id": 2,
            "title": "Practical Applications",
            "description": "Apply concepts to real-world problems",
            "difficulty": "Intermediate",
            "estimatedHours": 12,
            "topics": ["Problem Solving", "Projects", "Case Studies"]
        },
        {
            "id": 3,
            "title": "Advanced Topics",
            "description": "Deep dive into complex concepts",
            "difficulty": "Advanced",
            "estimatedHours": 15,
            "topics": ["Optimization", "Best Practices", "Advanced Patterns"]
        }
    ]
    
    return {
        "overview": f"Your personalized {level} level journey through {subject}.",
        "totalWeeks": 6,
        "milestones": milestones
    }

def tutor_response(message, subject, level):
    """Generate tutor response"""
    return f"""🤖 **AI Tutor Response**

Thanks for your question about "{message}" in {subject}!

**Key Points:**
- This is an important concept for {level} level learners
- Practice regularly to master this topic
- Try breaking it down into smaller parts

**Pro Tip:** The best way to learn is by doing. Write code every day!

Would you like me to provide an example or explain further?"""

def get_quiz_questions(subject, weaknesses):
    """Generate quiz questions"""
    return [
        {
            "id": 1,
            "question": f"What is the first step when learning {subject}?",
            "options": ["Understanding concepts", "Memorizing syntax", "Building projects", "Reading docs"],
            "correct": "Understanding concepts"
        },
        {
            "id": 2,
            "question": f"Which practice is most effective for mastering {subject}?",
            "options": ["Daily coding", "Only reading", "Watching videos", "Memorization"],
            "correct": "Daily coding"
        },
        {
            "id": 3,
            "question": f"What is your main learning goal for {subject}?",
            "options": None,
            "correct": None
        }
    ]

def grade_quiz(questions, answers):
    """Grade quiz"""
    correct = 0
    results = []
    
    for i, q in enumerate(questions):
        user_answer = answers.get(i, "")
        is_correct = False
        
        if q.get('options'):
            if user_answer == q.get('correct'):
                is_correct = True
                correct += 1
        
        results.append({
            "question": q['question'],
            "userAnswer": user_answer,
            "correct": is_correct
        })
    
    percentage = (correct / len(questions)) * 100 if questions else 0
    
    return {
        "score": correct,
        "total": len(questions),
        "percentage": percentage,
        "results": results
    }

# ============================================
# MAIN UI
# ============================================

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 AI Mentor</h1>
    <p>Your Personalized Technical Learning Assistant</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for progress
with st.sidebar:
    st.markdown("## 📊 Your Progress")
    
    if st.session_state.evaluation:
        st.metric("Diagnostic Score", f"{st.session_state.evaluation['score']}%")
        st.metric("Level", st.session_state.evaluation['assessedLevel'])
        st.metric("Tutor Sessions", st.session_state.tutor_sessions)
        st.metric("Quizzes Taken", len(st.session_state.quiz_history))
        
        if st.session_state.quiz_history:
            avg_score = sum(q['percentage'] for q in st.session_state.quiz_history) / len(st.session_state.quiz_history)
            st.metric("Avg Quiz Score", f"{avg_score:.0f}%")
    
    st.markdown("---")
    st.markdown("### 🎯 Quick Navigation")
    if st.button("📝 Learning Setup"):
        st.session_state.step = 1
        st.rerun()
    if st.button("🧠 Diagnostic"):
        st.session_state.step = 2
        st.rerun()
    if st.button("🗺️ Learning Path"):
        st.session_state.step = 3
        st.rerun()
    if st.button("💬 AI Tutor"):
        st.session_state.step = 4
        st.rerun()
    if st.button("📝 Quiz"):
        st.session_state.step = 5
        st.rerun()

# Step 1: Learning Setup
if st.session_state.step == 1:
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("## 🎯 Learning Profile Setup")
        
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.selectbox(
                "Select Subject",
                ["Programming (Python)", "Data Structures & Algorithms", "Web Development", 
                 "Machine Learning", "Database Management", "Operating Systems"]
            )
            st.session_state.subject = subject
        
        with col2:
            level = st.selectbox(
                "Your Skill Level",
                ["Beginner", "Intermediate", "Advanced"]
            )
            st.session_state.level = level
        
        topics = st.text_area("Topics of Interest (optional)", placeholder="e.g., recursion, algorithms, databases...")
        goal = st.text_input("Learning Goal (optional)", placeholder="e.g., Prepare for interviews, build projects...")
        
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("🔍 Start Diagnostic Assessment", use_container_width=True):
                st.session_state.diagnostic_questions = get_diagnostic_questions(subject, level)
                st.session_state.step = 2
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Step 2: Diagnostic Assessment
elif st.session_state.step == 2:
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("## 🧠 Diagnostic Assessment")
        st.info("Answer these questions honestly to help AI understand your current level.")
        
        if st.session_state.diagnostic_questions:
            answers = {}
            for q in st.session_state.diagnostic_questions:
                answer = st.text_area(f"**Q{q['id']}: {q['question']}**", 
                                     placeholder=f"Hint: {q['hint']}",
                                     key=f"diag_{q['id']}")
                answers[q['id']] = answer
            
            col1, col2, col3 = st.columns([1,1,1])
            with col2:
                if st.button("📊 Evaluate My Answers", use_container_width=True):
                    with st.spinner("AI is evaluating your answers..."):
                        st.session_state.evaluation = evaluate_answers(
                            st.session_state.subject,
                            st.session_state.level,
                            answers
                        )
                        st.session_state.step = 3
                        st.rerun()
        else:
            st.warning("Please complete the learning setup first.")
            if st.button("Go to Setup"):
                st.session_state.step = 1
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Step 3: Learning Path
elif st.session_state.step == 3:
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("## 🗺️ Personalized Learning Path")
        
        if st.session_state.evaluation:
            if not st.session_state.learning_path:
                with st.spinner("Generating your personalized learning path..."):
                    st.session_state.learning_path = get_learning_path(
                        st.session_state.subject,
                        st.session_state.level,
                        st.session_state.evaluation['weaknesses']
                    )
            
            # Show evaluation results
            st.markdown("### 📊 Diagnostic Results")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Score", f"{st.session_state.evaluation['score']}%")
            with col2:
                st.metric("Assessed Level", st.session_state.evaluation['assessedLevel'])
            with col3:
                st.metric("Status", "Completed ✅")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**✅ Strengths**")
                for s in st.session_state.evaluation['strengths']:
                    st.markdown(f"- {s}")
            with col2:
                st.markdown("**⚠️ Areas to Improve**")
                for w in st.session_state.evaluation['weaknesses']:
                    st.markdown(f"- {w}")
            
            st.markdown("---")
            
            # Learning Path
            st.markdown(f"### 🎯 Your Learning Journey")
            st.info(f"**Overview:** {st.session_state.learning_path['overview']} | **Duration:** {st.session_state.learning_path['totalWeeks']} weeks")
            
            for milestone in st.session_state.learning_path['milestones']:
                with st.expander(f"📌 Milestone {milestone['id']}: {milestone['title']}"):
                    st.markdown(f"**Description:** {milestone['description']}")
                    st.markdown(f"**Difficulty:** {milestone['difficulty']}")
                    st.markdown(f"**Estimated Time:** {milestone['estimatedHours']} hours")
                    st.markdown(f"**Topics:** {', '.join(milestone['topics'])}")
                    
                    if st.button(f"✅ Mark Complete", key=f"complete_{milestone['id']}"):
                        st.session_state.completed_milestones.add(milestone['id'])
                        st.success("Milestone completed! 🎉")
                        st.rerun()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💬 Continue to AI Tutor", use_container_width=True):
                    st.session_state.step = 4
                    st.rerun()
            with col2:
                if st.button("📝 Take a Quiz", use_container_width=True):
                    st.session_state.step = 5
                    st.rerun()
        else:
            st.warning("Please complete the diagnostic assessment first.")
            if st.button("Go to Diagnostic"):
                st.session_state.step = 2
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Step 4: AI Tutor
elif st.session_state.step == 4:
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("## 💬 AI Tutor")
        st.info("Ask me anything about your subject! I'm here to help you learn.")
        
        # Chat interface
        chat_container = st.container()
        
        with chat_container:
            for msg in st.session_state.chat_history:
                if msg['role'] == 'user':
                    st.markdown(f"**You:** {msg['content']}")
                else:
                    st.markdown(f"**🤖 AI Tutor:** {msg['content']}")
                st.markdown("---")
        
        # Suggested questions
        st.markdown("### 💡 Suggested Questions")
        col1, col2, col3 = st.columns(3)
        
        questions = [
            f"Explain {st.session_state.subject} basics",
            "Give me a practical example",
            "What are common mistakes?",
            "How can I improve faster?",
            "Show me a code example"
        ]
        
        cols = [col1, col2, col3]
        for i, q in enumerate(questions[:3]):
            with cols[i]:
                if st.button(q, key=f"suggest_{i}", use_container_width=True):
                    st.session_state.chat_history.append({'role': 'user', 'content': q})
                    with st.spinner("AI is thinking..."):
                        response = tutor_response(q, st.session_state.subject, st.session_state.level)
                        st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                        st.session_state.tutor_sessions += 1
                    st.rerun()
        
        # Chat input
        user_input = st.text_input("Ask your question:", key="chat_input", placeholder="Type your question here...")
        
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("Send Message", use_container_width=True):
                if user_input:
                    st.session_state.chat_history.append({'role': 'user', 'content': user_input})
                    with st.spinner("AI is thinking..."):
                        response = tutor_response(user_input, st.session_state.subject, st.session_state.level)
                        st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                        st.session_state.tutor_sessions += 1
                    st.rerun()
        
        if st.button("🗑 Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Step 5: Quiz
elif st.session_state.step == 5:
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("## 📝 Knowledge Quiz")
        
        if st.session_state.evaluation:
            if st.button("🔄 Generate New Quiz", use_container_width=True):
                with st.spinner("Generating quiz..."):
                    st.session_state.quiz_questions = get_quiz_questions(
                        st.session_state.subject,
                        st.session_state.evaluation['weaknesses']
                    )
                    st.session_state.quiz_results = None
                    st.rerun()
            
            if st.session_state.quiz_questions and not st.session_state.quiz_results:
                st.markdown("### Answer the following questions:")
                answers = {}
                
                for i, q in enumerate(st.session_state.quiz_questions):
                    st.markdown(f"**Q{i+1}: {q['question']}**")
                    
                    if q.get('options'):
                        answer = st.radio("Select your answer:", q['options'], key=f"quiz_{i}")
                        answers[i] = answer
                    else:
                        answer = st.text_area("Your answer:", key=f"quiz_{i}", placeholder="Type your answer here...")
                        answers[i] = answer
                    
                    st.markdown("---")
                
                if st.button("✅ Submit Quiz", use_container_width=True):
                    with st.spinner("Grading your quiz..."):
                        results = grade_quiz(st.session_state.quiz_questions, answers)
                        st.session_state.quiz_results = results
                        st.session_state.quiz_history.append({
                            'date': datetime.now().strftime("%Y-%m-%d"),
                            'percentage': results['percentage']
                        })
                        st.rerun()
            
            elif st.session_state.quiz_results:
                # Show results
                results = st.session_state.quiz_results
                
                if results['percentage'] >= 60:
                    st.success(f"🎉 You scored {results['percentage']:.0f}% - Great job!")
                else:
                    st.warning(f"💪 You scored {results['percentage']:.0f}% - Keep practicing!")
                
                st.markdown(f"**Score:** {results['score']}/{results['total']}")
                
                st.markdown("### Detailed Results:")
                for i, res in enumerate(results['results']):
                    with st.expander(f"Question {i+1}: {res['question']}"):
                        st.markdown(f"**Your answer:** {res['userAnswer']}")
                        if res['correct']:
                            st.markdown("✅ **Correct!**")
                        else:
                            st.markdown("❌ **Incorrect**")
                
                if st.button("🔄 Take Another Quiz", use_container_width=True):
                    st.session_state.quiz_results = None
                    st.session_state.quiz_questions = []
                    st.rerun()
        else:
            st.warning("Please complete the diagnostic assessment first.")
            if st.button("Go to Diagnostic"):
                st.session_state.step = 2
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🎓 AI Mentor - Your Personalized Learning Assistant | Powered by AI</p>
</div>
""", unsafe_allow_html=True)
