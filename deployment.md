# Streamlit Cloud Deployment Guide

This guide outlines the steps to deploy your Mutual Fund FAQ Assistant (RAG Chatbot) to the free **Streamlit Community Cloud**.

> [!IMPORTANT]
> Do **NOT** upload your `.env` file or commit your `GROQ_API_KEY` directly into your code. You will configure the API key securely through the Streamlit Cloud dashboard.

## Step 1: Prepare Your Repository

1. **Create a `.gitignore` file** (if you don't have one) in your project root to ensure sensitive and heavy files aren't uploaded to GitHub:
   ```text
   .env
   __pycache__/
   venv/
   chroma_db/
   ```
   *(Note: For this specific deployment, we are excluding `chroma_db/` because Streamlit Cloud provides an ephemeral filesystem. If your vector database is small and you want to bundle it, you can remove `chroma_db/` from the `.gitignore` to deploy the offline corpus directly with your app. Otherwise, `ingest.py` must run on startup or on a separate pipeline).*

2. **Push to GitHub**:
   Initialize a git repository, commit your files, and push them to a public or private repository on your GitHub account.
   ```bash
   git init
   git add .
   git commit -m "Initial commit of FAQ Assistant"
   git branch -M main
   git remote add origin https://github.com/your-username/your-repo-name.git
   git push -u origin main
   ```

## Step 2: Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in using your GitHub account.
2. Click the **"New app"** button.
3. Select the GitHub repository you just created.
4. Set the **Branch** to `main`.
5. Set the **Main file path** to `app.py`.
6. **Do NOT click "Deploy" yet.**

## Step 3: Configure Secrets

Because we didn't push the `.env` file, the app needs to know your Groq API key to function.

1. Click on **"Advanced settings..."** (below the Main file path input).
2. Look for the **Secrets** section.
3. Enter your Groq API Key exactly as you had it in your `.env` file:
   ```toml
   GROQ_API_KEY="your-groq-api-key-here"
   ```
4. Click **Save**.

## Step 4: Deploy and Test

1. Click the **"Deploy!"** button.
2. Streamlit will now read your `requirements.txt`, install all the packages, and boot up your `app.py`.
3. This process usually takes 1-3 minutes. You can monitor the progress by clicking the "Manage app" menu in the bottom right corner of the screen to view the terminal logs.
4. Once loaded, your Mutual Fund FAQ Assistant will be live on the internet! 

## Note on Data Ingestion & ChromaDB
If you excluded `chroma_db` from Git:
Because Streamlit Cloud instances sleep after periods of inactivity and have ephemeral storage, your local `chroma_db` will not exist on the cloud container unless you commit it. 

**Recommended Approach for Streamlit Cloud:**
Remove `chroma_db/` from your `.gitignore` and push the generated `chroma_db` directory to GitHub along with your code. Since it's a lightweight facts database containing only 5 documents, bundling it into the repo ensures the `Retriever` can access it instantly on Streamlit without having to scrape Groww every time the app wakes up.
