import streamlit as st
import random
from datetime import datetime

# Page config
st.set_page_config(
    page_title="AI Mentor",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'user' not in st.session_state:
    st.session_state.user = ''
if 'subject' not in st.session_state:
    st.session_state.subject = ''
if 'level' not in st.session_state:
    st.session_state.level = 'Beginner'
if 'diagnostic_done' not in st.session_state:
    st.session_state.diagnostic_done = False
if 'diagnostic_answers' not in st.session_state:
    st.session_state.diagnostic_answers = {}
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'weaknesses' not in st.session_state:
    st.session_state.weaknesses = []
if 'strengths' not in st.session_state:
    st.session_state.strengths = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'quiz_taken' not in st.session_state:
    st.session_state.quiz_taken = False
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0

# Custom CSS
st.markdown("""
<style>
    .main-title {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
    }
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .success-badge {
        background-color: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# LOGIN PAGE
# ============================================
if st.session_state.page == 'login':
    st.markdown('<div class="main-title">', unsafe_allow_html=True)
    st.markdown("# 🎓 AI Mentor")
    st.markdown("## Your Personalized Learning Assistant")
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            name = st.text_input("Enter your name:", placeholder="Your name")
            if st.button("🚀 Start Learning", use_container_width=True):
                if name:
                    st.session_state.user = name
                    st.session_state.page = 'setup'
                    st.rerun()
                else:
                    st.error("Please enter your name!")
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SETUP PAGE
# ============================================
elif st.session_state.page == 'setup':
    st.markdown('<div class="main-title">', unsafe_allow_html=True)
    st.markdown(f"# Welcome, {st.session_state.user}! 👋")
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("## 🎯 Learning Setup")
        
        col1, col2 = st.columns(2)
        with col1:
            subject = st.selectbox("Select Subject", [
                "Python Programming",
                "Data Structures & Algorithms",
                "Web Development",
                "Machine Learning",
                "Database Management"
            ])
            st.session_state.subject = subject
        
        with col2:
            level = st.selectbox("Your Level", ["Beginner", "Intermediate", "Advanced"])
            st.session_state.level = level
        
        goal = st.text_input("Your Learning Goal (optional)", placeholder="e.g., Get a job, Build projects, Pass exam")
        
        if st.button("🔍 Start Diagnostic Test", use_container_width=True):
            st.session_state.page = 'diagnostic'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# DIAGNOSTIC PAGE
# ============================================
elif st.session_state.page == 'diagnostic':
    st.markdown('<div class="main-title">', unsafe_allow_html=True)
    st.markdown("## 🧠 Diagnostic Assessment")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.info("Answer these questions honestly to help me understand your level.")
    
    questions = [
        f"What is the most important concept in {st.session_state.subject}?",
        f"Describe a real-world application of {st.session_state.subject}.",
        f"What topics in {st.session_state.subject} do you find most challenging?",
        f"How would you teach {st.session_state.subject} to a beginner?",
        f"What's your goal for learning {st.session_state.subject}?"
    ]
    
    answers = {}
    for i, q in enumerate(questions, 1):
        with st.container():
            st.markdown(f"**Q{i}: {q}**")
            answer = st.text_area("Your answer:", key=f"q{i}", height=100)
            answers[i] = answer
            st.markdown("---")
    
    if st.button("📊 Submit Answers", use_container_width=True):
        # Calculate score based on answer length
        total_score = 0
        for ans in answers.values():
            if ans:
                score = min(len(ans) / 50, 1.0) * 20
                total_score += score
            else:
                total_score += 5
        
        st.session_state.score = int(min(total_score / len(questions) * 1.2 + 50, 95))
        
        # Generate strengths and weaknesses
        all_strengths = [
            "Understanding fundamentals",
            "Practical thinking",
            "Problem-solving",
            "Learning attitude",
            "Persistence"
        ]
        
        all_weaknesses = [
            f"Advanced {st.session_state.subject} concepts",
            "Code optimization",
            "Debugging skills",
            "Time management",
            "Project planning"
        ]
        
        random.seed(st.session_state.score)
        st.session_state.strengths = random.sample(all_strengths, 3)
        st.session_state.weaknesses = random.sample(all_weaknesses, 3)
        
        st.session_state.diagnostic_done = True
        st.session_state.page = 'results'
        st.rerun()

# ============================================
# RESULTS PAGE
# ============================================
elif st.session_state.page == 'results':
    st.markdown('<div class="main-title">', unsafe_allow_html=True)
    st.markdown("## 📊 Your Diagnostic Results")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", f"{st.session_state.score}%")
    with col2:
        level_text = "Intermediate" if st.session_state.score > 70 else "Beginner" if st.session_state.score < 50 else "Advanced"
        st.metric("Assessed Level", level_text)
    with col3:
        st.metric("Status", "Completed ✅")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ✅ Your Strengths")
        for s in st.session_state.strengths:
            st.markdown(f"• {s}")
    
    with col2:
        st.markdown("### ⚠️ Areas to Improve")
        for w in st.session_state.weaknesses:
            st.markdown(f"• {w}")
    
    st.markdown("---")
    st.markdown("### 🎯 Recommendations")
    st.markdown(f"• Practice {st.session_state.weaknesses[0]} daily")
    st.markdown(f"• Build a project using {st.session_state.subject}")
    st.markdown("• Take weekly quizzes to track progress")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗺️ View Learning Path", use_container_width=True):
            st.session_state.page = 'path'
            st.rerun()
    with col2:
        if st.button("💬 Chat with AI Tutor", use_container_width=True):
            st.session_state.page = 'tutor'
            st.rerun()

# ============================================
# LEARNING PATH PAGE
# ============================================
elif st.session_state.page == 'path':
    st.markdown('<div class="main-title">', unsafe_allow_html=True)
    st.markdown("## 🗺️ Your Learning Path")
    st.markdown('</div>', unsafe_allow_html=True)
    
    milestones = [
        {"week": 1, "title": f"{st.session_state.subject} Fundamentals", "hours": 10},
        {"week": 2, "title": "Core Concepts & Practice", "hours": 12},
        {"week": 3, "title": "Advanced Topics", "hours": 15},
        {"week": 4, "title": "Project Building", "hours": 20},
        {"week": 5, "title": "Review & Polish", "hours": 10},
        {"week": 6, "title": "Final Assessment", "hours": 8}
    ]
    
    st.info(f"📌 Based on your {st.session_state.level} level, here's your personalized 6-week plan")
    
    for m in milestones:
        with st.expander(f"Week {m['week']}: {m['title']}"):
            st.markdown(f"**Estimated time:** {m['hours']} hours")
            st.markdown(f"**Focus area:** {st.session_state.weaknesses[0] if m['week'] > 2 else 'Building strong foundation'}")
            if st.button(f"Mark Week {m['week']} Complete", key=f"week_{m['week']}"):
                st.success(f"Great progress! Week {m['week']} completed! 🎉")
    
    if st.button("💬 Continue to AI Tutor", use_container_width=True):
        st.session_state.page = 'tutor'
        st.rerun()

# ============================================
# AI TUTOR PAGE
# ============================================
elif st.session_state.page == 'tutor':
    st.markdown('<div class="main-title">', unsafe_allow_html=True)
    st.markdown("## 💬 AI Tutor")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat display
    for chat in st.session_state.chat_history:
        if chat['role'] == 'user':
            st.markdown(f"**You:** {chat['content']}")
        else:
            st.markdown(f"**🤖 AI Tutor:** {chat['content']}")
        st.markdown("---")
    
    # Suggested questions
    st.markdown("### 💡 Suggested Questions")
    cols = st.columns(3)
    suggestions = [
        f"Explain {st.session_state.subject} basics",
        f"How to learn {st.session_state.subject} faster?",
        f"Common mistakes in {st.session_state.weaknesses[0]}"
    ]
    
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st.button(suggestion, key=f"sugg_{i}", use_container_width=True):
                st.session_state.chat_history.append({'role': 'user', 'content': suggestion})
                
                # Generate response
                response = f"""Thanks for asking about "{suggestion}"!

Here's what you should know about {st.session_state.subject}:

**Key Point:** This is an important concept for {st.session_state.level} level learners.

**Practical Tip:** Practice daily for 30 minutes to see improvement.

**Next Step:** Would you like me to provide an example?

Keep up the great work! 🚀"""
                
                st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                st.rerun()
    
    # Chat input
    user_input = st.text_input("Ask your question:", placeholder="Type your question here...")
    
    if st.button("Send", use_container_width=True):
        if user_input:
            st.session_state.chat_history.append({'role': 'user', 'content': user_input})
            
            response = f"""Great question about "{user_input}"!

Here's my response for a {st.session_state.level} level learner:

**Core Concept:** This relates to fundamental principles of {st.session_state.subject}.

**Learning Tip:** Try breaking it down into smaller parts and practice each part separately.

**Remember:** Every expert was once a beginner. Keep asking questions!

Would you like me to explain further with an example?"""
            
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    
    if st.button("📝 Take a Quiz", use_container_width=True):
        st.session_state.page = 'quiz'
        st.rerun()

# ============================================
# QUIZ PAGE
# ============================================
elif st.session_state.page == 'quiz':
    st.markdown('<div class="main-title">', unsafe_allow_html=True)
    st.markdown("## 📝 Knowledge Quiz")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not st.session_state.quiz_taken:
        questions = [
            {
                "q": f"What is the first step in learning {st.session_state.subject}?",
                "options": ["Understanding basics", "Memorizing everything", "Building complex projects", "Reading documentation"]
            },
            {
                "q": f"Which is most important for mastering {st.session_state.subject}?",
                "options": ["Daily practice", "Only theory", "Watching videos", "Reading books"]
            },
            {
                "q": f"How can you improve in {st.session_state.weaknesses[0] if st.session_state.weaknesses else st.session_state.subject}?",
                "options": ["Practice regularly", "Ignore it", "Only study theory", "Memorize examples"]
            }
        ]
        
        answers = {}
        for i, q in enumerate(questions):
            st.markdown(f"**Q{i+1}: {q['q']}**")
            answer = st.radio("Select answer:", q['options'], key=f"quiz_{i}", index=None)
            answers[i] = answer
            st.markdown("---")
        
        if st.button("✅ Submit Quiz", use_container_width=True):
            correct = 0
            # Check answers (first option is correct for all)
            for i, ans in answers.items():
                if ans and ans.startswith(questions[i]['options'][0][:10]):
                    correct += 1
            
            st.session_state.quiz_score = (correct / len(questions)) * 100
            st.session_state.quiz_taken = True
            st.rerun()
    
    else:
        # Show results
        if st.session_state.quiz_score >= 70:
            st.success(f"🎉 Great job! You scored {st.session_state.quiz_score:.0f}%!")
        else:
            st.warning(f"💪 You scored {st.session_state.quiz_score:.0f}%. Keep practicing!")
        
        st.markdown("### 📊 Quiz Results")
        st.progress(st.session_state.quiz_score / 100)
        
        if st.button("🔄 Take Another Quiz", use_container_width=True):
            st.session_state.quiz_taken = False
            st.rerun()
        
        if st.button("🏠 Back to Dashboard", use_container_width=True):
            st.session_state.page = 'results'
            st.rerun()

# ============================================
# SIDEBAR PROGRESS
# ============================================
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user}")
    st.markdown("---")
    
    if st.session_state.diagnostic_done:
        st.markdown("### 📊 Progress")
        st.metric("Diagnostic Score", f"{st.session_state.score}%")
        st.metric("Level", st.session_state.level)
        
        if st.session_state.quiz_taken:
            st.metric("Quiz Score", f"{st.session_state.quiz_score:.0f}%")
        
        st.markdown("---")
        st.markdown("### 🎯 Focus Areas")
        for w in st.session_state.weaknesses[:2]:
            st.markdown(f"• {w}")
    
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
