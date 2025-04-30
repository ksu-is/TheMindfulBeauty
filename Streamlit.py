import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

with st.sidebar:
    st.image("logo.png", width=350)  # Logo image
    st.markdown("<h4 style='text-align: center;'>Welcome! Choose from the options below to begin your ethical shopping journey.</h4>", unsafe_allow_html=True)

    category = st.selectbox(
        "Choose Category", ["Skincare", "Fashion"])
    selected = option_menu(
        menu_title="Main Menu",
        options=["View Dataset", f"Explore Brands", f"Compare Brands"],
        icons=["eye", "flower1", "columns-gap"],
         menu_icon = "cast",
        default_index=0,
    )

# Function to get performance emoji based on score
def get_performance_emoji(score): 
    if score >= 70:
        return "🌟"
    else:
        return "❌"
# Function to get score label and emoji
def get_score_label(score, max_score):
    percentage = (score / max_score) * 100
    if percentage >= 70:
        return "🌱", "Good"
    elif percentage >= 40:
        return "➖", "Acceptable"
    else:
        return "❌", "Poor"
# Function to load data based on category
def load_data(category):
    if category == "Skincare":
        df =pd.read_csv("skincare.csv").drop(columns=['Public Record Criticisms+'])
        criteria_cols = [
            'Animal Welfare', 'Vegetarian/Vegan Verified', 'Environmental Report', 'Genetic Modification', 'Organic',
            'Nuclear Power', 'Fossil Fuels', 'Ethical Accreditation', 'Public Record Criticisms', 'Ethical Innovator',
            'Armaments', 'Irresponsible Marketing', 'Political Donations'
        ]

        max_scores = {
            'Animal Welfare': 20,
            'Vegetarian/Vegan Verified': 10.1,
            'Environmental Report': 10.1,
            'Genetic Modification': 10.1,
            'Organic': 10.1,
            'Nuclear Power': 10.1,
            'Fossil Fuels': 10.1,
            'Ethical Accreditation': 10.1,
            'Public Record Criticisms': 20,
            'Ethical Innovator': 8,
            'Armaments': 10.1,
            'Irresponsible Marketing': 10.1,
            'Political Donations': 10.1
        }
        raw_score_total = 149
    else:
        df = pd.read_csv("fashion.csv").drop(columns=['Human Rights+', 'Other Criticisms+'])
        criteria_cols = [
            'Animal Welfare', 'Environmental Report', 'Organic', 'Nuclear Power', 'Better Cotton Initiative',
            'Fossil Fuels', 'Ethical Accreditation', 'Other Criticisms', 'Ethical Innovator', 'Armaments',
            'Code of Conduct', 'Political Donations', 'Ethical Trading Schemes', 'Human Rights'
        ]

        max_scores = {
            'Animal Welfare': 10.1,
            'Environmental Report': 10.1,
            'Organic': 10.1,
            'Nuclear Power': 10.1,
            'Better Cotton Initiative': 10.1,
            'Fossil Fuels': 10.1,
            'Ethical Accreditation': 10.1,
            'Other Criticisms': 20,
            'Ethical Innovator': 8,
            'Armaments': 10.1,
            'Code of Conduct': 10.1,
            'Political Donations': 10.1,
            'Ethical Trading Schemes': 10.1,
            'Human Rights': 20
        }
        raw_score_total = 159
    df.index += 1    
    return df, criteria_cols, max_scores, raw_score_total 

