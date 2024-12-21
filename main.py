import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Set page configuration
st.set_page_config(page_title="Physical Tests Analysis", layout="wide")

# Function to load and process data
@st.cache_data
def load_data():
    df = pd.read_excel("physical_tests.xlsx")
    # Rename the unnamed column to 'Name'
    df = df.rename(columns={df.columns[0]: 'Name'})
    return df

# Load the data
df = load_data()

# Title
st.title("Physical Tests Analysis")

# Create sidebar for person selection
selected_person = st.sidebar.selectbox(
    "Select Athlete",
    options=df['Name'].tolist()
)

# Filter data for selected person
person_data = df[df['Name'] == selected_person]

# Create two columns for the visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader("Mobility & Stability Tests")
    
    # Prepare mobility data
    mobility_metrics = [
        'Deep Squat', 'Hurdle Step', 'Inline lunge',
        'Shoulder mobility DA', 'Shoulder mobility NDA',
        'Leg Raise DA', 'Leg Raise NDA',
        'TS Push Up', 'Rotary Stability'
    ]
    
    values = person_data[mobility_metrics].values[0]
    
    # Create radar chart using plotly
    fig_mobility = go.Figure()
    
    fig_mobility.add_trace(go.Scatterpolar(
        r=values,
        theta=mobility_metrics,
        fill='toself',
        name=selected_person
    ))
    
    fig_mobility.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3]
            )
        ),
        showlegend=True
    )
    
    st.plotly_chart(fig_mobility, use_container_width=True)

with col2:
    st.subheader("Jump Performance")
    
    # Process jump data
    jump_data = df[['Name', 'CM Jump (cm)', 'Squat Jump (cm)']].copy()
    jump_data = jump_data[jump_data['CM Jump (cm)'].apply(lambda x: isinstance(x, (int, float)))]
    jump_data = jump_data[jump_data['Squat Jump (cm)'].apply(lambda x: isinstance(x, (int, float)))]
    
    # Create bar chart using plotly
    fig_jumps = go.Figure()
    
    # Add bars for CM Jump
    fig_jumps.add_trace(go.Bar(
        x=jump_data['Name'],
        y=jump_data['CM Jump (cm)'],
        name='Counter Movement Jump',
        marker_color='#22c55e'
    ))
    
    # Add bars for Squat Jump
    fig_jumps.add_trace(go.Bar(
        x=jump_data['Name'],
        y=jump_data['Squat Jump (cm)'],
        name='Squat Jump',
        marker_color='#3b82f6'
    ))
    
    fig_jumps.update_layout(
        barmode='group',
        xaxis_tickangle=-45,
        yaxis_title='Height (cm)',
        legend_title="Jump Type"
    )
    
    st.plotly_chart(fig_jumps, use_container_width=True)

# Add statistics section
st.subheader("Jump Performance Statistics")
col_stats1, col_stats2 = st.columns(2)

with col_stats1:
    st.write("Counter Movement Jump")
    valid_cm = jump_data['CM Jump (cm)']
    st.write(f"Maximum: {valid_cm.max():.1f} cm")
    st.write(f"Minimum: {valid_cm.min():.1f} cm")
    st.write(f"Average: {valid_cm.mean():.1f} cm")

with col_stats2:
    st.write("Squat Jump")
    valid_sq = jump_data['Squat Jump (cm)']
    st.write(f"Maximum: {valid_sq.max():.1f} cm")
    st.write(f"Minimum: {valid_sq.min():.1f} cm")
    st.write(f"Average: {valid_sq.mean():.1f} cm")

# Add data quality note
st.info("""
Legenda: 'L' (Lesionada), 'NP' (Não Participou)
""")