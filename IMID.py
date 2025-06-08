import pandas as pd
import plotly.express as px
import os
from datetime import datetime

def normalize_column_name(name):
    """Normalizes column names to lowercase and replaces spaces with underscores."""
    return name.lower().replace(' ', '_')

def process_csv_data(file_path):
    """
    Processes the CSV data:
    - Converts 'Date' to datetime.
    - Fills missing 'Engagements' with 0.
    - Normalizes column names.
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty.")
        return None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

    # Normalize column names
    df.columns = [normalize_column_name(col) for col in df.columns]

    required_columns = ['date', 'platform', 'sentiment', 'location', 'engagements', 'media_type']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print(f"Error: Missing required columns: {', '.join(missing_columns)}")
        return None

    # Convert 'date' to datetime, handling errors
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    # Drop rows where date conversion failed (NaT - Not a Time)
    df.dropna(subset=['date'], inplace=True)
    if df.empty:
        print("Warning: No valid date entries found after cleaning. No charts can be generated.")
        return None

    # Fill missing 'engagements' with 0
    df['engagements'] = pd.to_numeric(df['engagements'], errors='coerce').fillna(0).astype(int)

    return df

def generate_charts_and_insights(df, output_dir="charts_and_recap"):
    """
    Generates 5 interactive Plotly charts and their insights.
    Charts are saved as HTML files, and insights are returned as a dictionary.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    insights = {}
    chart_files = []

    # --- 1. Sentiment Breakdown (Pie Chart) ---
    sentiment_counts = df['sentiment'].value_counts(dropna=False).reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    fig_sentiment = px.pie(sentiment_counts, names='Sentiment', values='Count',
                           title='Sentiment Breakdown',
                           color_discrete_sequence=px.colors.qualitative.Pastel)
    sentiment_path = os.path.join(output_dir, 'sentiment_breakdown_pie.html')
    fig_sentiment.write_html(sentiment_path)
    chart_files.append(f"Sentiment Breakdown: {sentiment_path}")

    total_sentiments = sentiment_counts['Count'].sum()
    top_sentiment = sentiment_counts.iloc[0]['Sentiment'] if not sentiment_counts.empty else 'N/A'
    top_sentiment_percentage = (sentiment_counts.iloc[0]['Count'] / total_sentiments * 100).round(2) if total_sentiments > 0 else 0
    lowest_sentiment = sentiment_counts.iloc[-1]['Sentiment'] if len(sentiment_counts) > 0 else 'N/A'

    insights['sentiment'] = [
        f"The dominant sentiment is '{top_sentiment}', accounting for {top_sentiment_percentage}% of all entries.",
        f"'{lowest_sentiment}' is the least frequent sentiment.",
        f"A total of {total_sentiments} sentiment entries were analyzed."
    ]

    # --- 2. Engagement Trend over time (Line Chart) ---
    engagement_by_date = df.groupby(df['date'].dt.date)['engagements'].sum().reset_index()
    engagement_by_date.columns = ['Date', 'Total Engagements']
    fig_engagements_trend = px.line(engagement_by_date, x='Date', y='Total Engagements',
                                   title='Engagement Trend Over Time')
    engagements_trend_path = os.path.join(output_dir, 'engagement_trend_line.html')
    fig_engagements_trend.write_html(engagements_trend_path)
    chart_files.append(f"Engagement Trend: {engagements_trend_path}")

    max_engagement_date = engagement_by_date.loc[engagement_by_date['Total Engagements'].idxmax()]['Date'].strftime('%Y-%m-%d') if not engagement_by_date.empty else 'N/A'
    min_engagement_date = engagement_by_date.loc[engagement_by_date['Total Engagements'].idxmin()]['Date'].strftime('%Y-%m-%d') if not engagement_by_date.empty else 'N/A'
    total_engagements = engagement_by_date['Total Engagements'].sum() if not engagement_by_date.empty else 0

    insights['engagements_trend'] = [
        f"The highest engagement occurred on {max_engagement_date}.",
        f"The lowest engagement occurred on {min_engagement_date}.",
        f"Overall, the data covers a period with a total of {total_engagements} engagements."
    ]


    # --- 3. Platform Engagements (Bar Chart) ---
    engagements_by_platform = df.groupby('platform')['engagements'].sum().reset_index()
    engagements_by_platform.columns = ['Platform', 'Total Engagements']
    fig_platform_engagements = px.bar(engagements_by_platform, x='Platform', y='Total Engagements',
                                      title='Engagements by Platform',
                                      color_discrete_sequence=px.colors.qualitative.Set2)
    platform_engagements_path = os.path.join(output_dir, 'platform_engagements_bar.html')
    fig_platform_engagements.write_html(platform_engagements_path)
    chart_files.append(f"Platform Engagements: {platform_engagements_path}")

    top_platform = engagements_by_platform.loc[engagements_by_platform['Total Engagements'].idxmax()]['Platform'] if not engagements_by_platform.empty else 'N/A'
    max_platform_engagement = engagements_by_platform['Total Engagements'].max() if not engagements_by_platform.empty else 0
    total_platform_engagements = engagements_by_platform['Total Engagements'].sum() if not engagements_by_platform.empty else 0
    top_platform_percentage = (max_platform_engagement / total_platform_engagements * 100).round(2) if total_platform_engagements > 0 else 0

    insights['platform_engagements'] = [
        f"'{top_platform}' is the leading platform in terms of engagements, contributing {top_platform_percentage}% of the total.",
        f"The sum of engagements across all platforms is {total_platform_engagements}.",
        "Platforms with lower engagement might indicate areas for strategic focus or different audience demographics."
    ]

    # --- 4. Media Type Mix (Pie Chart) ---
    media_type_counts = df['media_type'].value_counts(dropna=False).reset_index()
    media_type_counts.columns = ['Media Type', 'Count']
    fig_media_type = px.pie(media_type_counts, names='Media Type', values='Count',
                           title='Media Type Mix',
                           color_discrete_sequence=px.colors.qualitative.Dark2)
    media_type_path = os.path.join(output_dir, 'media_type_mix_pie.html')
    fig_media_type.write_html(media_type_path)
    chart_files.append(f"Media Type Mix: {media_type_path}")

    total_media_types = media_type_counts['Count'].sum()
    top_media_type = media_type_counts.iloc[0]['Media Type'] if not media_type_counts.empty else 'N/A'
    top_media_type_percentage = (media_type_counts.iloc[0]['Count'] / total_media_types * 100).round(2) if total_media_types > 0 else 0

    insights['media_type'] = [
        f"'{top_media_type}' is the most prevalent media type, making up {top_media_type_percentage}% of the analyzed content.",
        "The diversity in media types suggests varied content strategies.",
        "Consider analyzing why certain media types perform better or worse in terms of overall presence."
    ]

    # --- 5. Top 5 Locations (Bar Chart) ---
    engagements_by_location = df.groupby('location')['engagements'].sum().nlargest(5).reset_index()
    engagements_by_location.columns = ['Location', 'Total Engagements']
    fig_top_locations = px.bar(engagements_by_location, x='Location', y='Total Engagements',
                                title='Top 5 Locations by Engagements',
                                color_discrete_sequence=px.colors.qualitative.Vivid)
    top_locations_path = os.path.join(output_dir, 'top_locations_bar.html')
    fig_top_locations.write_html(top_locations_path)
    chart_files.append(f"Top 5 Locations: {top_locations_path}")

    top_location_name = engagements_by_location.iloc[0]['Location'] if not engagements_by_location.empty else 'N/A'

    insights['top_locations'] = [
        f"The top location by engagements is '{top_location_name}'.",
        "The top 5 locations represent key geographical areas for engagement.",
        "Further analysis of these locations could reveal regional preferences or market opportunities."
    ]

    return insights, chart_files