# Function to display brand information and scores
def display_brand_info(df, brand, criteria_cols, max_scores, raw_score_total):
    brand_details = df[df['Brand'] == brand]  
    st.header(f"{brand} {get_performance_emoji(brand_details['GSG Score'].values[0])}")
    st.subheader(f"Parent Company: {brand_details['Parent Company'].values[0]}", divider="grey")
    st.markdown(f"[🔗Learn more about this brand]({brand_details['Link'].values[0]})", unsafe_allow_html=True)

    gauge_bar_color = "royalblue"

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=brand_details['GSG Score'].values[0],
        title={'text': "GSG Score"},
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': gauge_bar_color}, 'steps': [
            {'range': [0, 40], 'color': "#f4b6b6"},
            {'range': [40, 70], 'color': "#ffe39f"},
            {'range': [70, 100], 'color': "#a6dcb2"}
        ]}
    ))

    st.plotly_chart(fig_gauge)

    # Prepare data for chart
    labels = []
    values = []
    colors = []
    hover_texts = []

    for criteria in criteria_cols:

        score = brand_details[criteria].values[0]

        if pd.notna(score):
            max_score = max_scores[criteria]
            normalized_score = (score / max_score) * 100
            if score == 0:
                normalized_score = 5.0
            emoji, label = get_score_label(score, max_score)
            labels.append(f"{criteria} {emoji}")
            values.append(normalized_score)
            hover_texts.append(f"{label} ({score}/{max_score})")
            colors.append("#4caf50" if label == "Good" else "#f0ad4e" if label == "Acceptable" else "#dc3545")  

    # Create plotly figure
    fig_bar_chart = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation='h',
        marker=dict(color=colors),
        hovertext=hover_texts,
        hoverinfo="text",
    ))

    fig_bar_chart.update_layout(
        title="Criteria Scores (Normalized)",
        xaxis_title="Score (%)",
        yaxis_title="Criteria",
        yaxis=dict(autorange="reversed"),  # Highest first
        font=dict(color="white"),
        height=600,
    )

    st.plotly_chart(fig_bar_chart, use_container_width=True)

    total = brand_details[criteria_cols].sum(axis=1).values[0]
    st.subheader(f"Raw Score Total: {int(round(total))} / {raw_score_total}", divider="grey")

# Function to compare selected brands
def compare_brands(df, criteria_cols, max_scores):
    selected_brands = st.multiselect("Select Brands for Comparison", df['Brand'].dropna())
    if selected_brands:
        # Filter the dataset for the selected brands
        comparison_df = df[df['Brand'].isin(selected_brands)]
        comparison_data = {}
        for _, row in comparison_df.iterrows():
            brand = row['Brand']
            if brand in selected_brands:
                comparison_data[brand] = row[criteria_cols].values
        comparison_table = pd.DataFrame(comparison_data, index=criteria_cols)
        raw_scores = {brand: comparison_df[comparison_df['Brand'] == brand][criteria_cols].sum(axis=1).values[0]
                      for brand in selected_brands}
        comparison_table.loc['Raw Score Total'] = raw_scores
        st.subheader("Comparison of Selected Brands")
        st.table(comparison_table.style.format("{:.1f}"))
    
    st.divider()
    st.subheader("Find Brands by Ethical Areas")
    selected_criteria = st.multiselect(
        "Select Ethical Criteria to filter brands by (must score 'Good')",
        criteria_cols
    )
    if selected_criteria:
        filtered_df = df.copy()
        for crit in selected_criteria:
            max_score = max_scores[crit]
            filtered_df = filtered_df[
                (filtered_df[crit] / max_score * 100) >= 70
            ]
        st.success(f"Found {len(filtered_df)} brands that match your selected criteria.")
        st.dataframe(filtered_df, height=600, use_container_width=True)
    else:
        st.info("Select criteria to find matching brands.")

# Load data based on selected category
df, criteria_cols, max_scores, raw_score_total = load_data(category)
if selected == "View Dataset":
    st.subheader(f"{category} Dataset")
    st.dataframe(df, height=800, use_container_width=True)

elif selected == "Explore Brands":
    st.subheader(f"Explore {category} Brands")
    selected_brand = st.selectbox("Choose a brand", df['Brand'].dropna())
    display_brand_info(df, selected_brand, criteria_cols, max_scores, raw_score_total)

elif selected == "Compare Brands":
    st.subheader(f"Compare {category} Brands")
    compare_brands(df, criteria_cols, max_scores)