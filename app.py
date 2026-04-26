import streamlit as st
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Mentor - Personalized Learning Assistant",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main-header {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .section-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'subject' not in st.session_state:
    st.session_state.subject = ""
if 'level' not in st.session_state:
    st.session_state.level = "Beginner"
if 'diagnostic_answers' not in st.session_state:
    st.session_state.diagnostic_answers = {}
if 'evaluation' not in st.session_state:
    st.session_state.evaluation = None
if 'learning_path' not in st.session_state:
    st.session_state.learning_path = None
if 'completed_milestones' not in st.session_state:
    st.session_state.completed_milestones = []
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
if 'current_page' not in st.session_state:
    st.session_state.current_page = "login"

# ============================================
# AI FUNCTIONS (No external APIs needed)
# ============================================

def generate_diagnostic_questions(subject, level):
    questions = [
        {
            "id": 1,
            "question": f"What is the most fundamental concept in {subject} that a {level} level learner should master?",
            "hint": "Think about the core building blocks and foundations"
        },
        {
            "id": 2,
            "question": f"Describe a real-world project where you would use {subject}. Explain why it's suitable.",
            "hint": "Connect theoretical concepts to practical applications"
        },
        {
            "id": 3,
            "question": f"What specific topics in {subject} do you find most challenging? Why?",
            "hint": "Be honest about your difficulties - this helps personalize your learning"
        },
        {
            "id": 4,
            "question": f"Explain {subject} in simple terms to someone with no technical background.",
            "hint": "Use analogies and simple language"
        },
        {
            "id": 5,
            "question": "What are your career goals and how does learning this subject help achieve them?",
            "hint": "This helps us tailor the learning path to your aspirations"
        }
    ]
    return questions

def evaluate_diagnostic(subject, level, answers):
    # Calculate score based on answer quality
    total_score = 0
    for answer in answers.values():
        if answer:
            length_score = min(len(answer) / 100, 1.0) * 20
            total_score += length_score
        else:
            total_score += 5
    
    score = min(int((total_score / len(answers)) * 1.5) + 60, 95)
    
    strengths = [
        "Fundamental concept understanding",
        "Practical problem-solving approach",
        "Logical thinking and reasoning",
        "Willingness to learn new concepts",
        "Ability to explain technical concepts"
    ][:3]
    
    weaknesses = [
        f"Advanced {subject} concepts",
        "Code optimization and efficiency",
        "Error handling and debugging",
        f"Practical implementation of {subject}"
    ][:3]
    
    recommendations = [
        f"Practice daily coding exercises in {subject}",
        f"Build a complete project using {subject}",
        "Review fundamentals and strengthen basics",
        "Take more quizzes to test knowledge"
    ][:3]
    
    assessed_level = level
    if score >= 85 and level == "Beginner":
        assessed_level = "Intermediate"
    elif score >= 85 and level == "Intermediate":
        assessed_level = "Advanced"
    elif score <= 65 and level == "Advanced":
        assessed_level = "Intermediate"
    elif score <= 65 and level == "Intermediate":
        assessed_level = "Beginner"
    
    return {
        "score": score,
        "assessedLevel": assessed_level,
        "summary": f"You have a {'strong' if score >= 80 else 'good'} understanding of {subject}.",
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations
    }

