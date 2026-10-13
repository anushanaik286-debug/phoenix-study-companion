"""
=============================================================================
Phoenix — Your AI Study Companion
Multimodal AI Hackathon 2026 | Track D: Personalized Tutoring & Adaptive Learning
=============================================================================
Foundation Build (Task 1):
- Streamlit web interface with responsive sidebar navigation
- PDF upload and resilient text extraction using PyPDF
- Session state caching for uploaded study notes
- Transparent roadmap for upcoming AI tutoring features (Google Gemini API)
"""

import streamlit as st
import pypdf

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
# st.set_page_config must be the first Streamlit command called.
# It sets the browser tab title, favicon, and standard layout width.
st.set_page_config(
    page_title="Phoenix — Your AI Study Companion",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS STYLING
# -----------------------------------------------------------------------------
# Injecting simple CSS allows us to give Phoenix a clean, modern aesthetic
# with custom cards, badges, and soft accent colors.
st.markdown("""
<style>
    /* Main container title styling */
    .hero-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #ff5722;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #555555;
        margin-bottom: 1.5rem;
    }
    /* Card box for feature highlights */
    .feature-card {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    /* Status badges */
    .badge-planned {
        background-color: #fff3cd;
        color: #856404;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 4px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .badge-active {
        background-color: #d4edda;
        color: #155724;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 4px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
# Streamlit reruns the script on user interactions (clicks, uploads).
# st.session_state acts as memory so we don't lose extracted text when switching pages.
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = ""
if "page_count" not in st.session_state:
    st.session_state.page_count = 0


# -----------------------------------------------------------------------------
# 4. HELPER FUNCTION: PDF TEXT EXTRACTION
# -----------------------------------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from an uploaded PDF using pypdf.
    
    Handles:
    - Encrypted/password-protected PDFs
    - Zero-page or corrupted files
    - Scanned/image-only PDFs (where text extraction yields blank strings)
    
    Returns:
        tuple: (text: str, num_pages: int, warning_or_error: str or None)
    """
    try:
        reader = pypdf.PdfReader(uploaded_file)
        
        # Check if the PDF requires a password
        if reader.is_encrypted:
            return None, 0, "🔒 This PDF is encrypted or password-protected. Please upload an unprotected file."
        
        num_pages = len(reader.pages)
        if num_pages == 0:
            return None, 0, "⚠️ The uploaded PDF contains zero pages."

        extracted_text_list = []
        for i, page in enumerate(reader.pages):
            page_content = page.extract_text() or ""
            extracted_text_list.append(page_content.strip())

        full_text = "\n\n".join(extracted_text_list).strip()

        # Check if the PDF has pages but no readable digital text (scanned image)
        if not full_text:
            warning_msg = (
                "ℹ️ No selectable digital text was found in this PDF. "
                "It may contain scanned images or photos of pages. "
                "(In the next phase, multimodal Gemini will be able to read these visually!)"
            )
            return "", num_pages, warning_msg

        return full_text, num_pages, None

    except Exception as e:
        return None, 0, f"❌ An unexpected error occurred while reading the PDF: {str(e)}"


# -----------------------------------------------------------------------------
# 5. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🔥 Phoenix")
    st.caption("AI Study Companion • Hackathon 2026")
    st.write("---")
    
    # Navigation options specified in project requirements
    page = st.radio(
        "Navigation",
        ["Study Materials", "Ask Phoenix", "Practice Quiz", "Learning Progress"],
        index=0
    )
    
    st.write("---")
    # Quick status panel in sidebar to keep the user informed
    st.subheader("Document Status")
    if st.session_state.uploaded_filename:
        st.success(f"📄 **Loaded:** {st.session_state.uploaded_filename}")
        st.caption(f"Pages: {st.session_state.page_count} | Characters: {len(st.session_state.extracted_text):,}")
    else:
        st.info("No study material loaded yet.")

    st.write("---")
    st.caption("Track D: Personalized Tutoring & Adaptive Learning")


# -----------------------------------------------------------------------------
# 6. PAGE VIEWS
# -----------------------------------------------------------------------------

# =============================================================================
# VIEW 1: STUDY MATERIALS (Main Upload & Foundation Hub)
# =============================================================================
if page == "Study Materials":
    st.markdown('<div class="hero-title">Phoenix — Your AI Study Companion</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">'
        'Welcome to Phoenix! An intelligent, adaptive tutor built for the <b>Multimodal AI Hackathon 2026</b>.<br>'
        'Upload your lecture slides, notes, or textbook chapters to get started.'
        '</div>',
        unsafe_allow_html=True
    )

    # Explanation of Phoenix's core goals
    with st.expander("💡 What is Phoenix? (Click to view vision & planned features)", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🎯 The Mission:**
            Standard study tools offer one-size-fits-all flashcards. Phoenix adapts to *your* unique learning style, pacing, and knowledge gaps using Gemini's multimodal reasoning.
            """)
        with col2:
            st.markdown("""
            **🚀 Feature Roadmap:**
            1. **Study Materials** *(Active)* — Extract text from notes & PDFs.
            2. **Ask Phoenix** *(Planned)* — Socratic Q&A grounded in your notes.
            3. **Practice Quiz** *(Planned)* — Adaptive quizzes generated on demand.
            4. **Learning Progress** *(Planned)* — Track mastery & revisit weak areas.
            """)

    st.write("### 📤 Upload Study Materials")
    uploaded_file = st.file_uploader(
        "Select a PDF file (e.g., lecture slides, study guides, chapters)",
        type=["pdf"],
        help="Upload a PDF file to extract study content."
    )

    # Trigger extraction when a file is provided
    if uploaded_file is not None:
        # Check if this is a newly uploaded file or re-evaluating the current one
        if uploaded_file.name != st.session_state.uploaded_filename:
            with st.spinner(f"Extracting text from '{uploaded_file.name}'..."):
                text, pages, error_or_warning = extract_text_from_pdf(uploaded_file)
                
                if error_or_warning and text is None:
                    # Fatal error (e.g., password protected, corrupted)
                    st.error(error_or_warning)
                else:
                    # Successful read (or scanned PDF warning)
                    st.session_state.extracted_text = text or ""
                    st.session_state.uploaded_filename = uploaded_file.name
                    st.session_state.page_count = pages
                    
                    if error_or_warning:
                        st.warning(error_or_warning)
                    else:
                        st.success(f"✅ Successfully processed **{uploaded_file.name}** ({pages} pages)!")

    # Display extracted content if available in session state
    if st.session_state.extracted_text:
        st.write("---")
        st.subheader("📖 Extracted Material Overview")
        
        # Display key summary metrics
        word_count = len(st.session_state.extracted_text.split())
        char_count = len(st.session_state.extracted_text)
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Total Pages", st.session_state.page_count)
        metric_col2.metric("Estimated Words", f"{word_count:,}")
        metric_col3.metric("Total Characters", f"{char_count:,}")

        # Provide a text preview container
        st.write("#### Extracted Text Preview:")
        st.text_area(
            label="Extracted Content",
            value=st.session_state.extracted_text,
            height=300,
            help="This extracted text will be fed to Gemini for answering questions and generating quizzes."
        )

        # Clear button if the user wants to remove the uploaded document
        if st.button("🗑️ Clear Extracted Material"):
            st.session_state.extracted_text = ""
            st.session_state.uploaded_filename = ""
            st.session_state.page_count = 0
            st.rerun()

    elif not uploaded_file:
        st.info("👆 Please upload a PDF above to inspect its contents and prepare it for AI tutoring.")


# =============================================================================
# VIEW 2: ASK PHOENIX (Planned AI Tutor)
# =============================================================================
elif page == "Ask Phoenix":
    st.title("💬 Ask Phoenix")
    
    if not st.session_state.get("extracted_text"):
        st.info("Please upload a PDF in Study Materials first.")
    else:
        with st.form("ask_phoenix_form"):
            question = st.text_input(
                "Ask a question about your study material:",
                placeholder="e.g. Explain the main concept"
            )
            submitted = st.form_submit_button("Search my notes")

        if submitted:
            if not question.strip():
                st.warning("Please type a question first.")
            else:
                keywords = [
                    word.lower().strip(".,?!:;()[]{}\"'")
                    for word in question.split()
                    if len(word.strip(".,?!:;()[]{}\"'")) > 3
                ]

                text = st.session_state.extracted_text
                lines = [line.strip() for line in text.splitlines() if line.strip()]

                results = []
                for line in lines:
                    score = sum(
                        1 for word in keywords if word in line.lower()
                    )
                    if score > 0:
                        results.append((score, line))

                results.sort(key=lambda item: item[0], reverse=True)
                matches = [line for score, line in results[:5]]

                if matches:
                    st.subheader("Relevant excerpts from your notes")
                    for match in matches:
                        st.write("• " + match)
                    st.caption(
                        "This version searches your notes using keywords; "
                        "it does not generate AI explanations yet."
                    )
                else:
                    st.info(
                        "I couldn't find a matching passage. "
                        "Try using keywords from your PDF."
                    )

    st.markdown('<span class="badge-planned">🚧 Planned Feature — Coming in Next Step</span>', unsafe_allow_html=True)
    
    st.markdown("""
    Ask questions in plain English and receive clear, step-by-step explanations grounded in your uploaded study notes.
    """)

    st.write("---")
    
    if st.session_state.extracted_text:
        st.info(f"📄 Active Material: **{st.session_state.uploaded_filename}** ({len(st.session_state.extracted_text):,} characters ready for AI analysis).")
    else:
        st.warning("⚠️ No study materials uploaded yet. Go to **Study Materials** to upload a PDF first.")

    st.markdown("""
    ### 🛠️ What will be implemented here:
    - **Google Gemini API Integration**: Using Gemini 1.5 / 2.0 to ground answers directly in your study material.
    - **Socratic Tutoring Mode**: Prompts that guide you toward answers rather than just handing them out.
    - **Interactive Chat Interface**: Conversational multi-turn history with memory.
    """)
    
# =============================================================================
# VIEW 3: PRACTICE QUIZ (Planned Adaptive Testing)
# =============================================================================
elif page == "Practice Quiz":
    
    st.title("📝 Practice Quiz")

    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "quiz_history" not in st.session_state:
        st.session_state.quiz_history = []

    if not st.session_state.get("extracted_text"):
        st.info("Please upload a PDF in Study Materials first.")
    else:
        number = st.selectbox("Number of Questions", [3, 5, 8, 10])

        if st.button("Generate Practice Quiz"):
            import re
            import random

            text = st.session_state.extracted_text
            sentences = [
                s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text)
                if 8 <= len(s.split()) <= 45
            ]

            words = list(set(re.findall(r"\b[A-Za-z]{5,}\b", text)))
            random.shuffle(sentences)
            questions = []

            for sentence in sentences:
                candidates = re.findall(r"\b[A-Za-z]{5,}\b", sentence)
                if not candidates:
                    continue

                answer = random.choice(candidates)
                choices = list(set(w for w in words if w.lower() != answer.lower()))

                if len(choices) < 3:
                    continue

                question = re.sub(
                    r"\b" + re.escape(answer) + r"\b",
                    "________",
                    sentence,
                    count=1,
                    flags=re.IGNORECASE
                )

                options = random.sample(choices, 3) + [answer]
                random.shuffle(options)

                questions.append({
                    "question": question,
                    "answer": answer,
                    "options": options
                })

                if len(questions) == number:
                    break

            st.session_state.quiz_questions = questions

        if st.session_state.quiz_questions:
            st.subheader("Answer these questions")

            with st.form("practice_quiz_form"):
                answers = []

                for i, q in enumerate(st.session_state.quiz_questions):
                    st.write(f"**Q{i + 1}.** {q['question']}")
                    answers.append(
                        st.radio(
                            "Choose the missing word:",
                            q["options"],
                            key=f"answer_{i}"
                        )
                    )

                submitted = st.form_submit_button("Submit Answers")

            if submitted:
                score = sum(
                    answers[i].lower() == q["answer"].lower()
                    for i, q in enumerate(st.session_state.quiz_questions)
                )
                total = len(st.session_state.quiz_questions)

                st.success(f"Your score: {score}/{total}")

                st.session_state.quiz_history.append({
                    "score": score,
                    "total": total
                })

                for i, q in enumerate(st.session_state.quiz_questions):
                    st.write(
                        f"Q{i + 1}: Correct answer — **{q['answer']}**"
                    )



# =============================================================================
# VIEW 4: LEARNING PROGRESS (Planned Adaptive Analytics)
# =============================================================================
elif page == "Learning Progress":
    
    st.title("📊 Learning Progress")

    if "quiz_history" not in st.session_state:
        st.session_state.quiz_history = []

    history = st.session_state.quiz_history

    if not history:
        st.info("No quiz attempts yet. Complete a quiz in Practice Quiz first!")

        st.metric("Quiz Attempts", 0)
        st.metric("Quiz Accuracy", "Not available yet")
        st.metric("Questions Answered", 0)

    else:
        attempts = len(history)
        total_correct = sum(item["score"] for item in history)
        total_questions = sum(item["total"] for item in history)

        accuracy = (
            total_correct / total_questions * 100
            if total_questions else 0
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Quiz Attempts", attempts)
        col2.metric("Quiz Accuracy", f"{accuracy:.1f}%")
        col3.metric(
            "Questions Answered",
            total_questions
        )

        st.subheader("📚 Quiz History")

        for i, attempt in enumerate(reversed(history), start=1):
            st.write(
                f"**Attempt {attempts - i + 1}:** "
                f"{attempt['score']}/{attempt['total']} correct"
            )

        st.subheader("💡 Study Recommendation")

        if accuracy >= 80:
            st.success(
                "Great work! Review your notes and try a new quiz "
                "to keep practising."
            )
        elif accuracy >= 50:
            st.info(
                "Good start! Revisit the topics in your notes "
                "and practise again."
            )
        else:
            st.warning(
                "Spend some more time reviewing your PDF notes, "
                "then try another quiz."
            )

