import streamlit as st
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Mentor - Personalized Learning Assistant",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS with #F2F0EB background
st.markdown("""
<style>
    /* Main background color */
    .stApp {
        background-color: #F2F0EB;
    }
    
    /* Main container */
    .main {
        background-color: #F2F0EB;
    }
    
    /* Title header */
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Card style */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    /* Success badge */
    .success-badge {
        background-color: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
        font-size: 0.875rem;
    }
    
    /* Warning badge */
    .warning-badge {
        background-color: #f59e0b;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
        font-size: 0.875rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: white;
    }
    
    /* Info box */
    .info-box {
        background-color: #eef2ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    /* Metric card */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    /* Chat message styling */
    .user-message {
        background-color: #667eea;
        color: white;
        padding: 0.75rem;
        border-radius: 15px;
        margin: 0.5rem 0;
    }
    
    .assistant-message {
        background-color: #f3f4f6;
        color: #1f2937;
        padding: 0.75rem;
        border-radius: 15px;
        margin: 0.5rem 0;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'subject' not in st.session_state:
    st.session_state.subject = "Python Programming"
if 'level' not in st.session_state:
    st.session_state.level = "Beginner"
if 'diagnostic_answers' not in st.session_state:
    st.session_state.diagnostic_answers = {}
if 'diagnostic_complete' not in st.session_state:
    st.session_state.diagnostic_complete = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'strengths' not in st.session_state:
    st.session_state.strengths = []
if 'weaknesses' not in st.session_state:
    st.session_state.weaknesses = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'quiz_taken' not in st.session_state:
    st.session_state.quiz_taken = False
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'current_page' not in st.session_state:
    st.session_state.current_page = "login"

# ============================================
# LOGIN PAGE
# ============================================
if st.session_state.current_page == "login":
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown("# 🎓 AI Mentor")
        st.markdown("## Your Personalized Learning Assistant")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Welcome! 👋")
        
        name = st.text_input("Enter your name to begin:", placeholder="Your name")
        
        if st.button("🚀 Start Learning Journey", use_container_width=True):
            if name:
                st.session_state.user_name = name
                st.session_state.logged_in = True
                st.session_state.current_page = "setup"
                st.rerun()
            else:
                st.error("Please enter your name to continue!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# MAIN APP
# ============================================
elif st.session_state.logged_in:
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👋 Welcome, {st.session_state.user_name}!")
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📚 Navigation")
        
        if st.button("🎯 Learning Setup", use_container_width=True):
            st.session_state.current_page = "setup"
            st.rerun()
        
        if st.button("🧠 Diagnostic Test", use_container_width=True):
            if st.session_state.subject:
                st.session_state.current_page = "diagnostic"
                st.rerun()
            else:
                st.error("Please complete learning setup first!")
        
        if st.button("📊 Results", use_container_width=True):
            if st.session_state.diagnostic_complete:
                st.session_state.current_page = "results"
                st.rerun()
            else:
                st.error("Please complete diagnostic test first!")
        
        if st.button("🗺️ Learning Path", use_container_width=True):
            if st.session_state.diagnostic_complete:
                st.session_state.current_page = "path"
                st.rerun()
            else:
                st.error("Please complete diagnostic test first!")
        
        if st.button("💬 AI Tutor", use_container_width=True):
            if st.session_state.subject:
                st.session_state.current_page = "tutor"
                st.rerun()
            else:
                st.error("Please complete learning setup first!")
        
        if st.button("📝 Take Quiz", use_container_width=True):
            if st.session_state.diagnostic_complete:
                st.session_state.current_page = "quiz"
                st.rerun()
            else:
                st.error("Please complete diagnostic test first!")
        
        st.markdown("---")
        
        # Progress metrics
        if st.session_state.diagnostic_complete:
            st.markdown("### 📊 Your Progress")
            st.metric("Diagnostic Score", f"{st.session_state.score}%")
            st.metric("Level", st.session_state.level)
            
            if st.session_state.quiz_taken:
                st.metric("Quiz Score", f"{st.session_state.quiz_score:.0f}%")
            
            st.markdown("---")
            st.markdown("### 🎯 Focus Areas")
            for w in st.session_state.weaknesses[:2]:
                st.markdown(f"• {w}")
        
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Page: Learning Setup
    if st.session_state.current_page == "setup":
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown(f"# Welcome, {st.session_state.user_name}! 👋")
        st.markdown("## Let's set up your learning profile")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("## 🎯 Learning Profile Setup")
        
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.selectbox(
                "Select your subject",
                ["Python Programming", "Data Structures & Algorithms", "Web Development",
                 "Machine Learning", "Database Management", "Operating Systems"]
            )
            st.session_state.subject = subject
        
        with col2:
            level = st.selectbox(
                "Your current skill level",
                ["Beginner", "Intermediate", "Advanced"]
            )
            st.session_state.level = level
        
        topics = st.text_area("Topics you're interested in (optional)", 
                             placeholder="e.g., data structures, algorithms, web development...")
        
        goal = st.text_input("Your learning goal (optional)",
                            placeholder="e.g., Prepare for technical interviews, build projects, career change...")
        
        if st.button("🔍 Start Diagnostic Test", use_container_width=True):
            st.session_state.current_page = "diagnostic"
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Page: Diagnostic Test
    elif st.session_state.current_page == "diagnostic":
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown("## 🧠 Diagnostic Assessment")
        st.markdown("Answer these questions honestly to help me understand your level")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        questions = [
            f"What is the most important concept in {st.session_state.subject} that every {st.session_state.level} should know?",
            f"Describe a real-world application where {st.session_state.subject} is used.",
            f"What specific topics in {st.session_state.subject} do you find most challenging?",
            f"How would you explain {st.session_state.subject} to someone with no technical background?",
            f"What are your career goals and how does {st.session_state.subject} help achieve them?"
        ]
        
        answers = {}
        for i, q in enumerate(questions, 1):
            st.markdown(f"**Q{i}: {q}**")
            answer = st.text_area("Your answer:", key=f"diag_{i}", height=100)
            answers[i] = answer
            st.markdown("---")
        
        if st.button("📊 Submit & Evaluate", use_container_width=True):
            with st.spinner("🤖 AI is analyzing your responses..."):
                # Calculate score
                total_score = 0
                for ans in answers.values():
                    if ans:
                        score = min(len(ans) / 100, 1.0) * 20
                        total_score += score
                    else:
                        total_score += 5
                
                st.session_state.score = int(min(total_score / len(questions) * 1.5 + 50, 95))
                
                # Generate strengths and weaknesses
                strengths_pool = [
                    "Understanding of basic concepts",
                    "Practical thinking ability",
                    "Problem-solving approach",
                    "Learning motivation",
                    "Technical curiosity"
                ]
                
                weaknesses_pool = [
                    f"Advanced {st.session_state.subject} concepts",
                    "Code optimization skills",
                    "Debugging techniques",
                    "Time management",
                    "Project planning"
                ]
                
                random.seed(st.session_state.score)
                st.session_state.strengths = random.sample(strengths_pool, 3)
                st.session_state.weaknesses = random.sample(weaknesses_pool, 3)
                st.session_state.diagnostic_complete = True
                
                st.session_state.current_page = "results"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Page: Results
    elif st.session_state.current_page == "results":
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown("## 📊 Your Diagnostic Results")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score", f"{st.session_state.score}%")
        with col2:
            assessed = "Advanced" if st.session_state.score > 80 else "Intermediate" if st.session_state.score > 60 else "Beginner"
            st.metric("Assessed Level", assessed)
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
        st.markdown("### 🎯 AI Recommendations")
        st.markdown(f"• Practice {st.session_state.weaknesses[0]} daily")
        st.markdown(f"• Build a project using {st.session_state.subject}")
        st.markdown("• Take weekly quizzes to track progress")
        st.markdown("• Engage with the AI tutor for difficult concepts")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗺️ View Learning Path", use_container_width=True):
                st.session_state.current_page = "path"
                st.rerun()
        with col2:
            if st.button("💬 Chat with AI Tutor", use_container_width=True):
                st.session_state.current_page = "tutor"
                st.rerun()
    
    # Page: Learning Path
    elif st.session_state.current_page == "path":
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown("## 🗺️ Your Personalized Learning Path")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Generate learning path based on level
        if st.session_state.level == "Beginner":
            weeks = 6
            milestones = [
                {"week": 1, "title": f"{st.session_state.subject} Fundamentals", "hours": 10, "topics": ["Basic concepts", "Syntax", "Setup"]},
                {"week": 2, "title": "Core Programming Concepts", "hours": 12, "topics": ["Variables", "Loops", "Functions"]},
                {"week": 3, "title": "Data Structures", "hours": 15, "topics": ["Lists", "Dictionaries", "Sets"]},
                {"week": 4, "title": "Problem Solving", "hours": 15, "topics": ["Algorithms", "Practice problems"]},
                {"week": 5, "title": "Mini Project", "hours": 20, "topics": ["Project planning", "Implementation"]},
                {"week": 6, "title": "Review & Assessment", "hours": 10, "topics": ["Revision", "Final test"]}
            ]
        elif st.session_state.level == "Intermediate":
            weeks = 6
            milestones = [
                {"week": 1, "title": "Advanced Concepts", "hours": 12, "topics": ["Advanced topics", "Best practices"]},
                {"week": 2, "title": f"Mastering {st.session_state.weaknesses[0]}", "hours": 15, "topics": ["Deep dive", "Practice"]},
                {"week": 3, "title": "Optimization Techniques", "hours": 12, "topics": ["Performance", "Efficiency"]},
                {"week": 4, "title": "Real-world Applications", "hours": 15, "topics": ["Case studies", "Projects"]},
                {"week": 5, "title": "Portfolio Project", "hours": 20, "topics": ["Build", "Document"]},
                {"week": 6, "title": "Interview Preparation", "hours": 10, "topics": ["Mock interviews", "Review"]}
            ]
        else:
            weeks = 8
            milestones = [
                {"week": 1, "title": "System Design", "hours": 15, "topics": ["Architecture", "Design patterns"]},
                {"week": 2, "title": "Advanced Optimization", "hours": 15, "topics": ["Performance tuning"]},
                {"week": 3, "title": f"Mastering {st.session_state.weaknesses[0]}", "hours": 20, "topics": ["Expert level"]},
                {"week": 4, "title": "Complex Projects", "hours": 20, "topics": ["Real-world challenges"]},
                {"week": 5, "title": "Teaching Others", "hours": 10, "topics": ["Mentoring", "Content creation"]},
                {"week": 6, "title": "Open Source Contribution", "hours": 15, "topics": ["GitHub", "Collaboration"]},
                {"week": 7, "title": "Portfolio Enhancement", "hours": 15, "topics": ["Showcase", "Networking"]},
                {"week": 8, "title": "Career Preparation", "hours": 10, "topics": ["Resume", "Interviews"]}
            ]
        
        st.info(f"📌 **Estimated Duration:** {weeks} weeks | **Total Hours:** {sum(m['hours'] for m in milestones)} hours")
        
        for m in milestones:
            with st.expander(f"Week {m['week']}: {m['title']} (Est. {m['hours']} hours)"):
                st.markdown("**Topics to cover:**")
                for topic in m['topics']:
                    st.markdown(f"• {topic}")
                
                if st.button(f"✅ Mark Week {m['week']} Complete", key=f"week_{m['week']}"):
                    st.success(f"🎉 Great progress! Week {m['week']} completed!")
        
        st.markdown("---")
        
        if st.button("💬 Chat with AI Tutor", use_container_width=True):
            st.session_state.current_page = "tutor"
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Page: AI Tutor
    elif st.session_state.current_page == "tutor":
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown("## 💬 AI Tutor")
        st.markdown("Ask me anything about your subject!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Chat history
        for chat in st.session_state.chat_history:
            if chat['role'] == 'user':
                st.markdown(f'<div class="user-message"><strong>You:</strong> {chat["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message"><strong>🤖 AI Tutor:</strong> {chat["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Suggested questions
        st.markdown("### 💡 Suggested Questions")
        cols = st.columns(3)
        suggestions = [
            f"Explain {st.session_state.subject} basics",
            f"How can I improve in {st.session_state.weaknesses[0] if st.session_state.weaknesses else st.session_state.subject}?",
            "Give me a coding example",
            "What are common mistakes to avoid?",
            "Best resources to learn",
            "How to stay motivated?"
        ]
        
        for i, suggestion in enumerate(suggestions[:3]):
            with cols[i]:
                if st.button(suggestion, key=f"sugg_{i}", use_container_width=True):
                    st.session_state.chat_history.append({'role': 'user', 'content': suggestion})
                    
                    response = f"""**Thanks for your question!**

Here's what you should know about "{suggestion}" for {st.session_state.subject}:

✨ **Key Insight:** This is an important concept for {st.session_state.level} level learners.

📝 **Practical Tip:** 
- Practice for 30 minutes daily
- Break down complex problems
- Review and learn from mistakes

💡 **Pro Tip:** Consistency is more important than intensity. Small daily progress adds up!

Would you like me to elaborate on any specific part of this answer?

Keep up the great learning attitude! 🚀"""
                    
                    st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                    st.rerun()
        
        # Chat input
        user_input = st.text_input("Ask your question:", placeholder="Type your question here...")
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("Send Message", use_container_width=True):
                if user_input:
                    st.session_state.chat_history.append({'role': 'user', 'content': user_input})
                    
                    response = f"""**Great question!**

Let me help you with "{user_input}" in {st.session_state.subject}:

🎯 **Core Concept:** 
This relates to fundamental principles that every {st.session_state.level} learner should understand.

📚 **Learning Strategy:**
1. Start with the basics
2. Practice with examples
3. Apply to real problems
4. Review and refine

💪 **Motivation:** Every expert was once a beginner. You're on the right track!

Would you like me to provide a specific example or practice exercise?"""
                    
                    st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                    st.rerun()
        
        if st.button("🗑 Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Page: Quiz
    elif st.session_state.current_page == "quiz":
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown("## 📝 Knowledge Quiz")
        st.markdown("Test your understanding!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        if not st.session_state.quiz_taken:
            questions = [
                {
                    "text": f"What is the first step in mastering {st.session_state.subject}?",
                    "options": ["Understanding core concepts", "Memorizing syntax", "Building complex projects", "Reading documentation"]
                },
                {
                    "text": f"Which practice is most effective for learning {st.session_state.subject}?",
                    "options": ["Daily coding practice", "Only watching tutorials", "Reading books only", "Memorizing examples"]
                },
                {
                    "text": f"How can you improve in {st.session_state.weaknesses[0] if st.session_state.weaknesses else st.session_state.subject}?",
                    "options": ["Regular practice", "Ignoring difficult topics", "Only theory", "Memorization"]
                }
            ]
            
            answers = {}
            for i, q in enumerate(questions):
                st.markdown(f"**Q{i+1}: {q['text']}**")
                answer = st.radio("Select your answer:", q['options'], key=f"quiz_{i}", index=None)
                answers[i] = answer
                st.markdown("---")
            
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("✅ Submit Quiz", use_container_width=True):
                    correct = 0
                    for i, ans in answers.items():
                        if ans and ans == questions[i]['options'][0]:
                            correct += 1
                    
                    st.session_state.quiz_score = (correct / len(questions)) * 100
                    st.session_state.quiz_taken = True
                    st.rerun()
        
        else:
            # Show results
            if st.session_state.quiz_score >= 70:
                st.success(f"🎉 Excellent work! You scored {st.session_state.quiz_score:.0f}%!")
            elif st.session_state.quiz_score >= 50:
                st.info(f"👍 Good effort! You scored {st.session_state.quiz_score:.0f}%. Keep practicing!")
            else:
                st.warning(f"💪 You scored {st.session_state.quiz_score:.0f}%. Review the material and try again!")
            
            st.markdown("### 📊 Detailed Results")
            st.progress(st.session_state.quiz_score / 100)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Take Another Quiz", use_container_width=True):
                    st.session_state.quiz_taken = False
                    st.rerun()
            with col2:
                if st.button("💬 Ask AI Tutor", use_container_width=True):
                    st.session_state.current_page = "tutor"
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🎓 AI Mentor - Your Personalized Learning Assistant | Made with ❤️ for lifelong learners</p>
</div>
""", unsafe_allow_html=True)
