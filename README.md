# Streamlit
Improve your Git &amp; GitLab knowledge with this QuizBot. Sign in with GitLab, take a 15-question test covering various topics &amp; difficulties. See visual results, review errors, &amp; learn from detailed explanations. Your path to Git mastery!
# 🎓 Git & GitLab Tech QuizBot 🚀

A Streamlit-based interactive quiz application designed to test and improve your knowledge of Git and GitLab. It features dynamic question generation, user identification via GitLab API, detailed feedback, and performance tracking.

## ✨ Features

*   **GitLab User Identification:** Authenticates and greets users by fetching their GitLab profile (username, avatar).
*   **Dynamic Quiz Generation:**
    *   Questions categorized by difficulty (Low, Medium, High).
    *   Balanced selection of questions across difficulties for each quiz session.
*   **Interactive Quiz Interface:**
    *   Presents questions one by one.
    *   Radio button options for answers.
*   **Immediate Feedback:**
    *   Indicates if the selected answer is correct or incorrect.
    *   Provides detailed explanations for each question.
    *   Links to external resources for further learning.
*   **Scoring and Results:**
    *   Calculates and displays the final score and percentage.
    *   Visualizes performance by topic and difficulty using Plotly charts.
    *   Allows review of incorrect answers with explanations.
*   **Session-Based Attempt History:** Tracks quiz attempts for the identified user within the current browser session.
*   **Chat-like Interaction:** Uses a simple chat interface to start the quiz after user identification.
*   **Customizable Styling:** Supports a `style.css` file for custom UI enhancements.
*   **Environment Configuration:** Securely handles API keys using `.env` files for local development or Streamlit secrets for deployment.

## 🛠️ Tech Stack

*   **Frontend & Application Logic:** [Streamlit](https://streamlit.io/)
*   **Data Handling:** [Pandas](https://pandas.pydata.org/)
*   **Plotting:** [Plotly Express](https://plotly.com/python/plotly-express/)
*   **API Interaction:** [Requests](https://requests.readthedocs.io/en/latest/)
*   **Environment Variables:** [python-dotenv](https://pypi.org/project/python-dotenv/)
*   **Language:** Python 3.x

## ⚙️ Setup and Installation

### Prerequisites

*   Python 3.7+
*   pip (Python package installer)
*   A GitLab account and a Personal Access Token (PAT)

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    Create a `requirements.txt` file with the following content:
    ```txt
    streamlit
    pandas
    numpy
    plotly
    requests
    python-dotenv
    ```
    Then run:
    ```bash
    pip install -r requirements.txt
    ```
    *(Alternatively, you can generate `requirements.txt` from your active environment using `pip freeze > requirements.txt` after installing packages manually)*

4.  **Configure Environment Variables (Crucial for GitLab API):**

    You need to provide a GitLab Personal Access Token (PAT) for the application to fetch user profiles.

    *   **Create a GitLab PAT:**
        1.  Go to your GitLab profile settings: `https://gitlab.com/-/profile/personal_access_tokens` (or your self-hosted GitLab instance).
        2.  Create a new token.
        3.  Give it a name (e.g., `streamlit_quiz_bot`).
        4.  Select the **`read_user`** scope. This is the minimum required scope.
        5.  Copy the generated token. **You will not be able to see it again.**

    *   **Set up `.env` file (for local development):**
        Create a file named `.env` in the root directory of the project (same level as `app.py`). Add your PAT and optionally your GitLab instance URL (if not `gitlab.com`):
        ```env
        GITLAB_PAT="YOUR_GITLAB_PERSONAL_ACCESS_TOKEN_HERE"
        # GITLAB_URL="https://your.gitlab.instance.com/" # Optional, defaults to https://gitlab.com/
        ```
        **Important:** Add `.env` to your `.gitignore` file to prevent committing your secret token!

    *   **Streamlit Secrets (for deployment on Streamlit Cloud):**
        If deploying, create a `.streamlit/secrets.toml` file:
        ```toml
        GITLAB_PAT = "YOUR_GITLAB_PERSONAL_ACCESS_TOKEN_HERE"
        # GITLAB_URL = "https://your.gitlab.instance.com/" # Optional
        ```
        Refer to [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management) for more details.

5.  **(Optional) Custom Styling:**
    If you have a `style.css` file, ensure it's in the same directory as `app.py`.

## 🚀 Running the Application

Once the setup is complete, run the Streamlit application:

```bash
streamlit run app.py
