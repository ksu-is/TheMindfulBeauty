import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Criteria columns and max scores
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

with st.sidebar:
    st.image("logo.png", width=350)  # Logo image
    st.markdown("<h3 style='text-align: center;'>Welcome! Choose from the options below to begin your ethical shopping journey.</h3>", unsafe_allow_html=True)
    category = st.selectbox(
        "Choose Category",
        ["Skincare", "Fashion"]
    )

    selected = option_menu(
        menu_title="Main Menu",
        options=["View Dataset", f"Explore Brands", f"Compare Brands"],
        icons=["eye", "flower1", "columns-gap"],
         menu_icon = "cast",
        default_index=0,
    )

# Load Data
if category == "Skincare":
    df_1 = pd.read_csv("skincare.csv")

    # Drop unnecessary columns
    df_skin = df_1.drop(columns=['Public Record Criticisms+'])
    df_skin.index = df_skin.index + 1

    brand_column = 'Brand'
    brands = df_skin[brand_column].dropna()

    # Handle "View Dataset"
    if selected == "View Dataset":
        with st.container():
            st.subheader("Skincare Dataset")
            st.dataframe(df_skin, height=800, use_container_width=True)

    # Handle "Explore Brands"
    if selected == "Explore Brands":
        st.subheader("Explore Brands")

        # Select brand
        selected_brand = st.selectbox("Choose a brand", brands)

        brand_details = df_skin[df_skin['Brand'] == selected_brand]
        parent_company = brand_details['Parent Company'].values[0]
        gsg_score = brand_details['GSG Score'].values[0]
        brand_link = brand_details['Link'].values[0]
        
        def get_performance_emoji(score):
            if score >= 70:
                return "🌟"
            else:
                return "❌"
            
        performance_emoji = get_performance_emoji(gsg_score)
            
        st.header(f"{selected_brand} {performance_emoji}", anchor="brand")
        st.subheader(f"Parent Company: {parent_company}", divider="grey")
        st.markdown(f"[🔗Learn more about this brand]({brand_link})", unsafe_allow_html=True)

        # Define a variable for the gauge bar color
        gauge_bar_color = "royalblue"

        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=gsg_score,
            title={'text': "GSG Score"},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': gauge_bar_color}},
        ))

        st.plotly_chart(fig2)
        # Consolidated function definition
        def get_score_label(score, max_score):
            percentage = (score / max_score) * 100
            if percentage >= 70:
                return "🌱", "Good"
            elif percentage >= 40:
                return "➖", "Acceptable"
            else:
                return "❌", "Poor"
            
        # Prepare data for chart
        labels = []
        values = []
        colors = []
        hover_texts = []

        for criteria in criteria_cols:
            score = brand_details[criteria].values[0]
            
            if pd.notna(score):
                max_score = max_scores.get(criteria, 10)
                normalized_score = (score / max_score) * 100

                # Assign a default normalized score of 5.0 for criteria with a raw score of 0
                # This ensures that such criteria are not completely excluded from visualization
                if score == 0:
                    normalized_score = 5.0
                
                emoji, tooltip = get_score_label(score, max_score)
                
                labels.append(f"{criteria} {emoji}")
                values.append(normalized_score)
                hover_texts.append(f"{criteria}: {tooltip} ({score}/{max_score})")
                
                # Color based on the level
                if tooltip == "Good":
                    colors.append("#4caf50")
                elif tooltip == "Acceptable":
                    colors.append("#f0ad4e")
                else:
                    colors.append("#dc3545")

        # Create plotly figure
        fig = go.Figure(go.Bar(
            x=values,
            y=labels,
            orientation='h',
            marker=dict(color=colors),
            hovertext=hover_texts,
            hoverinfo="text",
        ))

        fig.update_layout(
            title="Criteria Scores (Normalized)",
            xaxis_title="Score (%)",
            yaxis_title="Criteria",
            yaxis=dict(autorange="reversed"),  # Highest first
            font=dict(color="white"),
            height=600,
        )

        st.plotly_chart(fig, use_container_width=True)

        total_raw_score = brand_details[criteria_cols].sum(axis=1).values[0]
        st.subheader(f"Raw Score Total: {int(round(total_raw_score))} / 149", divider="grey")

    if selected == "Compare Brands":
        st.subheader("Compare Brands")
        
        # Allow multiple brand selection for comparison
        selected_brands = st.multiselect("Select Brands for Comparison", brands)
        
        if selected_brands:
            # Filter the dataset for the selected brands
            comparison_df = df_skin[df_skin['Brand'].isin(selected_brands)]
            
            # Create a new DataFrame for comparison
            comparison_data = {}
            
            for brand in selected_brands:
                brand_data = comparison_df[comparison_df['Brand'] == brand]
                comparison_data[brand] = brand_data[criteria_cols].values.flatten()
            
            # Convert to a DataFrame
            comparison_df_final = pd.DataFrame(comparison_data, index=criteria_cols)

            gsg_scores = {brand: comparison_df[comparison_df['Brand'] == brand]['Raw Score Total'].values[0] for brand in selected_brands}
            comparison_df_final.loc['Raw Score Total'] = gsg_scores

            # Display the comparison table
            st.subheader("Comparison of Selected Brands")
            st.table(comparison_df_final.style.format("{:.1f}"))
        
        st.divider()
        st.subheader("Find Brands by Ethical Areas")

        # Let user select multiple ethical criteria
        selected_criteria = st.multiselect(
            "Select Ethical Criteria to filter brands by (must score 'Good')",
            options=criteria_cols
        )

        if selected_criteria:
            filtered_df = df_skin.copy()

            for crit in selected_criteria:
                max_score = max_scores.get(crit, 10)
                filtered_df = filtered_df[
                    (filtered_df[crit] / max_score * 100) >= 70
                ]

            st.success(f"Found {len(filtered_df)} brands that match your selected criteria.")
            st.dataframe(filtered_df, height=600, use_container_width=True)
        else:
            st.info("Select criteria to find matching brands.")

