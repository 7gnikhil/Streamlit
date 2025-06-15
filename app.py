import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
import requests  # For GitLab API calls
from datetime import datetime  # For timestamping attempts
import os  # Import os to access environment variables
from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# --- 0. STYLING ---
# (You'll need to create/update 'style.css' in the same directory)
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file '{file_name}' not found. Some styling will be missing. Please create it.")

# --- 1. QUIZ CONTENT (QUESTIONS DB) ---
QUESTIONS_DB = [
    # Low Difficulty (5 questions)
    {
        "id": 1, "topic": "Git Basics", "difficulty": "Low",
        "text": "What is the command to initialize a new Git repository in the current directory?",
        "options": ["git start", "git init", "git new", "git create repo"], "correct_answer": "git init",
        "explanation": "The `git init` command creates a new Git repository. It can be used to convert an existing, unversioned project to a Git repository or initialize a new, empty repository.",
        "resource_link": "https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository"
    },
    {
        "id": 2, "topic": "Git Basics", "difficulty": "Low",
        "text": "Which command stages changes (adds them to the staging area) for the next commit?",
        "options": ["git commit -m 'message'", "git push", "git add <file>", "git status"], "correct_answer": "git add <file>",
        "explanation": "`git add <file>` adds changes in the working directory to the staging area. You can also use `git add .` to stage all changes.",
        "resource_link": "https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository#_tracking_new_files"
    },
    {
        "id": 3, "topic": "Cloning", "difficulty": "Low",
        "text": "What command do you use to download a copy of a remote repository (e.g., from GitLab) to your local machine?",
        "options": ["git pull", "git fetch", "git clone <repository_url>", "git download <repository_url>"], "correct_answer": "git clone <repository_url>",
        "explanation": "`git clone <repository_url>` is used to create a local copy of an existing remote repository. It also sets up tracking for the remote branches.",
        "resource_link": "https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository#_cloning_an_existing_repository"
    },
    {
        "id": 4, "topic": "Committing", "difficulty": "Low",
        "text": "Which command is used to save your staged changes to the local repository history with a descriptive message?",
        "options": ["git save 'message'", "git commit -m 'message'", "git store 'message'", "git log 'message'"], "correct_answer": "git commit -m 'message'",
        "explanation": "`git commit -m 'message'` records snapshots of your project to the commit history. The `-m` flag allows you to provide a commit message directly.",
        "resource_link": "https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository#_committing_your_changes"
    },
    {
        "id": 5, "topic": "Git Log", "difficulty": "Low",
        "text": "Which command allows you to view the commit history of your repository?",
        "options": ["git history", "git show commits", "git log", "git list history"], "correct_answer": "git log",
        "explanation": "`git log` is used to view the commit history of a repository, showing commit hashes, authors, dates, and messages.",
        "resource_link": "https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History"
    },
    # Medium Difficulty (5 questions)
    {
        "id": 6, "topic": "Branching", "difficulty": "Medium",
        "text": "What is the command to create a new branch named 'feature-xyz' AND switch to it in one step?",
        "options": ["git branch feature-xyz && git switch feature-xyz", "git new-branch feature-xyz", "git checkout -b feature-xyz", "git create-and-switch feature-xyz"], "correct_answer": "git checkout -b feature-xyz",
        "explanation": "`git checkout -b <branchname>` is a shortcut command that creates a new branch and immediately switches you to it. It's equivalent to running `git branch <branchname>` followed by `git checkout <branchname>` (or `git switch <branchname>`).",
        "resource_link": "https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging#_basic_branching"
    },
    {
        "id": 7, "topic": "GitLab CI/CD", "difficulty": "Medium",
        "text": "In GitLab CI/CD, which file, typically located in the root of your repository, defines the CI/CD pipeline configuration?",
        "options": ["pipeline.yml", ".gitlab-ci.yml", "config.yml", "ci-config.yaml"], "correct_answer": ".gitlab-ci.yml",
        "explanation": "GitLab CI/CD pipelines are configured using a YAML file named `.gitlab-ci.yml` located in the root directory of your repository.",
        "resource_link": "https://docs.gitlab.com/ee/ci/yaml/"
    },
    {
        "id": 8, "topic": "Remote Repositories", "difficulty": "Medium",
        "text": "How do you send your locally committed changes from your current branch to a remote repository (e.g., 'origin') and its corresponding branch (e.g., 'main')?",
        "options": ["git send origin main", "git upload origin main", "git push origin main", "git sync origin main"], "correct_answer": "git push origin main",
        "explanation": "`git push <remote_name> <branch_name>` (e.g., `git push origin main`) uploads local branch commits to the specified remote repository branch.",
        "resource_link": "https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes#_pushing_to_your_remotes"
    },
    {
        "id": 9, "topic": "Merging", "difficulty": "Medium",
        "text": "What Git command is used to integrate changes from one branch (e.g., 'feature-branch') into your currently active branch (e.g., 'main')?",
        "options": ["git combine feature-branch", "git attach feature-branch", "git merge feature-branch", "git update-from feature-branch"], "correct_answer": "git merge feature-branch",
        "explanation": "`git merge <branch_name>` joins two or more development histories together. Typically, you merge a feature branch into your main branch.",
        "resource_link": "https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging"
    },
    {
        "id": 10, "topic": "Git Stash", "difficulty": "Medium",
        "text": "You have uncommitted changes in your working directory, but you need to switch branches quickly. What Git command temporarily shelves your changes so you can re-apply them later?",
        "options": ["git save-changes", "git hold-work", "git stash", "git pause-work"], "correct_answer": "git stash",
        "explanation": "`git stash` takes your uncommitted changes (both staged and unstaged), saves them away for later use, and then reverts them from your working copy, leaving it clean. You can re-apply them later with `git stash pop`.",
        "resource_link": "https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning"
    },
    # High Difficulty (5 questions)
    {
        "id": 11, "topic": "Rebasing", "difficulty": "High",
        "text": "What is a primary difference in outcome between `git merge` and `git rebase` when integrating changes from one branch to another?",
        "options": [
            "`git rebase` creates a merge commit, while `git merge` does not.",
            "`git rebase` rewrites commit history to create a linear sequence, while `git merge` preserves history and creates a merge commit.",
            "`git merge` is for local branches, `git rebase` for remote branches.",
            "They achieve the exact same history and outcome."
        ], "correct_answer": "`git rebase` rewrites commit history to create a linear sequence, while `git merge` preserves history and creates a merge commit.",
        "explanation": "`git rebase` re-applies commits from one branch onto the tip of another, resulting in a cleaner, linear history. `git merge` creates a new merge commit, preserving the distinct history of both branches.",
        "resource_link": "https://git-scm.com/book/en/v2/Git-Branching-Rebasing"
    },
    {
        "id": 12, "topic": "Git Fetch vs Pull", "difficulty": "High",
        "text": "Explain the core difference between `git fetch` and `git pull`.",
        "options": [
            "`git fetch` downloads remote changes and immediately integrates them, `git pull` only downloads.",
            "`git pull` downloads remote changes and immediately integrates (merges or rebases) them, `git fetch` only downloads remote changes without integration.",
            "They are functionally identical in modern Git versions.",
            "`git fetch` is for single files, `git pull` is for the entire repository."
        ], "correct_answer": "`git pull` downloads remote changes and immediately integrates (merges or rebases) them, `git fetch` only downloads remote changes without integration.",
        "explanation": "`git fetch` retrieves new data from a remote repository but doesn't integrate any of it into your working files. `git pull` is essentially `git fetch` followed by `git merge FETCH_HEAD` (or `git rebase` if configured).",
        "resource_link": "https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes#_fetching_and_pulling_from_your_remotes"
    },
    {
        "id": 13, "topic": "GitLab Merge Requests (MRs)", "difficulty": "High",
        "text": "In GitLab, before merging a Merge Request from a feature branch into 'main', what are crucial best practices to ensure code quality and stability?",
        "options": [
            "Deleting the local feature branch immediately to keep things clean.",
            "Ensuring the CI/CD pipeline for the MR passes, obtaining code reviews, and resolving discussions.",
            "Force pushing any last-minute changes directly to the feature branch to update the MR quickly.",
            "Merging 'main' back into the feature branch without running tests again."
        ], "correct_answer": "Ensuring the CI/CD pipeline for the MR passes, obtaining code reviews, and resolving discussions.",
        "explanation": "Before merging, it's critical that automated tests (CI pipeline) pass, at least one other person has reviewed the code for quality and correctness, and all review comments/discussions are resolved.",
        "resource_link": "https://docs.gitlab.com/ee/user/project/merge_requests/reviews/"
    },
    {
        "id": 14, "topic": "Undoing Changes", "difficulty": "High",
        "text": "You've accidentally committed sensitive data and pushed it to a remote repository. Which Git command (used with extreme caution and coordination) is part of a strategy to remove this commit from the *shared* remote history, as opposed to just undoing its changes with a new commit?",
        "options": [
            "`git revert <commit_hash>` then `git push`",
            "`git reset --hard HEAD~1` (locally) then `git push --force` (to remote)",
            "Deleting the repository on GitLab and re-uploading without the bad commit.",
            "Editing the commit message via the GitLab UI."
        ], "correct_answer": "`git reset --hard HEAD~1` (locally) then `git push --force` (to remote)",
        "explanation": "To remove a commit from shared history (dangerous, rewrites history), you would `git reset` locally to move the branch pointer before the bad commit, then `git push --force`. `git revert` creates a *new* commit that undoes the changes, but the original bad commit remains in history. For thorough cleaning of sensitive data, tools like `git filter-repo` or BFG Repo-Cleaner are recommended.",
        "resource_link": "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository"
    },
    {
        "id": 15, "topic": "Git Tags", "difficulty": "Medium",
        "text": "What is the primary purpose of using `git tag`?",
        "options": [
            "To temporarily save changes like `git stash`.",
            "To mark specific points in a repository's history as being important, typically used for releases (e.g., v1.0).",
            "To create a new branch for experimental features.",
            "To write notes or comments about a specific commit."
        ], "correct_answer": "To mark specific points in a repository's history as being important, typically used for releases (e.g., v1.0).",
        "explanation": "Git tags are used to create a permanent marker for a specific commit, often to denote a release version (like `v1.0.0`). There are lightweight tags and annotated tags (which are full Git objects).",
        "resource_link": "https://git-scm.com/book/en/v2/Git-Basics-Tagging"
    }
]

