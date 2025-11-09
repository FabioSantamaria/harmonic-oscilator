import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from oscillator_solver import solve_damped_oscillator
from laplace_analysis import calculate_laplace_transform

# Apply custom CSS
def apply_custom_css():
    with open("assets/style.css") as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Initialize session state for animation
if 'animation_running' not in st.session_state:
    st.session_state.animation_running = False

# Apply CSS
apply_custom_css()

# Page configuration
st.set_page_config(
    page_title="Damped Oscillator Pro",
    page_icon="🔬",
    layout="wide"
)

# Header
st.markdown("""
<div class="header-container">
    <h1 class="title-text">🔬 Damped Harmonic Oscillator Pro</h1>
    <p class="subtitle-text">Advanced Simulation & Laplace Transform Analysis</p>
</div>
""", unsafe_allow_html=True)

# Main layout with improved sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.title("⚙️ System Controls")
    
    # System Parameters Section
    st.markdown('<div class="param-card">', unsafe_allow_html=True)
    st.markdown('<p class="param-title">System Parameters</p>', unsafe_allow_html=True)
    
    m = st.slider("Mass (kg)", 0.1, 10.0, 1.0, 0.1, help="Mass of the oscillating object")
    c = st.slider("Damping Coefficient (N·s/m)", 0.0, 20.0, 2.0, 0.1, help="Damping coefficient")
    k = st.slider("Spring Constant (N/m)", 1.0, 100.0, 10.0, 0.5, help="Stiffness of the spring")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # External Force Section
    st.markdown('<div class="param-card">', unsafe_allow_html=True)
    st.markdown('<p class="param-title">External Force</p>', unsafe_allow_html=True)
    
    F0 = st.slider("Force Amplitude (N)", 0.0, 50.0, 10.0, 0.5, help="Amplitude of sinusoidal force")
    omega = st.slider("Force Frequency (rad/s)", 0.1, 20.0, 5.0, 0.1, help="Frequency of external force")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Initial Conditions Section
    st.markdown('<div class="param-card">', unsafe_allow_html=True)
    st.markdown('<p class="param-title">Initial Conditions</p>', unsafe_allow_html=True)
    
    x0 = st.slider("Initial Position (m)", -5.0, 5.0, 1.0, 0.1, help="Starting position")
    v0 = st.slider("Initial Velocity (m/s)", -10.0, 10.0, 0.0, 0.1, help="Starting velocity")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Simulation Settings
    st.markdown('<div class="param-card">', unsafe_mit_allow_html=True)
    st.markdown('<p class="param-title">Simulation Settings</p>', unsafe_allow_html=True)
    
    t_max = st.slider("Simulation Time (s)", 1.0, 50.0, 20.0, 1.0, help="Total simulation time")
    num_points = st.select_slider("Resolution", options=[1000, 2000, 5000, 10000], value=5000, 
                                   help="Number of data points")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # System Characteristics Display
    omega_n = np.sqrt(k / m)
    zeta = c / (2 * np.sqrt(m * k))
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{omega_n:.2f}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Natural Frequency (rad/s)</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{zeta:.3f}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Damping Ratio</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Animation toggle
    if st.button("▶️ Toggle Animation", help="Toggle real-time animation"):
        st.session_state.animation_running = not st.session_state.animation_running
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main content area
tab1, tab2 = st.tabs(["📊 **Time Domain**", "🌐 **Frequency Domain**"])

# Solve ODE
@st.cache_data
def get_solution(m, c, k, F0, omega, x0, v0, t_max, num_points):
    return solve_damped_oscillator(m, c, k, F0, omega, x0, v0, t_max, num_points)

with st.spinner("🧮 Solving differential equations..."):
    t, x, v = get_solution(m, c, k, F0, omega, x0, v0, t_max, num_points)