def generate_learning_path(subject, level, weaknesses):
    milestones = [
        {"id": 1, "title": f"{subject} Fundamentals", "description": f"Master the core concepts of {subject}", "difficulty": "Beginner", "hours": 10, "topics": ["Core Concepts", "Basic Syntax", "Foundations"]},
        {"id": 2, "title": "Practical Applications", "description": "Apply concepts to real-world problems", "difficulty": "Intermediate", "hours": 12, "topics": ["Problem Solving", "Projects", "Case Studies"]},
        {"id": 3, "title": "Advanced Topics", "description": "Deep dive into complex concepts", "difficulty": "Advanced", "hours": 15, "topics": ["Optimization", "Best Practices", "Advanced Patterns"]}
    ]
    
    total_hours = sum(m["hours"] for m in milestones)
    total_weeks = max(4, total_hours // 10)
    
    return {
        "overview": f"Your personalized {level} level journey through {subject}.",
        "totalWeeks": total_weeks,
        "totalHours": total_hours,
        "milestones": milestones
    }

def ai_tutor_response(user_question, subject, level):
    question_lower = user_question.lower()
    
    if any(word in question_lower for word in ["explain", "what is", "define"]):
        return f"""**Here's an explanation about {subject}:**

In simple terms, {subject} is a fundamental area of computer science.

**Key Points:**
• Start with the basics - don't rush
• Practice with small examples daily
• Relate concepts to real-world scenarios

Would you like me to provide more specific examples?"""

    elif any(word in question_lower for word in ["example", "show"]):
        return f"""**Practical Example for {subject}:**

**Scenario:** Building a simple application to demonstrate concepts

**Step-by-step implementation:**
1. First, understand the requirements
2. Break down the problem into smaller parts  
3. Implement each part gradually
4. Test and refine your solution

**Next step:** Try modifying this code with different inputs!"""

    elif any(word in question_lower for word in ["mistake", "error", "common"]):
        return f"""**Common Mistakes to Avoid:**

**❌ Don't do these:**
• Rushing through fundamentals without practice
• Skipping debugging and error handling
• Only reading without hands-on coding

**✅ Instead, try these strategies:**
• Code for at least 30 minutes daily
• Break complex problems into smaller steps
• Learn from errors - they're learning opportunities"""

    else:
        return f"""**Great question about {user_question}!**

**Core Concept:**
This involves understanding how different components work together in {subject}.

**Practical Tip:**
Try breaking down this concept into smaller, manageable parts.

**Remember:** Every expert was once a beginner. Keep asking questions!

Would you like me to give you a practice exercise related to this topic?"""

def generate_quiz(subject, weaknesses):
    questions = [
        {
            "id": 1,
            "question": f"What is the most important first step when learning {subject}?",
            "options": ["Understanding core concepts", "Memorizing syntax", "Building projects", "Reading docs"],
            "correct": "Understanding core concepts",
            "explanation": "Understanding core concepts provides a foundation for everything else!"
        },
        {
            "id": 2,
            "question": f"Which practice is most effective for mastering {subject}?",
            "options": ["Daily coding", "Only reading", "Watching videos", "Memorization"],
            "correct": "Daily coding",
            "explanation": "Active practice and building projects reinforce learning much better!"
        },
        {
            "id": 3,
            "question": "What is your main learning goal?",
            "options": None,
            "correct": None,
            "explanation": "Having clear goals helps guide your learning journey!"
        }
    ]
    return questions

def grade_quiz(questions, answers):
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
            "user_answer": user_answer,
            "correct": is_correct,
            "explanation": q.get('explanation', "Keep practicing!")
        })
    
    percentage = (correct / len(questions)) * 100 if questions else 0
    
    return {
        "score": correct,
        "total": len(questions),
        "percentage": percentage,
        "results": results
    }

# ============================================
# LOGIN PAGE
# ============================================