# --- HELPER FUNCTION TO GET QUIZ QUESTIONS ---
def get_quiz_questions(num_questions=15):
    difficulty_order = {"Low": 0, "Medium": 1, "High": 2}
    
    low_diff = [q for q in QUESTIONS_DB if q['difficulty'] == 'Low']
    medium_diff = [q for q in QUESTIONS_DB if q['difficulty'] == 'Medium']
    high_diff = [q for q in QUESTIONS_DB if q['difficulty'] == 'High']
    
    random.shuffle(low_diff)
    random.shuffle(medium_diff)
    random.shuffle(high_diff)
    
    num_per_difficulty = num_questions // 3
    extra = num_questions % 3
    
    selected_questions = []
    selected_questions.extend(low_diff[:num_per_difficulty + (1 if extra > 0 else 0)])
    selected_questions.extend(medium_diff[:num_per_difficulty + (1 if extra > 1 else 0)])
    selected_questions.extend(high_diff[:num_per_difficulty])
    
    final_questions = selected_questions[:num_questions]
    random.shuffle(final_questions) 
    return final_questions

# --- GITLAB API FUNCTION---
@st.cache_data(ttl=300) # Cache for 5 minutes
def fetch_gitlab_user_by_username(username: str):
    """Fetches a user's details from GitLab API by username.
    Prioritizes st.secrets, then falls back to environment variables."""

    gitlab_url_from_secrets = None
    pat_from_secrets = None

    try:
        # This is the part that can raise StreamlitSecretNotFoundError if secrets.toml is missing
        # We attempt to get the values. If the file is missing, the error will be caught.
        # If the file exists but keys are missing, .get() will return None.
        gitlab_url_from_secrets = st.secrets.get("GITLAB_URL")
        pat_from_secrets = st.secrets.get("GITLAB_PAT")
    except st.errors.StreamlitAPIException as e: # More general Streamlit API exception
        # This can catch issues if st.secrets itself is not properly initialized
        # but often StreamlitSecretNotFoundError is the primary one for missing files.
        st.warning(f"Note: Could not access Streamlit secrets (API Exception): {e}. Will try .env file.")
        # Variables will remain None
    except Exception as e: # Catch any other unexpected error during secrets access
        # This is a broader catch. StreamlitSecretNotFoundError *should* be caught by the above
        # or be a subclass of StreamlitAPIException for some versions.
        # For robustness, we check the error message if it's a generic Exception.
        if "StreamlitSecretNotFoundError" in str(type(e).__name__) or "No secrets found" in str(e):
             st.info("Note: Streamlit secrets file not found. Will try .env file.")
        else:
            st.warning(f"Note: An unexpected error occurred while accessing Streamlit secrets: {type(e).__name__} - {e}. Will try .env file.")
        # Variables will remain None

    # Fallback to environment variables (loaded by python-dotenv from .env)
    gitlab_url_from_env = os.getenv("GITLAB_URL")
    pat_from_env = os.getenv("GITLAB_PAT")

    # Determine which source to use: Prioritize st.secrets if its values were successfully retrieved
    gitlab_url_config = gitlab_url_from_secrets if gitlab_url_from_secrets is not None else gitlab_url_from_env
    pat_config = pat_from_secrets if pat_from_secrets is not None else pat_from_env

    # Default to public gitlab.com if no URL is configured anywhere
    if gitlab_url_config is None:
        gitlab_url_config = "https://code.swecha.org/"
    gitlab_url = gitlab_url_config.rstrip('/') # Ensure no trailing slash


    if not pat_config:
        msg = "Critical: GitLab PAT not configured. Please set GITLAB_PAT in Streamlit secrets (.streamlit/secrets.toml) or in a .env file for local development."
        st.error(msg) # Show error in UI as this is critical
        return {"error": msg}

    if not username:
        return {"error": "Username cannot be empty."}

    api_url = f"{gitlab_url}/api/v4/users?username={username}"
    headers = {"PRIVATE-TOKEN": pat_config}

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        users = response.json()
        if users: # API returns a list, even for a unique username query
            return users[0] # Return the first user found
        else:
            return None # User not found
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return {"error": "Unauthorized. Check your GitLab PAT and its scopes (needs 'read_user'). Ensure it's correctly set in secrets or .env."}
        return {"error": f"GitLab API request failed: {e.response.status_code} - {e.response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error connecting to GitLab: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

# --- SESSION STATE INITIALIZATION ---
def initialize_session_state():
    # GitLab User Identification
    if "gitlab_user_input" not in st.session_state:
        st.session_state.gitlab_user_input = ""
    if "current_gitlab_user" not in st.session_state: 
        st.session_state.current_gitlab_user = None
    if "user_identification_status" not in st.session_state: 
        st.session_state.user_identification_status = "not_started"

    # Quiz specific state
    if "quiz_state" not in st.session_state: 
        st.session_state.quiz_state = "awaiting_user" 
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = []
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "selected_option_key" not in st.session_state:
        st.session_state.selected_option_key = 0
    if "submitted_answer" not in st.session_state:
        st.session_state.submitted_answer = None

    # Chat
    if "messages" not in st.session_state:
        st.session_state.messages = [] 

    # Store quiz attempts (session-based)
    if "all_quiz_attempts" not in st.session_state:
        st.session_state.all_quiz_attempts = {}

# --- QUIZ DISPLAY AND LOGIC FUNCTIONS ---
def display_question_and_feedback():
    if st.session_state.quiz_state not in ["in_progress", "feedback"]:
        return

    question_index = st.session_state.current_question_index
    if question_index >= len(st.session_state.quiz_questions):
        st.warning("Trying to display question out of bounds. Resetting quiz state.")
        st.session_state.quiz_state = "user_identified" 
        st.rerun()
        return
        
    question = st.session_state.quiz_questions[question_index]

    st.markdown(f"<div class='quiz-container'>", unsafe_allow_html=True)
    st.markdown(f"<h4>Question {question_index + 1}/{len(st.session_state.quiz_questions)} (Topic: {question['topic']}, Difficulty: {question['difficulty']})</h4>", unsafe_allow_html=True)
    st.markdown(f"<p class='question-text'>{question['text']}</p>", unsafe_allow_html=True)

    if st.session_state.quiz_state == "in_progress":
        selected_option = st.radio(
            "Your answer:",
            question["options"],
            index=None,
            key=f"q_option_{st.session_state.selected_option_key}_{question_index}" # More unique key
        )
        if st.button("Submit Answer", key=f"submit_q_{question_index}"):
            if selected_option is not None:
                st.session_state.submitted_answer = selected_option
                st.session_state.quiz_state = "feedback"
                st.rerun()
            else:
                st.warning("Please select an answer.")

    elif st.session_state.quiz_state == "feedback":
        submitted = st.session_state.submitted_answer
        is_correct = (submitted == question["correct_answer"])

        options_with_selection = question["options"]
        try:
            selected_idx = options_with_selection.index(submitted)
        except ValueError:
            selected_idx = None 
        
        st.radio(
            "Your answer was:",
            options_with_selection,
            index=selected_idx,
            key=f"q_option_feedback_{st.session_state.selected_option_key}_{question_index}", # More unique key
            disabled=True
        )

        if is_correct:
            st.success(f"Correct! 🎉")
            # Ensure score is added only once per question attempt if logic allows re-visiting feedback
            if not any(ua['question_id'] == question['id'] and ua.get('scored', False) for ua in st.session_state.user_answers):
                st.session_state.score += 1
                # Mark as scored if implementing more complex navigation
        else:
            st.error(f"Not quite. The correct answer is: {question['correct_answer']}")
        
        with st.expander("Explanation & Resources", expanded=True):
            st.markdown("<div class='explanation-box'>", unsafe_allow_html=True)
            st.markdown(f"**Explanation:** {question['explanation']}")
            if question['resource_link']:
                st.markdown(f"**Learn more:** [Resource Link]({question['resource_link']})")
            st.markdown("</div>", unsafe_allow_html=True)

        # Add to user_answers (only once per question during a quiz attempt)
        if not any(ua['question_id'] == question['id'] for ua in st.session_state.user_answers):
            st.session_state.user_answers.append({
                "question_id": question["id"],
                "question_text": question["text"],
                "selected_option": submitted,
                "correct_answer": question["correct_answer"],
                "is_correct": is_correct,
                "topic": question["topic"],
                "difficulty": question["difficulty"],
                "explanation": question["explanation"],
                "resource_link": question["resource_link"],
                "scored": is_correct # track if this answer contributed to score
            })

        if st.button("Next Question", key=f"next_q_{question_index}"):
            st.session_state.current_question_index += 1
            st.session_state.quiz_state = "in_progress"
            # st.session_state.selected_option_key += 1 # Not strictly needed if key includes question_index
            st.session_state.submitted_answer = None
            if st.session_state.current_question_index >= len(st.session_state.quiz_questions):
                st.session_state.quiz_state = "completed"
            st.rerun()
    st.markdown(f"</div>", unsafe_allow_html=True)

# --- DISPLAY RESULTS ---
def display_results():
    if not st.session_state.current_gitlab_user:
        st.error("Cannot display results. No GitLab user identified for this session.")
        # Optionally, guide user back to identification
        if st.button("Identify User"):
            st.session_state.quiz_state = "awaiting_user"
            st.rerun()
        return

    user_name = st.session_state.current_gitlab_user.get('name', 'Quiz Taker')
    st.markdown("<div class='quiz-container results-summary'>", unsafe_allow_html=True)
    st.header(f"✨ Quiz Results for {user_name} ✨")
    
    total_questions = len(st.session_state.quiz_questions)
    score = st.session_state.score
    percentage = (score / total_questions * 100) if total_questions > 0 else 0
    
    st.subheader(f"Your Score: {score}/{total_questions} ({percentage:.2f}%)")

    if percentage >= 80:
        st.balloons()
        st.success("🎉 Excellent! Great job on the Git & GitLab Quiz!")
    elif percentage >= 60:
        st.info("👍 Good effort! Review the topics below to improve further.")
    else:
        st.warning("😕 Needs improvement. Focus on the explanations and resources for the questions you missed.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")

    df_answers = pd.DataFrame(st.session_state.user_answers)
    if not df_answers.empty:
        st.subheader("📊 Performance by Topic")
        topic_performance = df_answers.groupby("topic")["is_correct"].agg(
            Correct='sum', 
            Total='count'
        ).reset_index()
        topic_performance["Percentage Correct (%)"] = (topic_performance["Correct"] / topic_performance["Total"]) * 100
        
        fig_topic = px.bar(topic_performance, x="topic", y="Percentage Correct (%)",
                           title="Your Score per Topic", labels={"Percentage Correct (%)": "Correctness (%)", "topic": "Topic"},
                           color="topic", text_auto=".0f") 
        fig_topic.update_yaxes(range=[0, 100])
        st.plotly_chart(fig_topic, use_container_width=True)

        st.subheader("📈 Performance by Difficulty")
        difficulty_performance = df_answers.groupby("difficulty")["is_correct"].agg(
            Correct='sum', 
            Total='count'
        ).reset_index()
        difficulty_performance["Percentage Correct (%)"] = (difficulty_performance["Correct"] / difficulty_performance["Total"]) * 100
        difficulty_order_cat = ["Low", "Medium", "High"]
        difficulty_performance['difficulty'] = pd.Categorical(difficulty_performance['difficulty'], categories=difficulty_order_cat, ordered=True)
        difficulty_performance = difficulty_performance.sort_values('difficulty')

        fig_difficulty = px.bar(difficulty_performance, x="difficulty", y="Percentage Correct (%)",
                                title="Your Score per Difficulty Level", labels={"Percentage Correct (%)": "Correctness (%)", "difficulty": "Difficulty"},
                                color="difficulty", color_discrete_map={"Low": "#28a745", "Medium": "#ffc107", "High": "#dc3545"},
                                text_auto=".0f")
        fig_difficulty.update_yaxes(range=[0, 100])
        st.plotly_chart(fig_difficulty, use_container_width=True)

    st.subheader("🔍 Review Your Answers")
    incorrect_answers = [ans for ans in st.session_state.user_answers if not ans["is_correct"]]
    if not incorrect_answers:
        st.success("Amazing! You got all questions correct!")
    else:
        st.warning(f"You had {len(incorrect_answers)} incorrect answer(s). Let's review them:")
        for i, ans in enumerate(incorrect_answers):
            expander_title = f"Question on '{ans['topic']}' (Difficulty: {ans['difficulty']}): {ans['question_text'][:60]}..."
            with st.expander(expander_title):
                st.markdown(f"**Your Answer:** <span class='incorrect-answer-feedback'>{ans['selected_option']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Correct Answer:** <span class='correct-answer-feedback'>{ans['correct_answer']}</span>", unsafe_allow_html=True)
                st.markdown("<div class='explanation-box'>", unsafe_allow_html=True)
                st.markdown(f"**Explanation:** {ans['explanation']}")
                if ans['resource_link']:
                    st.markdown(f"**Learn more:** [Resource Link]({ans['resource_link']})")
                st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")

    user_id = st.session_state.current_gitlab_user['id']
    if user_id not in st.session_state.all_quiz_attempts:
        st.session_state.all_quiz_attempts[user_id] = []
    
    current_attempt_data = {
        "timestamp": datetime.now().isoformat(),
        "score": score,
        "total_questions": total_questions,
        "percentage": percentage,
        "answers_details": st.session_state.user_answers 
    }
    
    # Simple check to avoid duplicate storage on refresh of results page
    last_attempt_time = None
    if st.session_state.all_quiz_attempts[user_id]:
        last_attempt_time_str = st.session_state.all_quiz_attempts[user_id][-1].get("timestamp")
        if last_attempt_time_str:
            last_attempt_time = datetime.fromisoformat(last_attempt_time_str)

    if not last_attempt_time or (datetime.now() - last_attempt_time).total_seconds() > 10: 
        st.session_state.all_quiz_attempts[user_id].append(current_attempt_data)
        st.success(f"Quiz attempt saved for {user_name} (session-based).")


    if st.button("Take Quiz Again (as same user)", key="retake_quiz"):
        st.session_state.quiz_state = "user_identified" 
        st.session_state.current_question_index = 0
        st.session_state.user_answers = []
        st.session_state.score = 0
        st.session_state.quiz_questions = [] 
        st.session_state.selected_option_key += 1000 # Make radio keys very different
        st.session_state.submitted_answer = None
        st.session_state.messages = [{"role": "assistant", "content": f"Hi {user_name}! Ready for another round?"}] # Reset chat messages
        st.rerun()

    if st.button("Identify Different User / Logout", key="logout_user"):
        # Full reset
        for key in list(st.session_state.keys()): # Iterate over a copy of keys
            if key not in ['all_quiz_attempts']: # Optionally preserve all_quiz_attempts across user logouts in the same browser session
                del st.session_state[key]
        initialize_session_state() # Re-initialize to default start
        st.rerun()

# --- MAIN APP LAYOUT ---
def main():
    st.set_page_config(layout="wide", page_title="Git & GitLab QuizBot")
    local_css("style.css") # Apply custom CSS
    initialize_session_state() # Initialize/load states

    st.markdown("<h1 style='text-align: center; color: #0056b3;'>🎓 Git & GitLab Tech Quiz 🚀</h1>", unsafe_allow_html=True)

    # --- GitLab User Identification Section ---
    if st.session_state.quiz_state == "awaiting_user":
        st.markdown("<p style='text-align: center; color: #555;'><i>Please identify yourself using your GitLab username to begin.</i></p>", unsafe_allow_html=True)
        st.markdown("---")
        
        with st.form(key="gitlab_user_form"):
            username_input_val = st.text_input("Enter your GitLab Username:", value=st.session_state.gitlab_user_input, key="gitlab_username_field")
            submit_button = st.form_submit_button(label="Find My GitLab Profile")

        if submit_button:
            if not username_input_val:
                st.warning("Please enter a GitLab username.")
                st.session_state.user_identification_status = "not_started"
            else:
                st.session_state.gitlab_user_input = username_input_val
                with st.spinner(f"Fetching profile for {username_input_val}..."):
                    user_data_fetched = fetch_gitlab_user_by_username(username_input_val)
                
                if user_data_fetched and "error" not in user_data_fetched:
                    st.session_state.current_gitlab_user = user_data_fetched
                    st.session_state.user_identification_status = "success"
                    st.session_state.quiz_state = "user_identified"
                    st.session_state.messages = [{"role": "assistant", "content": f"Hi {user_data_fetched.get('name', username_input_val)}! Ready to test your Git & GitLab knowledge?"}]
                    st.rerun()
                elif user_data_fetched and "error" in user_data_fetched:
                    st.error(f"Could not fetch profile: {user_data_fetched['error']}")
                    st.session_state.user_identification_status = "error"
                else: # User not found
                    st.error(f"GitLab user '{username_input_val}' not found. Please check the username and try again.")
                    st.session_state.user_identification_status = "error"
        
        st.caption("ℹ️ For this app to connect to GitLab, ensure `GITLAB_URL` (optional, defaults to gitlab.com) and `GITLAB_PAT` (required, with `read_user` scope) are set in `.streamlit/secrets.toml` or a local `.env` file.")

    # --- User Identified, Offer Quiz ---
    elif st.session_state.quiz_state == "user_identified":
        if st.session_state.current_gitlab_user:
            user_info_data = st.session_state.current_gitlab_user
            cols_id = st.columns([1,4]) # Using st.columns for layout
            with cols_id[0]:
                if user_info_data.get('avatar_url'):
                    st.image(user_info_data['avatar_url'], width=100, caption=user_info_data.get('name', user_info_data['username']))
            with cols_id[1]:
                st.subheader(f"Welcome, {user_info_data.get('name', user_info_data['username'])}!")
                st.markdown(f"GitLab User ID: `{user_info_data['id']}` | Username: `@{user_info_data['username']}`")
            st.markdown("---")

            # Chat-like interaction to start quiz
            chat_container = st.container(height=200) # Constrain chat height
            with chat_container:
                for message in st.session_state.messages[-5:]: # Show last few messages
                    with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
                        st.markdown(message["content"])
            
            if prompt_val := st.chat_input(f"Type 'start quiz' or 'yes' to begin, {user_info_data.get('name', 'User')}...", key=f"quiz_chat_user_identified_{st.session_state.selected_option_key}"):
                st.session_state.messages.append({"role": "user", "content": prompt_val})
                prompt_lower_val = prompt_val.lower()
                response_text = ""
                if "start" in prompt_lower_val or "yes" in prompt_lower_val:
                    st.session_state.quiz_state = "in_progress"
                    st.session_state.quiz_questions = get_quiz_questions(15)
                    st.session_state.current_question_index = 0
                    st.session_state.user_answers = [] 
                    st.session_state.score = 0         
                    st.session_state.selected_option_key += 1 # To refresh chat input if needed
                    st.session_state.submitted_answer = None
                    response_text = "Great! Starting the quiz now. Answer the questions as they appear below."
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                else:
                    response_text = "Okay, let me know when you're ready to start the quiz!"
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                st.rerun()
            
            user_id_attempts = st.session_state.current_gitlab_user['id']
            if user_id_attempts in st.session_state.all_quiz_attempts and st.session_state.all_quiz_attempts[user_id_attempts]:
                with st.expander("View Your Past Quiz Attempts (This Session)"):
                    for i, attempt_item in enumerate(st.session_state.all_quiz_attempts[user_id_attempts]):
                        dt_object_item = datetime.fromisoformat(attempt_item['timestamp'])
                        formatted_time_item = dt_object_item.strftime("%Y-%m-%d %H:%M:%S")
                        st.write(f"Attempt {i+1} on {formatted_time_item}: Score {attempt_item['score']}/{attempt_item['total_questions']} ({attempt_item['percentage']:.2f}%)")

    # --- Quiz In Progress or Feedback ---
    elif st.session_state.quiz_state in ["in_progress", "feedback"]:
        if not st.session_state.quiz_questions:
            st.warning("Quiz questions not loaded. Please try starting the quiz again.")
            st.session_state.quiz_state = "user_identified" 
            st.rerun()
        else:
            display_question_and_feedback()

    # --- Quiz Completed ---
    elif st.session_state.quiz_state == "completed":
        display_results()

    else: 
        st.error("Invalid application state. Resetting.")
        # Full reset to avoid loops
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        initialize_session_state()
        st.rerun()

if __name__ == "__main__":
    main()