# Tab 1: Time Domain Analysis
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        st.subheader("📈 Position & Velocity Evolution")
        
        fig1 = make_subplots(
            rows=2, cols=1, shared_xaxes=True,
            subplot_titles=("Position (m)", "Velocity (m/s)"),
            vertical_spacing=0.1
        )
        
        # Add traces with smooth lines
        fig1.add_trace(
            go.Scatter(x=t, y=x, name="Position", line=dict(color="#00A8E8", width=2.5)),
            row=1, col=1
        )
        fig1.add_trace(
            go.Scatter(x=t, y=v, name="Velocity", line=dict(color="#FF6B35", width=2.5)),
            row=2, col=1
        )
        
        fig1.update_layout(
            height=500,
            template="plotly_dark",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=50, b=50, l=50, r=50)
        )
        fig1.update_xaxes(title_text="Time (s)", row=2, col=1)
        
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": True})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        st.subheader("🎯 Phase Space")
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=x, y=v, mode='lines', name="Trajectory",
            line=dict(color="#00A8E8", width=2.5)
        ))
        
        # Add initial condition marker
        fig2.add_trace(go.Scatter(
            x=[x0], y=[v0], mode='markers',
            marker=dict(color="#FF6B35", size=15, symbol="star"),
            name="Initial State"
        ))
        
        fig2.update_layout(
            title="Phase Portrait",
            xaxis_title="Position (m)",
            yaxis_title="Velocity (m/s)",
            template="plotly_dark",
            height=500,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Energy Analysis
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    st.subheader("⚡ Energy Analysis")
    
    kinetic = 0.5 * m * v**2
    potential = 0.5 * k * x**2
    total = kinetic + potential
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=t, y=kinetic, name="Kinetic", line=dict(color="#E74C3C", width=2)))
    fig3.add_trace(go.Scatter(x=t, y=potential, name="Potential", line=dict(color="#2ECC71", width=2)))
    fig3.add_trace(go.Scatter(x=t, y=total, name="Total", line=dict(color="#F39C12", width=3, dash="dash")))
    
    fig3.update_layout(
        title="Energy Components Over Time",
        xaxis_title="Time (s)",
        yaxis_title="Energy (J)",
        template="plotly_dark",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": True})
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Laplace Transform Analysis
with tab2:
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    
    with st.spinner("📡 Computing frequency response..."):
        frequencies, magnitude, phase, poles, zeros = calculate_laplace_transform(
            m, c, k, F0, omega
        )
    
    col3, col4 = st.columns([2, 1])
    
    with col3:
        st.subheader("📊 Bode Plot")
        
        fig4 = make_subplots(
            rows=2, cols=1, shared_xaxes=True,
            subplot_titles=("Magnitude (dB)", "Phase (degrees)"),
            vertical_spacing=0.1
        )
        
        fig4.add_trace(
            go.Scatter(x=frequencies, y=magnitude, line=dict(color="#9B59B6", width=2.5)),
            row=1, col=1
        )
        fig4.add_trace(
            go.Scatter(x=frequencies, y=phase, line=dict(color="#E67E22", width=2.5)),
            row=2, col=1
        )
        
        # Add critical frequency markers
        fig4.add_vline(x=omega, line_dash="dash", line_color="#FF6B35", 
                       annotation_text=f"ω_f = {omega:.2f}")
        fig4.add_vline(x=omega_n, line_dash="dash", line_color="#2ECC71", 
                       annotation_text=f"ω_n = {omega_n:.2f}")
        
        fig4.update_layout(
            height=500,
            template="plotly_dark",
            showlegend=False,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        fig4.update_xaxes(title_text="Frequency (rad/s)", type="log", row=2, col=1)
        
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": True})
    
    with col4:
        st.subheader("🎯 Pole-Zero Map")
        
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=np.real(poles), y=np.imag(poles),
            mode='markers', marker=dict(color="#E74C3C", size=15, symbol="x"),
            name="Poles"
        ))
        fig5.add_trace(go.Scatter(
            x=np.real(zeros), y=np.imag(zeros),
            mode='markers', marker=dict(color="#3498DB", size=12, symbol="circle"),
            name="Zeros"
        ))
        
        # Add stability boundary
        theta = np.linspace(0, 2*np.pi, 100)
        fig5.add_shape(
            type="circle",
            x0=-1, y0=-1, x1=1, y1=1,
            line=dict(color="rgba(255, 255, 255, 0.3)", dash="dot", width=1)
        )
        
        fig5.update_layout(
            title="Pole-Zero Map (s-plane)",
            xaxis_title="Real Axis",
            yaxis_title="Imaginary Axis",
            template="plotly_dark",
            height=500,
            xaxis=dict(scaleanchor="y", scaleratio=1, range=[-3, 3]),
            yaxis=dict(range=[-3, 3])
        )
        
        st.plotly_chart(fig5, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Stability Analysis
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    st.subheader("🛡️ System Stability Analysis")
    
    real_parts = np.real(poles)
    system_status = "STABLE" if np.all(real_parts < 0) else \
                    "MARGINALLY STABLE" if np.any(real_parts == 0) else "UNSTABLE"
    
    if system_status == "STABLE":
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(f"### ✅ System is **{system_status}**")
        st.write("All poles are in the left half-plane. The system will return to equilibrium.")
        st.markdown('</div>', unsafe_allow_html=True)
    elif system_status == "MARGINALLY STABLE":
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown(f"### ⚠️ System is **{system_status}**")
        st.write("Some poles lie on the imaginary axis. The system may oscillate indefinitely.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown(f"### ❌ System is **{system_status}**")
        st.write("Poles are in the right half-plane. The system is divergent!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Show poles and zeros
    col5, col6 = st.columns(2)
    
    with col5:
        with st.expander("📍 Poles"):
            for i, pole in enumerate(poles):
                st.text(f"p{i+1} = {pole:.4f}")
    
    with col6:
        with st.expander("🎯 Zeros"):
            for i, zero in enumerate(zeros):
                st.text(f"z{i+1} = {zero:.4f}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Mathematical Background
with st.expander("📚 **Mathematical Background & Equations**"):
    st.markdown(r"""
    ### Governing Equation
    $$
    m\ddot{x} + c\dot{x} + kx = F_0 \sin(\omega t)
    $$
    
    ### System Characteristics
    - **Natural Frequency**: $\omega_n = \sqrt{k/m}$
    - **Damping Ratio**: $\zeta = \frac{c}{2\sqrt{mk}}$
    
    ### Solution Components
    The total solution consists of:
    1. **Transient Response**: $x_h(t)$ (depends on initial conditions)
    2. **Steady-State Response**: $x_p(t)$ (forced oscillation)
    
    $$
    x(t) = x_h(t) + x_p(t)
    $$
    """)
    
    st.info("""
    **Tip**: Adjust the damping ratio ζ to see different behaviors:
    - ζ < 1: Underdamped (oscillates with decay)
    - ζ = 1: Critically damped (fastest return without oscillation)
    - ζ > 1: Overdamped (slow return without oscillation)
    """)

# Footer
st.markdown("""
<div class="footer">
    <p>Built with ❤️ using Python, Streamlit & Plotly | Deployed on Render</p>
    <p>© 2024 Damped Oscillator Pro - Advanced Physics Simulation</p>
</div>
""", unsafe_allow_html=True)