I.M.I.D - Interactive Media Intelligence Dashboard
Project Title and Description
The Interactive Media Intelligence Dashboard (I.M.I.D) is a powerful Python script designed to help you quickly analyze your media data. It automates the process of data cleaning, generates insightful interactive charts, and provides a clear summary of key findings. This tool is perfect for anyone looking to understand engagement trends, sentiment breakdown, and audience distribution within their media content, all from a simple CSV file!

Tech Stack
This project is built using:

Language:
Python 3.x

Core Libraries:
pandas: For efficient data manipulation and cleaning.
plotly: For creating beautiful, interactive data visualizations.

Features
CSV Data Processing: Easily reads and processes your media data from a standard CSV file.
Automated Data Cleaning:
Converts the 'Date' column to a proper date and time format.
Fills any missing 'Engagements' values with 0.
Normalizes column names for consistency (e.g., "Media Type" becomes "media_type").
Includes robust error handling for common issues like missing columns or invalid data entries.
Interactive Data Visualizations: Generates 5 distinct interactive charts saved as HTML files:
Sentiment Breakdown: A pie chart showing the distribution of positive, negative, and neutral sentiments.
Engagement Trend Over Time: A line chart illustrating how total engagements change across different dates.
Platform Engagements: A bar chart comparing total engagements received on various media platforms.
Media Type Mix: A pie chart displaying the proportion of different content types (e.g., Image, Video, Text).
Top 5 Locations by Engagements: A bar chart highlighting the geographical locations with the highest engagement.
Automated Insights: For each generated chart, the script provides 3 key insights, summarizing the most important observations from the data.
Analysis Recap: Compiles all the generated insights into a comprehensive, easy-to-read text file (.txt) for quick review and sharing.

Requirements
To run this dashboard, you'll need Python 3.x installed on your computer.

The required Python libraries are listed in the requirements.txt file and include:
pandas
plotly

Installation
Get the Files: Download or clone the project files (the Python script and requirements.txt) to a folder on your computer.
Open Terminal: Open your terminal or command prompt.
Navigate to Project Folder: Use the cd command to go into the folder where you saved the project files. For example:
cd /path/to/your/project/folder
Install Dependencies: Run the following command to install all the necessary Python libraries:
pip install -r requirements.txt
This command will automatically set up pandas and plotly for you.

Usage
Prepare Your CSV File:
Your data needs to be in a CSV (Comma Separated Values) file. This file must contain the following columns. The script is smart enough to handle different capitalization and spaces in the column names.
Date
Platform
Sentiment
Location
Engagements
Media Type
Example data.csv content:

Date,Platform,Sentiment,Location,Engagements,Media Type
2023-01-01,Twitter,Positive,Jakarta,150,Image
2023-01-01,Facebook,Neutral,Bandung,80,Text
2023-01-02,Instagram,Positive,Surabaya,300,Video
2023-01-02,Twitter,Negative,Jakarta,50,Text
2023-01-03,Facebook,Positive,Medan,200,Image
2023-01-03,Instagram,Neutral,Bandung,120,Video

Run the Script:
From your terminal or command prompt (still in the project folder), run the Python script:
python media_analysis.py

Enter CSV File Path:
The script will ask you for the path to your CSV file.
If your CSV file is in the same folder as the script, you can just type its name (e.g., data.csv).
If it's in a different folder, type the full path to the file.
Then press Enter.

Please enter the path to your CSV file (e.g., data.csv): your_file_name.csv

Output
Once the script finishes running, it will create a new folder named media_analysis_output (or charts_and_recap if you've changed the output_dir setting in the script). Inside this folder, you'll find:
Interactive HTML Charts: Five individual HTML files (like sentiment_breakdown_pie.html, engagement_trend_line.html, etc.). You can open these files directly in any web browser (like Chrome, Firefox, Edge) to explore the interactive graphs.
Analysis Recap: A text file named media_intelligence_recap.txt. This file contains a clear summary of all the key insights generated from your data analysis.

Contributing
We welcome contributions! If you have ideas for new features, improvements, or bug fixes, feel free to:
Fork the repository.
Create a new branch for your feature or fix.
Make your changes.
Submit a Pull Request with a clear description of your changes.

License
This project is open-source and available under the MIT License. This means you're free to use, modify, and distribute the code for personal or commercial purposes.

Acknowledgments
Built with great help from pandas for powerful data handling.
Visualizations made possible by the awesome Plotly library
