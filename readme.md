# **Social Media Engagement Analytics Module**

## **Objective**
Develop a basic analytics module utilizing **Langflow** and **DataStax Astra DB** to analyze engagement data from mock social media accounts. This project demonstrates how workflow automation, database operations, and GPT integration can provide valuable insights into social media post performance.

---
*Demo Link* : https://youtu.be/a1oZvDuiCqU
*Deployed Link* : https://analyzesocmed.streamlit.app/
---

## **Team Members**
- **Ayushman Saha**  
- **Bijinepalli Surat Dhani**  
- **Divya Sharma**  
- **Keya Sinha**

---

## **Project Overview**
This project analyzes engagement data from simulated social media accounts. It utilizes:
- **Langflow** for creating workflows and integrating GPT.
- **DataStax Astra DB** for storing and querying engagement data.

The solution provides insights into post performance across different formats like Images, Link and Videos.

---

## **Features**

### 1. **Data Management**  
- Users can upload a CSV file containing mock social media engagement data (e.g., likes, shares, comments, post types).  
- The app processes and previews the uploaded file with:  
  - A **data sample preview**.  
  - **Statistics** of numeric and text columns.  
  - **Missing values** information.  
- Users can upload the processed data to **DataStax Astra DB** by providing:  
  - Astra DB API endpoint.  
  - Database collection name.  
  - Astra DB application token.  

### 2. **Data Transformation**  
- The uploaded data is converted into a JSON format compatible with Astra DB.  
- Automatic processing of specific columns, such as:  
  - Mapping **ages** into categories (e.g., Child, Teenager, Adult, Senior Adult).  
  - Mapping **times** into time periods (e.g., morning, evening).  
  - Simplifying **descriptions** for better analysis.  

### 3. **Chat-Based Analysis**  
- A **chat interface** allows users to input queries for engagement analysis.  
- The app sends queries to **Langflow**, which uses:  
  - **Astra DB** to retrieve relevant data.  
  - **GPT** to analyze the data and generate simple insights.  
- Example insights include:  
  - Average likes, shares, and comments per post type.  
  - Comparison of performance between post types (e.g., reels vs. static posts).  

### 4. **Clear Chat History**  
- Users can clear the chat history and reset the session using the provided button in the app.

---

## **Tools Used**
- **Langflow**  
  - To create workflows and integrate GPT for generating insights.  
- **DataStax Astra DB**  
  - For database operations such as storing and querying the engagement dataset.  
- **Streamlit**  
  - To build the user interface for chat-based analysis and data management.  

---

## **Setup Instructions**

### Steps
1. Clone the repository:  
   ```bash
   git clone <repository_url>
   cd social-media-engagement-analytics
   ```

2. Install the required Python dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. **DataStax Astra DB Setup**:
   - Create an Astra DB instance.
   - Upload the mock dataset to the database.
   - Retrieve the database API key and endpoint.

4. **Langflow Workflow Setup**:
   - Create a Langflow workflow that accepts post types as input and queries Astra DB for engagement metrics.
   - Integrate GPT to generate insights from the queried data.

5. Run the Streamlit app:
   ```bash
   streamlit run streamlit.py
   ```

---

## **Dataset**

This dataset contains various metrics related to social media posts across different platforms. Each row represents a single post with the following columns:

- **platform**: The social media platform where the post was made (e.g., Facebook, Twitter, Instagram).
- **post_type**: The type of the post (e.g., text, image, video).
- **post_content**: The content of the post, which could include text, links, or media.
- **post_timestamp**: The timestamp when the post was published.
- **likes**: The number of likes the post received.
- **comments**: The number of comments on the post.
- **shares**: The number of times the post was shared.
- **impressions**: The total number of times the post was displayed to users.
- **reach**: The total number of unique users who saw the post.
- **engagement_rate**: The rate of engagement, typically calculated as (likes + comments + shares) / impressions.
- **audience_age**: The age range of the audience that interacted with the post.
- **sentiment**: The sentiment of the post content or comments, usually categorized as positive, neutral, or negative.
- **description**: A brief description or additional context about the post.
---

## **Example Outputs**
1. Trends:
The top-performing post type based on metrics is Video, with an average engagement rate of 45.04%, followed closely by Image at 44.26% and Link at 43.79%.

2. Insights:
The overall average engagement rate across all post types is 44.35%.
The database output indicates that all posts are Links targeted at adults or middle-aged audiences, but they lack sentiment data.
3. Recommendation:
To identify the "top post," consider focusing on Video content, as it generally yields the highest engagement. However, since the specific posts listed are Links, it may be beneficial to enhance these posts with engaging visuals or videos to improve performance.

---