criteria_cols_2 = [
    'Animal Welfare', 'Environmental Report', 'Organic', 'Nuclear Power', 'Better Cotton Initiative', 
    'Fossil Fuels', 'Ethical Accreditation', 'Other Criticisms', 'Ethical Innovator', 'Armaments', 
    'Code of Conduct', 'Political Donations', 'Ethical Trading Schemes', 'Human Rights'
]

max_scores_2 = {
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
    'Ethical Trading Schemes': 10.1,
    'Political Donations': 10.1,
    'Human Rights': 20
}
            
if category == "Fashion":
    # Load the fashion retailers dataset
    df_2 = pd.read_csv("fashion.csv")

    # Drop unnecessary columns
    df_fash = df_2.drop(columns=['Human Rights+', 'Other Criticisms+'])
    df_fash.index = df_fash.index + 1

    brand_column = 'Brand'
    brands = df_fash[brand_column].dropna()

    # Handle "View Dataset"
    if selected == "View Dataset":
        with st.container():
            st.subheader("Fashion Retailer Dataset")
            st.dataframe(df_fash, height=800, use_container_width=True)

     # Handle "Explore Brands"
    if selected == "Explore Brands":
        st.subheader("Explore Brands")

        # Select brand
        selected_brand = st.selectbox("Choose a brand", brands)

        brand_details = df_fash[df_fash['Brand'] == selected_brand]
        parent_company = brand_details['Parent Company'].values[0]
        gsg_score = brand_details['GSG Score'].values[0]
        brand_link = brand_details['Link'].values[0]
        
        def get_performance_emoji(score):
            if score >= 70:
                return "🌟"
            else:
                return "❌"
            
        performance_emoji = get_performance_emoji(gsg_score)
            
        st.header(f"{selected_brand} {performance_emoji}", anchor="brand")
        st.subheader(f"Parent Company: {parent_company}", divider="grey")
        st.markdown(f"[🔗Learn more about this brand]({brand_link})", unsafe_allow_html=True)

        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=gsg_score,
            title={'text': "GSG Score"},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "royalblue"}},
        ))

        st.plotly_chart(fig2)

        def get_score_label(score, max_score):
            percentage = (score / max_score) * 100
            if percentage >= 70:
                return "🌱", "Good"
            elif percentage >= 40:
                return "➖", "Acceptable"
            else:
                return "❌", "Poor"

        # Prepare data for chart
        labels = []
        values = []
        colors = []
        hover_texts = []

        for criteria in criteria_cols_2:
            score = brand_details[criteria].values[0]
            
            if pd.notna(score):
                max_score = max_scores_2.get(criteria, 10)
                normalized_score = (score / max_score) * 100

                if score == 0:
                    normalized_score = 5.0
                
                emoji, tooltip = get_score_label(score, max_score)
                
                labels.append(f"{criteria} {emoji}")
                values.append(normalized_score)
                hover_texts.append(f"{criteria}: {tooltip} ({score}/{max_score})")
                
                # Color based on the level
                if tooltip == "Good":
                    colors.append("#4caf50")
                elif tooltip == "Acceptable":
                    colors.append("#f0ad4e")
                else:
                    colors.append("#dc3545")

        # Create plotly figure
        fig = go.Figure(go.Bar(
            x=values,
            y=labels,
            orientation='h',
            marker=dict(color=colors),
            hovertext=hover_texts,
            hoverinfo="text",
        ))

        fig.update_layout(
            title="Criteria Scores (Normalized)",
            xaxis_title="Score (%)",
            yaxis_title="Criteria",
            yaxis=dict(autorange="reversed"),  # Highest first
            font=dict(color="white"),
            height=600,
        )

        st.plotly_chart(fig, use_container_width=True)

        total_raw_score = brand_details[criteria_cols_2].sum(axis=1).values[0]
        st.subheader(f"Raw Score Total: {int(total_raw_score)} / 159", divider="grey")

    if selected == "Compare Brands":
        st.subheader("Compare Brands")
        
        # Allow multiple brand selection for comparison
        selected_brands = st.multiselect("Select Brands for Comparison", brands)
        
        if selected_brands:
            # Filter the dataset for the selected brands
            comparison_df = df_fash[df_fash['Brand'].isin(selected_brands)]
            
            # Create a new DataFrame for comparison
            comparison_data = {}
            
            for brand in selected_brands:
                brand_data = comparison_df[comparison_df['Brand'] == brand]
                comparison_data[brand] = brand_data[criteria_cols_2].values.flatten()
            
            # Convert to a DataFrame
            comparison_df_final = pd.DataFrame(comparison_data, index=criteria_cols_2)

            gsg_scores = {brand: comparison_df[comparison_df['Brand'] == brand]['Raw Score Total'].values[0] for brand in selected_brands}
            comparison_df_final.loc['Raw Score Total'] = gsg_scores

            # Display the comparison table
            st.subheader("Comparison of Selected Brands")
            st.table(comparison_df_final.style.format("{:.1f}"))
        
        st.divider()
        st.subheader("Find Brands by Ethical Areas")

        # Let user select multiple ethical criteria
        selected_criteria = st.multiselect(
            "Select Ethical Criteria to filter brands by (must score 'Good')",
            options=criteria_cols_2
        )

        if selected_criteria:
            filtered_df = df_fash.copy()

            for crit in selected_criteria:
                max_score = max_scores_2.get(crit, 10)
                filtered_df = filtered_df[
                    (filtered_df[crit] / max_score * 100) >= 70
                ]

            st.success(f"Found {len(filtered_df)} brands that match your selected criteria.")
            st.dataframe(filtered_df, height=600, use_container_width=True)
        else:
            st.info("Select criteria to find matching brands.")