def generate_recap_text(insights):
    """Generates a comprehensive recap text from the collected insights."""
    recap = "# Media Intelligence Dashboard Recap\n\n"
    for section_title, insight_list in {
        "Sentiment Breakdown Insights": insights.get('sentiment', []),
        "Engagement Trend Over Time Insights": insights.get('engagements_trend', []),
        "Platform Engagements Insights": insights.get('platform_engagements', []),
        "Media Type Mix Insights": insights.get('media_type', []),
        "Top 5 Locations by Engagements Insights": insights.get('top_locations', []),
    }.items():
        if insight_list:
            recap += f"## {section_title}\n"
            for insight in insight_list:
                recap += f"- {insight}\n"
            recap += "\n"
    return recap

if __name__ == "__main__":
    print("Welcome to the I.M.I.D - Interactive Media Intelligence Dashboard (Python Version)!")
    print("This script will process your CSV data and generate interactive charts and an analysis recap.")

    csv_file_path = input("Please enter the path to your CSV file (e.g., data.csv): ")

    print("\nProcessing data...")
    processed_df = process_csv_data(csv_file_path)

    if processed_df is not None and not processed_df.empty:
        print("\nData successfully processed!")
        output_folder = "media_analysis_output"
        print(f"Generating charts and insights in the '{output_folder}' directory...")
        all_insights, generated_chart_files = generate_charts_and_insights(processed_df, output_folder)

        if all_insights:
            recap_content = generate_recap_text(all_insights)
            recap_file_path = os.path.join(output_folder, 'media_intelligence_recap.txt')
            with open(recap_file_path, 'w', encoding='utf-8') as f:
                f.write(recap_content)
            print(f"Analysis recap saved to: {recap_file_path}")

            print("\nCharts generated successfully! You can open these files in your web browser:")
            for chart_info in generated_chart_files:
                print(f"- {chart_info}")
        else:
            print("No insights were generated, likely due to data issues.")
    else:
        print("\nData processing failed. Please check the console messages for details.")

    print("\nAnalysis complete.")