if st.session_state.current_page == "login":
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown("# 🎓 AI Mentor")
        st.markdown("## Your Personalized Learning Assistant")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### Welcome! 👋")
        
        name = st.text_input("Enter your name to begin:", placeholder="Your name")
        
        if st.button("🚀 Start Learning Journey", use_container_width=True):
            if name:
                st.session_state.user_name = name
                st.session_state.logged_in = True
                st.session_state.current_page = "setup"
                st.rerun()
            else:
                st.warning("Please enter your name to continue!")
        
        st.markdown("</div>", unsafe_allow_html=True)

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
        
        if st.button("🗺️ Learning Path", use_container_width=True):
            if st.session_state.evaluation:
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
            if st.session_state.evaluation:
                st.session_state.current_page = "quiz"
                st.rerun()
            else:
                st.error("Please complete diagnostic test first!")
        
        st.markdown("---")
        
        # Progress metrics
        if st.session_state.evaluation:
            st.markdown("### 📊 Your Progress")
            st.metric("Diagnostic Score", f"{st.session_state.evaluation['score']}%")
            st.metric("Level", st.session_state.evaluation['assessedLevel'])
            st.metric("Tutor Sessions", st.session_state.tutor_sessions)
            st.metric("Quizzes Taken", len(st.session_state.quiz_history))
        
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Page: Setup
    if st.session_state.current_page == "setup":
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("## 🎯 Learning Setup")
        
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
        
        st.text_area("Topics you're interested in (optional)", placeholder="e.g., data structures, algorithms, web development...")
        st.text_input("Your learning goal (optional)", placeholder="e.g., Prepare for technical interviews, build projects...")
        
        if st.button("🔍 Start Diagnostic Test", use_container_width=True):
            if st.session_state.subject:
                st.session_state.current_page = "diagnostic"
                st.rerun()
            else:
                st.error("Please select a subject!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Page: Diagnostic
    elif st.session_state.current_page == "diagnostic":
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("## 🧠 Diagnostic Assessment")
        st.info("Answer these questions honestly. This helps me understand your current knowledge level.")
        
        if "diagnostic_questions" not in st.session_state:
            st.session_state.diagnostic_questions = generate_diagnostic_questions(
                st.session_state.subject, st.session_state.level
            )
        
        answers = {}
        for q in st.session_state.diagnostic_questions:
            st.markdown(f"**Q{q['id']}: {q['question']}**")
            answer = st.text_area("Your answer:", key=f"diag_{q['id']}", 
                                 placeholder=f"Hint: {q['hint']}")
            answers[q['id']] = answer
            st.markdown("---")
        
        if st.button("📊 Submit & Evaluate", use_container_width=True):
            with st.spinner("🤖 AI is analyzing your responses..."):
                st.session_state.evaluation = evaluate_diagnostic(
                    st.session_state.subject, st.session_state.level, answers
                )
                st.session_state.current_page = "results"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Page: Results
    elif st.session_state.current_page == "results":
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("## 📊 Your Diagnostic Results")
        
        eval_data = st.session_state.evaluation
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score", f"{eval_data['score']}%")
        with col2:
            st.metric("Assessed Level", eval_data['assessedLevel'])
        with col3:
            st.metric("Status", "Completed ✅")
        
        st.markdown(f"**Summary:** {eval_data['summary']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**✅ Your Strengths**")
            for s in eval_data['strengths']:
                st.markdown(f"• {s}")
        with col2:
            st.markdown("**⚠️ Areas to Improve**")
            for w in eval_data['weaknesses']:
                st.markdown(f"• {w}")
        
        st.markdown("**🎯 Recommendations**")
        for r in eval_data['recommendations']:
            st.markdown(f"• {r}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗺️ Generate Learning Path", use_container_width=True):
                with st.spinner("Creating your personalized learning path..."):
                    st.session_state.learning_path = generate_learning_path(
                        st.session_state.subject, st.session_state.level, eval_data['weaknesses']
                    )
                    st.session_state.current_page = "path"
                    st.rerun()
        with col2:
            if st.button("💬 Chat with AI Tutor", use_container_width=True):
                st.session_state.current_page = "tutor"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Page: Learning Path
    elif st.session_state.current_page == "path":
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("## 🗺️ Your Personalized Learning Path")
        
        if st.session_state.learning_path:
            path = st.session_state.learning_path
            st.info(f"**Overview:** {path['overview']}\n\n**Duration:** {path['totalWeeks']} weeks ({path['totalHours']} hours)")
            
            for milestone in path['milestones']:
                with st.expander(f"📌 Milestone {milestone['id']}: {milestone['title']}"):
                    st.markdown(f"**Description:** {milestone['description']}")
                    st.markdown(f"**Difficulty:** {milestone['difficulty']}")
                    st.markdown(f"**Estimated Time:** {milestone['hours']} hours")
            
            if st.button("💬 Ask AI Tutor", use_container_width=True):
                st.session_state.current_page = "tutor"
                st.rerun()
        else:
            st.warning("Please generate your learning path first!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Page: AI Tutor
    elif st.session_state.current_page == "tutor":
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("## 💬 AI Tutor")
        st.info("Ask me anything about your subject!")
        
        # Chat history
        if st.session_state.chat_history:
            for chat in st.session_state.chat_history:
                if chat["role"] == "user":
                    st.markdown(f"**You:** {chat['content']}")
                else:
                    st.markdown(f"**🤖 AI Tutor:** {chat['content']}")
                st.markdown("---")
        
        # Suggested questions
        st.markdown("### 💡 Suggested Questions")
        cols = st.columns(3)
        suggestions = [
            f"Explain {st.session_state.subject} basics",
            "Give me a practical example",
            "What common mistakes should I avoid?"
        ]
        
        for i, suggestion in enumerate(suggestions):
            with cols[i]:
                if st.button(suggestion, key=f"sugg_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": suggestion})
                    response = ai_tutor_response(suggestion, st.session_state.subject, st.session_state.level)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.session_state.tutor_sessions += 1
                    st.rerun()
        
        # Chat input
        user_question = st.text_input("Ask your question:", key="user_question")
        
        if st.button("Send Message", use_container_width=True):
            if user_question:
                with st.spinner("🤖 AI is thinking..."):
                    st.session_state.chat_history.append({"role": "user", "content": user_question})
                    response = ai_tutor_response(user_question, st.session_state.subject, st.session_state.level)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.session_state.tutor_sessions += 1
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Page: Quiz
    elif st.session_state.current_page == "quiz":
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("## 📝 Knowledge Quiz")
        
        if st.button("🔄 Generate New Quiz", use_container_width=True):
            with st.spinner("Generating quiz..."):
                st.session_state.quiz_questions = generate_quiz(
                    st.session_state.subject, st.session_state.evaluation['weaknesses']
                )
                st.session_state.quiz_results = None
                st.rerun()
        
        if st.session_state.quiz_questions and not st.session_state.quiz_results:
            answers = {}
            for i, q in enumerate(st.session_state.quiz_questions):
                st.markdown(f"**Q{i+1}: {q['question']}**")
                if q.get('options'):
                    answer = st.radio("Select your answer:", q['options'], key=f"quiz_{i}")
                    answers[i] = answer
                else:
                    answer = st.text_area("Your answer:", key=f"quiz_{i}")
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
            results = st.session_state.quiz_results
            if results['percentage'] >= 60:
                st.success(f"🎉 You scored {results['percentage']:.0f}% - Great job!")
            else:
                st.warning(f"💪 You scored {results['percentage']:.0f}% - Keep practicing!")
            
            st.markdown(f"**Score:** {results['score']}/{results['total']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
