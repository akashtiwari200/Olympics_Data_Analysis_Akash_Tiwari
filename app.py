import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

# Configure page with white theme
st.set_page_config(
    page_title="Olympics Analysis Dashboard",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for white theme with ALL fixes
st.markdown("""
    <style>
    /* Main background and text */
    .stApp {
        background-color: #ffffff;
    }

    /* Force ALL text to be dark by default */
    * {
        color: #1a1a1a !important;
    }

    /* But make headers blue */
    h1, h2, h3, h4, h5, h6 {
        color: #1e3a8a !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Sidebar specific */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    [data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }

    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #1e3a8a !important;
    }

    /* Metric cards */
    .stMetric {
        background-color: #f1f5f9;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
    }

    .stMetric label {
        color: #1e3a8a !important;
        font-weight: 600 !important;
    }

    .stMetric div {
        color: #1a1a1a !important;
        font-size: 24px !important;
        font-weight: 700 !important;
    }

    /* Enhanced DataFrame styling for ALL tables */
    .stDataFrame, .dataframe, table {
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        background-color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }

    .stDataFrame th, .dataframe th, table th {
        background-color: #f1f5f9 !important;
        color: #1e3a8a !important;
        font-weight: 700 !important;
        padding: 12px !important;
        border-bottom: 2px solid #3b82f6 !important;
    }

    .stDataFrame td, .dataframe td, table td {
        color: #1a1a1a !important;
        background-color: white !important;
        padding: 10px !important;
        border-bottom: 1px solid #e2e8f0 !important;
    }

    .stDataFrame tr:hover, .dataframe tr:hover, table tr:hover {
        background-color: #f8fafc !important;
    }

    /* CRITICAL FIX: Ensure ALL table text is visible */
    div[data-testid="stDataFrameCell"] {
        color: #1a1a1a !important;
    }

    div[data-testid="stDataFrameCell"] > div {
        color: #1a1a1a !important;
    }

    /* Force text color in all data elements */
    [data-testid="stDataFrameCellData"] {
        color: #1a1a1a !important;
    }

    /* Text selection for ALL tables */
    .stDataFrame ::selection,
    .dataframe ::selection,
    table ::selection,
    .stDataFrame ::-moz-selection,
    .dataframe ::-moz-selection,
    table ::-moz-selection {
        background-color: #3b82f6 !important;
        color: white !important;
    }

    /* Global text selection */
    ::selection {
        background-color: #3b82f6 !important;
        color: white !important;
    }

    ::-moz-selection {
        background-color: #3b82f6 !important;
        color: white !important;
    }

    /* Button styling */
    .stButton>button {
        background-color: #3b82f6 !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 5px !important;
        font-weight: 500 !important;
        border: 1px solid #2563eb !important;
    }

    .stButton>button:hover {
        background-color: #2563eb !important;
        color: white !important;
    }

    /* Download button specific */
    .stDownloadButton>button {
        background-color: #10b981 !important;
        color: white !important;
        border: 1px solid #059669 !important;
        padding: 10px 20px !important;
        border-radius: 5px !important;
        font-weight: 500 !important;
    }

    .stDownloadButton>button:hover {
        background-color: #059669 !important;
    }

    /* Radio buttons */
    .stRadio > div {
        background-color: #f8fafc;
        padding: 10px;
        border-radius: 10px;
    }

    .stRadio label {
        color: #1a1a1a !important;
        font-weight: 500 !important;
    }

    /* Selectbox styling */
    .stSelectbox label {
        color: #1e3a8a !important;
        font-weight: 600 !important;
    }

    .stSelectbox > div > div {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 5px;
        color: #1a1a1a !important;
    }

    /* CRITICAL FIX: Table 3-dots menu dropdown (popup menu) */
    div[data-baseweb="menu"] {
        background-color: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }

    /* Menu items in the dropdown */
    div[data-baseweb="menu"] li,
    div[data-baseweb="menu"] ul,
    div[data-baseweb="menu"] div,
    div[data-baseweb="menu"] span,
    div[data-baseweb="menu"] a {
        color: #1a1a1a !important;
        background-color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }

    /* Menu items hover state */
    div[data-baseweb="menu"] li:hover,
    div[data-baseweb="menu"] div:hover {
        background-color: #f1f5f9 !important;
        color: #1a1a1a !important;
    }

    /* Menu items focus/selected state */
    div[data-baseweb="menu"] li:focus,
    div[data-baseweb="menu"] li[aria-selected="true"] {
        background-color: #dbeafe !important;
        color: #1e3a8a !important;
    }

    /* Specific fix for sort menu items */
    [role="menuitem"] {
        color: #1a1a1a !important;
        background-color: white !important;
    }

    [role="menuitem"]:hover {
        background-color: #f1f5f9 !important;
        color: #1a1a1a !important;
    }

    /* Streamlit's specific menu class */
    .st-emotion-cache-1aehpvj {
        background-color: white !important;
    }

    .st-emotion-cache-1aehpvj li {
        color: #1a1a1a !important;
    }

    /* Fix for the entire popup container */
    [data-baseweb="popover"] {
        background-color: white !important;
        border: 1px solid #e2e8f0 !important;
    }

    [data-baseweb="popover"] * {
        color: #1a1a1a !important;
    }

    /* Fix for menu separators */
    [role="separator"] {
        background-color: #e2e8f0 !important;
    }

    /* Plotly chart text fixes */
    .js-plotly-plot .gtitle {
        color: #1e3a8a !important;
        font-weight: 600 !important;
    }

    .js-plotly-plot .xtitle, .js-plotly-plot .ytitle {
        color: #1a1a1a !important;
        font-weight: 500 !important;
    }

    .js-plotly-plot .xtick text, .js-plotly-plot .ytick text {
        color: #1a1a1a !important;
        fill: #1a1a1a !important;
    }

    .js-plotly-plot .legendtext {
        color: #1a1a1a !important;
        fill: #1a1a1a !important;
    }

    /* Remove streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}

    /* Custom header style */
    .custom-header {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        color: white !important;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .custom-header h1, .custom-header h2, .custom-header h3 {
        color: white !important;
    }

    /* Info boxes */
    .stAlert {
        background-color: #f0f9ff;
        border-left: 4px solid #0ea5e9;
    }

    .stAlert * {
        color: #0369a1 !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9;
        border-radius: 5px 5px 0 0;
        padding: 10px 20px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
    }

    /* Make all text in select boxes dark */
    .stSelectbox option, .stSelectbox select {
        color: #1a1a1a !important;
    }

    /* Ensure plot background is white */
    .plotly-graph-div {
        background-color: white !important;
    }

    /* Streamlit dataframe toolbar buttons */
    .stDataFrame [data-testid="stDataFrameToolbar"] button {
        color: #1a1a1a !important;
        background-color: white !important;
    }

    /* Fix for dataframe column headers */
    [data-testid="stDataFrameColumnHeader"] {
        color: #1e3a8a !important;
        background-color: #f1f5f9 !important;
    }

    /* Fix for all widget labels */
    .stWidgetLabel {
        color: #1e3a8a !important;
        font-weight: 600 !important;
    }

    /* Row selection color */
    .row-selected {
        background-color: #dbeafe !important;
    }

    /* Fix for tooltip text */
    [data-baseweb="tooltip"] {
        color: #1a1a1a !important;
        background-color: white !important;
        border: 1px solid #e2e8f0 !important;
    }

    /* Streamlit expander */
    .streamlit-expanderHeader {
        color: #1e3a8a !important;
        background-color: #f1f5f9 !important;
    }

    /* Make sure all text in modals/dialogs is visible */
    [role="dialog"] {
        background-color: white !important;
        color: #1a1a1a !important;
        border: 1px solid #e2e8f0 !important;
    }

    [role="dialog"] * {
        color: #1a1a1a !important;
    }

    /* Specific fix for the menu that contains Sort, Pin, etc. */
    .st-emotion-cache-1aehpvj,
    .stMenu,
    .stDataFrameMenu {
        background-color: white !important;
        border: 1px solid #e2e8f0 !important;
    }

    .st-emotion-cache-1aehpvj li,
    .stMenu li,
    .stDataFrameMenu li {
        color: #1a1a1a !important;
        background-color: white !important;
    }

    .st-emotion-cache-1aehpvj li:hover,
    .stMenu li:hover,
    .stDataFrameMenu li:hover {
        background-color: #f1f5f9 !important;
        color: #1a1a1a !important;
    }

    /* Icon colors in the menu */
    .st-emotion-cache-1aehpvj svg,
    .stMenu svg,
    .stDataFrameMenu svg {
        color: #1a1a1a !important;
        fill: #1a1a1a !important;
    }

    /* Checkmark in selected menu items */
    [data-baseweb="menu"] [aria-selected="true"] svg {
        color: #3b82f6 !important;
        fill: #3b82f6 !important;
    }

    /* Fix for fullscreen mode backdrop */
    .stDataFrame [data-testid="stFullScreenFrame"] {
        background-color: white !important;
    }

    /* Fix for column resize handle */
    .stDataFrame [data-testid="stDataFrameResizeHandle"] {
        background-color: #e2e8f0 !important;
    }

    /* Fix for search input in tables */
    .stDataFrame input {
        color: #1a1a1a !important;
        background-color: white !important;
        border: 1px solid #e2e8f0 !important;
    }

    /* EXTRA FIX: Ensure all text in athletes table is visible */
    .athletes-table td, .athletes-table th, .athletes-table tr, .athletes-table {
        color: #1a1a1a !important;
    }

    /* Fix for empty cells */
    .stDataFrame td:empty::before {
        content: "—";
        color: #94a3b8 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, region_df)

# Sidebar with improved design
with st.sidebar:
    st.markdown("<div class='custom-header'><h1 style='color:white;'>🏅 Olympics Analysis</h1></div>",
                unsafe_allow_html=True)

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_without_rims.svg/2560px-Olympic_rings_without_rims.svg.png",
        use_container_width=True
    )

    st.markdown("---")

    user_menu = st.radio(
        '📊 **SELECT ANALYSIS TYPE**',
        ('🏅 Medal Tally', '📈 Overall Analysis', '🌍 Country-wise Analysis', '👤 Athlete Analysis')
    )

    st.markdown("---")
    st.markdown("### 🎯 Filter Options")

# -----------------------------------------------------------
# 1️⃣ MEDAL TALLY
# -----------------------------------------------------------
if user_menu == '🏅 Medal Tally':
    st.markdown("<h1 style='color: #1e3a8a; text-align: center;'>🏅 Olympic Medal Tally</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        years, countries = helper.country_year_list(df)
        selected_year = st.selectbox("**Select Year**", years, key="year_select")

    with col2:
        selected_country = st.selectbox("**Select Country/Region**", countries, key="country_select")

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    # Title based on selection
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.markdown("<h2 style='color: #1e3a8a; text-align: center;'>📊 Overall Olympic Medal Tally</h2>",
                    unsafe_allow_html=True)
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.markdown(f"<h2 style='color: #1e3a8a; text-align: center;'>🏆 {selected_year} Olympic Games Medal Tally</h2>",
                    unsafe_allow_html=True)
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.markdown(
            f"<h2 style='color: #1e3a8a; text-align: center;'>🇺🇳 {selected_country} - Historical Performance</h2>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            f"<h2 style='color: #1e3a8a; text-align: center;'>🎯 {selected_country} in {selected_year} Olympics</h2>",
            unsafe_allow_html=True)

    # Display medal tally with better styling
    if not medal_tally.empty:
        # Create medal summary cards
        if 'Gold' in medal_tally.columns and 'Silver' in medal_tally.columns and 'Bronze' in medal_tally.columns:
            total_row = medal_tally.sum()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🥇 Gold Medals", int(total_row['Gold']))
            with col2:
                st.metric("🥈 Silver Medals", int(total_row['Silver']))
            with col3:
                st.metric("🥉 Bronze Medals", int(total_row['Bronze']))
            with col4:
                st.metric("🏅 Total Medals", int(total_row['total']))

        # Display table with custom styling
        st.markdown("### 📋 Detailed Medal Table")

        # Create a download button BEFORE the table (so it's visible)
        csv = medal_tally.to_csv(index=False).encode('utf-8')
        download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
        with download_col2:
            st.download_button(
                label="📥 Download Medal Data as CSV",
                data=csv,
                file_name=f"olympic_medals_{selected_year}_{selected_country}.csv",
                mime="text/csv",
                key="download_medals"
            )

        # Create styled dataframe with explicit text colors
        styled_df = medal_tally.style.set_properties(**{
            'background-color': 'white',
            'color': '#1a1a1a',
            'border': '1px solid #e2e8f0',
            'font-family': 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif'
        })

        # Apply gradients but ensure text remains visible
        if 'Gold' in medal_tally.columns:
            styled_df = styled_df.background_gradient(subset=['Gold'], cmap='YlOrBr', vmin=0)
        if 'Silver' in medal_tally.columns:
            styled_df = styled_df.background_gradient(subset=['Silver'], cmap='Blues', vmin=0)
        if 'Bronze' in medal_tally.columns:
            styled_df = styled_df.background_gradient(subset=['Bronze'], cmap='Oranges', vmin=0)
        if 'total' in medal_tally.columns:
            styled_df = styled_df.background_gradient(subset=['total'], cmap='Greens', vmin=0)

        # Display the table
        st.dataframe(
            styled_df,
            use_container_width=True,
            height=400
        )
    else:
        st.info("No medal data available for the selected filters.")

# -----------------------------------------------------------
# 2️⃣ OVERALL ANALYSIS
# -----------------------------------------------------------
if user_menu == '📈 Overall Analysis':
    st.markdown("<h1 style='color: #1e3a8a; text-align: center;'>📊 Olympic Games Overall Analysis</h1>",
                unsafe_allow_html=True)

    # Statistics cards
    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.markdown("### 📈 Key Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏛️ Editions", editions)
        st.metric("🌍 Host Cities", cities)
    with col2:
        st.metric("⚽ Sports", sports)
        st.metric("🎯 Events", events)
    with col3:
        st.metric("🇺🇳 Nations", nations)
        st.metric("👤 Athletes", athletes)

    # Charts section
    st.markdown("---")
    st.markdown("### 📈 Historical Trends")

    # Interactive line charts
    tab1, tab2, tab3 = st.tabs(["Nations Participation", "Events Evolution", "Athletes Growth"])

    with tab1:
        nations_over_time = helper.data_over_time(df, 'region')
        fig = px.line(nations_over_time, x="Edition", y="region",
                      title="Number of Participating Nations Over Time",
                      markers=True, line_shape="spline")
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color="#1a1a1a", size=12, family="Segoe UI"),
            title=dict(text="Number of Participating Nations Over Time",
                       font=dict(color="#1e3a8a", size=20, family="Segoe UI")),
            xaxis=dict(
                title="Edition",
                title_font=dict(color="#1a1a1a", size=14),
                tickfont=dict(color="#1a1a1a", size=12),
                gridcolor='#e2e8f0',
                linecolor='#e2e8f0'
            ),
            yaxis=dict(
                title="Number of Nations",
                title_font=dict(color="#1a1a1a", size=14),
                tickfont=dict(color="#1a1a1a", size=12),
                gridcolor='#e2e8f0',
                linecolor='#e2e8f0'
            ),
            legend=dict(
                font=dict(color="#1a1a1a", size=12),
                bgcolor='white',
                bordercolor='#e2e8f0',
                borderwidth=1
            )
        )
        fig.update_traces(line_color='#3b82f6', line_width=3)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        events_over_time = helper.data_over_time(df, 'Event')
        fig = px.line(events_over_time, x="Edition", y="Event",
                      title="Number of Events Over Time",
                      markers=True, line_shape="spline", color_discrete_sequence=['#ef4444'])
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color="#1a1a1a", size=12, family="Segoe UI"),
            title=dict(text="Number of Events Over Time", font=dict(color="#1e3a8a", size=20, family="Segoe UI")),
            xaxis=dict(
                title="Edition",
                title_font=dict(color="#1a1a1a", size=14),
                tickfont=dict(color="#1a1a1a", size=12),
                gridcolor='#e2e8f0',
                linecolor='#e2e8f0'
            ),
            yaxis=dict(
                title="Number of Events",
                title_font=dict(color="#1a1a1a", size=14),
                tickfont=dict(color="#1a1a1a", size=12),
                gridcolor='#e2e8f0',
                linecolor='#e2e8f0'
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        athletes_over_time = helper.data_over_time(df, 'Name')
        fig = px.line(athletes_over_time, x="Edition", y="Name",
                      title="Number of Athletes Over Time",
                      markers=True, line_shape="spline", color_discrete_sequence=['#10b981'])
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color="#1a1a1a", size=12, family="Segoe UI"),
            title=dict(text="Number of Athletes Over Time", font=dict(color="#1e3a8a", size=20, family="Segoe UI")),
            xaxis=dict(
                title="Edition",
                title_font=dict(color="#1a1a1a", size=14),
                tickfont=dict(color="#1a1a1a", size=12),
                gridcolor='#e2e8f0',
                linecolor='#e2e8f0'
            ),
            yaxis=dict(
                title="Number of Athletes",
                title_font=dict(color="#1a1a1a", size=14),
                tickfont=dict(color="#1a1a1a", size=12),
                gridcolor='#e2e8f0',
                linecolor='#e2e8f0'
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap
    st.markdown("### 🔥 Events Heatmap (Sport × Year)")
    fig, ax = plt.subplots(figsize=(20, 15))
    pivot = df.drop_duplicates(['Year', 'Sport', 'Event']) \
        .pivot_table(index='Sport', columns='Year',
                     values='Event', aggfunc='count') \
        .fillna(0).astype(int)
    sns.heatmap(pivot, annot=True, ax=ax, cmap='YlOrRd', fmt='g',
                annot_kws={"size": 8, "color": "#1a1a1a", "weight": "normal"})
    ax.set_xlabel('Year', fontsize=12, color='#1a1a1a', fontweight='normal')
    ax.set_ylabel('Sport', fontsize=12, color='#1a1a1a', fontweight='normal')
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')
    ax.tick_params(colors='#1a1a1a', labelsize=10)
    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.set_tick_params(color='#1a1a1a')
    cbar.ax.yaxis.label.set_color('#1a1a1a')
    plt.setp(ax.get_xticklabels(), color='#1a1a1a')
    plt.setp(ax.get_yticklabels(), color='#1a1a1a')
    st.pyplot(fig)

    # FIXED: Most Successful Athletes table with download button
    st.markdown("### 🏆 Most Successful Athletes")

    sport_list = sorted(df['Sport'].unique().tolist())
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox("**Select Sport**", sport_list, key="sport_select_overall")

    top_athletes = helper.most_successful(df, selected_sport)

    # Add CSS to ensure text visibility in the athletes table
    st.markdown("""
    <style>
    /* Ensure all text in the most successful athletes table is visible */
    #most-successful-athletes * {
        color: #1a1a1a !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Add download button BEFORE the table
    if not top_athletes.empty:
        csv_top = top_athletes.to_csv(index=False).encode('utf-8')
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="📥 Download Top Athletes as CSV",
                data=csv_top,
                file_name=f"top_athletes_{selected_sport.replace(' ', '_')}.csv",
                mime="text/csv",
                key="download_top_athletes"
            )

    # Display the styled table with FIXED visibility
    if not top_athletes.empty:
        # Ensure the dataframe has the right structure
        if 'Medals' not in top_athletes.columns:
            # Try to find medal column with different names
            for col in ['Total', 'Total Medals', 'medal_count', 'count']:
                if col in top_athletes.columns:
                    top_athletes = top_athletes.rename(columns={col: 'Medals'})
                    break

        # Add empty columns if they don't exist
        if 'Sport' not in top_athletes.columns:
            top_athletes['Sport'] = selected_sport if selected_sport != 'Overall' else 'Multiple'
        if 'region' not in top_athletes.columns and 'Country' in top_athletes.columns:
            top_athletes = top_athletes.rename(columns={'Country': 'region'})
        elif 'region' not in top_athletes.columns and 'NOC' in top_athletes.columns:
            top_athletes = top_athletes.rename(columns={'NOC': 'region'})

        # Display with guaranteed visible text
        st.markdown('<div id="most-successful-athletes">', unsafe_allow_html=True)

        # Create a simple display with markdown if dataframe display fails
        try:
            st.dataframe(
                top_athletes.style
                .set_properties(**{
                    'color': '#1a1a1a',
                    'background-color': 'white',
                    'border': '1px solid #e2e8f0'
                })
                .background_gradient(subset=['Medals'], cmap='YlOrBr'),
                use_container_width=True,
                height=400
            )
        except:
            # Fallback: Display as a markdown table
            st.markdown("**Top Athletes Table:**")
            st.markdown(top_athletes.to_markdown(), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if len(top_athletes) == 0:
            st.info(f"No athlete data found for {selected_sport}. Try selecting a different sport.")
    else:
        st.warning("No athlete data available. The dataset might not contain medal information for the selected sport.")

# -----------------------------------------------------------
# 3️⃣ COUNTRY WISE ANALYSIS
# -----------------------------------------------------------
if user_menu == '🌍 Country-wise Analysis':
    st.markdown("<h1 style='color: #1e3a8a; text-align: center;'>🌍 Country-wise Olympic Analysis</h1>",
                unsafe_allow_html=True)

    country_list = sorted(df['region'].dropna().unique().tolist())
    selected_country = st.selectbox("**Select Country**", country_list, key="country_analysis")

    st.markdown(f"<h2 style='color: #1e3a8a; text-align: center;'>🇺🇳 {selected_country} Olympic Performance</h2>",
                unsafe_allow_html=True)

    # Medal tally over years
    st.markdown("### 📈 Medal Progression Over Years")
    cdf = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(cdf, x="Year", y="Count",
                  title=f"{selected_country}'s Medal Count Over Years",
                  markers=True, line_shape="spline")
    fig.update_traces(line_color='#3b82f6', line_width=3)
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color="#1a1a1a", size=12, family="Segoe UI"),
        title=dict(text=f"{selected_country}'s Medal Count Over Years",
                   font=dict(color="#1e3a8a", size=20, family="Segoe UI")),
        xaxis=dict(
            title="Year",
            title_font=dict(color="#1a1a1a", size=14),
            tickfont=dict(color="#1a1a1a", size=12),
            gridcolor='#e2e8f0',
            linecolor='#e2e8f0'
        ),
        yaxis=dict(
            title="Medal Count",
            title_font=dict(color="#1a1a1a", size=14),
            tickfont=dict(color="#1a1a1a", size=12),
            gridcolor='#e2e8f0',
            linecolor='#e2e8f0'
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 🔥 Sport-wise Performance Heatmap")
        heatdata = helper.country_event_heatmap(df, selected_country)
        fig, ax = plt.subplots(figsize=(15, 10))
        sns.heatmap(heatdata, annot=True, ax=ax, cmap='YlOrRd', fmt='g',
                    annot_kws={"size": 8, "color": "#1a1a1a", "weight": "normal"})
        ax.set_xlabel('Year', fontsize=12, color='#1a1a1a', fontweight='normal')
        ax.set_ylabel('Sport', fontsize=12, color='#1a1a1a', fontweight='normal')
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')
        ax.tick_params(colors='#1a1a1a', labelsize=10)
        cbar = ax.collections[0].colorbar
        cbar.ax.yaxis.set_tick_params(color='#1a1a1a')
        cbar.ax.yaxis.label.set_color('#1a1a1a')
        plt.setp(ax.get_xticklabels(), color='#1a1a1a')
        plt.setp(ax.get_yticklabels(), color='#1a1a1a')
        st.pyplot(fig)

    with col2:
        # Top athletes with download option
        st.markdown("### 🏆 Top Athletes")
        top_athletes = helper.most_successful_countrywise(df, selected_country)

        # Add download button
        if not top_athletes.empty:
            csv_country = top_athletes.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Top Athletes",
                data=csv_country,
                file_name=f"top_athletes_{selected_country.replace(' ', '_')}.csv",
                mime="text/csv",
                key="download_country_athletes"
            )

        # Display top athletes
        if not top_athletes.empty:
            for idx, row in top_athletes.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div style='background-color:#f1f5f9; padding:10px; border-radius:10px; margin:5px 0; border-left:4px solid #3b82f6'>
                        <strong style='color:#1a1a1a'>{row['Name']}</strong><br>
                        <small style='color:#4b5563'>🏅 {row.get('Medals', row.get('Total', 'N/A'))} medals | {row.get('Sport', 'Various')}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info(f"No athlete data found for {selected_country}.")

# -----------------------------------------------------------
# 4️⃣ ATHLETE ANALYSIS
# -----------------------------------------------------------
if user_menu == '👤 Athlete Analysis':
    st.markdown("<h1 style='color: #1e3a8a; text-align: center;'>👤 Athlete Performance Analysis</h1>",
                unsafe_allow_html=True)

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Age distribution
    st.markdown("### 📊 Age Distribution Analysis")
    tab1, tab2 = st.tabs(["Medal Comparison", "Sport-wise Gold Medalists"])

    with tab1:
        x1 = athlete_df['Age'].dropna()
        x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
        x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
        x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

        fig = ff.create_distplot([x1, x2, x3, x4],
                                 ['All Athletes', 'Gold Medalists', 'Silver Medalists', 'Bronze Medalists'],
                                 show_hist=False, show_rug=False,
                                 colors=['#94a3b8', '#fbbf24', '#9ca3af', '#92400e'])
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color="#1a1a1a", size=12, family="Segoe UI"),
            title=dict(text="Age Distribution by Medal Type", font=dict(color="#1e3a8a", size=20, family="Segoe UI")),
            legend=dict(
                font=dict(color="#1a1a1a", size=12),
                bgcolor='white',
                bordercolor='#e2e8f0',
                borderwidth=1
            ),
            xaxis=dict(
                title="Age",
                title_font=dict(color="#1a1a1a", size=14),
                tickfont=dict(color="#1a1a1a", size=12),
                gridcolor='#e2e8f0',
                linecolor='#e2e8f0'
            ),
            yaxis=dict(
                title="Density",
                title_font=dict(color="#1a1a1a", size=14),
                tickfont=dict(color="#1a1a1a", size=12),
                gridcolor='#e2e8f0',
                linecolor='#e2e8f0'
            ),
            width=1000,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        famous_sports = sorted(['Athletics', 'Swimming', 'Gymnastics', 'Basketball', 'Football', 'Tennis'])
        x = []
        names = []
        colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']

        for sport in famous_sports:
            temp = athlete_df[(athlete_df['Sport'] == sport) & (athlete_df['Medal'] == 'Gold')]
            if not temp.empty:
                x.append(temp['Age'].dropna())
                names.append(sport)

        if x:
            fig = ff.create_distplot(x, names, show_hist=False, show_rug=False, colors=colors[:len(names)])
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color="#1a1a1a", size=12, family="Segoe UI"),
                title=dict(text="Age Distribution of Gold Medalists by Sport",
                           font=dict(color="#1e3a8a", size=20, family="Segoe UI")),
                legend=dict(
                    font=dict(color="#1a1a1a", size=12),
                    bgcolor='white',
                    bordercolor='#e2e8f0',
                    borderwidth=1
                ),
                xaxis=dict(
                    title="Age",
                    title_font=dict(color="#1a1a1a", size=14),
                    tickfont=dict(color="#1a1a1a", size=12),
                    gridcolor='#e2e8f0',
                    linecolor='#e2e8f0'
                ),
                yaxis=dict(
                    title="Density",
                    title_font=dict(color="#1a1a1a", size=14),
                    tickfont=dict(color="#1a1a1a", size=12),
                    gridcolor='#e2e8f0',
                    linecolor='#e2e8f0'
                ),
                width=1000,
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

    # Height vs Weight Analysis
    st.markdown("### 📏 Height vs Weight Analysis")
    col1, col2 = st.columns([1, 2])

    with col1:
        sport_list = sorted(df['Sport'].unique().tolist())
        sport_list.insert(0, 'Overall')
        selected_sport = st.selectbox("**Select Sport**", sport_list, key="sport_scatter")

    with col2:
        temp_df = helper.weight_v_height(df, selected_sport)
        fig, ax = plt.subplots(figsize=(10, 6))

        medal_colors = {'Gold': '#fbbf24', 'Silver': '#9ca3af', 'Bronze': '#92400e', 'No Medal': '#94a3b8'}

        for medal, color in medal_colors.items():
            subset = temp_df[temp_df['Medal'] == medal]
            if not subset.empty:
                ax.scatter(subset['Weight'], subset['Height'],
                           label=medal, alpha=0.6, s=50, color=color)

        ax.set_xlabel('Weight (kg)', fontsize=12, color='#1a1a1a', fontweight='normal')
        ax.set_ylabel('Height (cm)', fontsize=12, color='#1a1a1a', fontweight='normal')
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')
        ax.legend(title='Medal Type', title_fontsize=12, fontsize=10,
                  labelcolor='#1a1a1a', facecolor='white', edgecolor='#e2e8f0')
        ax.grid(True, alpha=0.3, color='#e2e8f0')
        ax.tick_params(colors='#1a1a1a', labelsize=10)
        for spine in ax.spines.values():
            spine.set_color('#e2e8f0')
        st.pyplot(fig)

    # Men vs Women Participation
    st.markdown("### ⚥ Gender Participation Over Time")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"],
                  title="Male vs Female Participation Over the Years",
                  color_discrete_map={'Male': '#3b82f6', 'Female': '#ec4899'})
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color="#1a1a1a", size=12, family="Segoe UI"),
        title=dict(text="Male vs Female Participation Over the Years",
                   font=dict(color="#1e3a8a", size=20, family="Segoe UI")),
        legend=dict(
            font=dict(color="#1a1a1a", size=12),
            bgcolor='white',
            bordercolor='#e2e8f0',
            borderwidth=1,
            title_font=dict(color="#1a1a1a")
        ),
        xaxis=dict(
            title="Year",
            title_font=dict(color="#1a1a1a", size=14),
            tickfont=dict(color="#1a1a1a", size=12),
            gridcolor='#e2e8f0',
            linecolor='#e2e8f0'
        ),
        yaxis=dict(
            title="Number of Athletes",
            title_font=dict(color="#1a1a1a", size=14),
            tickfont=dict(color="#1a1a1a", size=12),
            gridcolor='#e2e8f0',
            linecolor='#e2e8f0'
        ),
        width=1000,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 14px;'>🏅 Olympics Analysis Dashboard • Data from 1896-2016</div>",
    unsafe_allow_html=True)