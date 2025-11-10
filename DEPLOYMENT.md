# Damped Harmonic Oscillator Pro - Deployment Guide

## Streamlit Cloud Deployment

### Prerequisites
- GitHub account
- Streamlit Cloud account (free)

### Steps to Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit - Damped Oscillator Pro"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Select the repository containing this code
   - Set the main file path to `app.py`
   - Click "Deploy!"

### Configuration Files

The app includes the following configuration files:

- **`requirements.txt`**: Python dependencies
- **`packages.txt`**: System dependencies (for Streamlit Cloud)
- **`.streamlit/config.toml`**: Streamlit configuration

### Troubleshooting

#### Port Permission Error
If you encounter "Permission denied" errors, ensure:
- No hardcoded port numbers in the code
- The `.streamlit/config.toml` file doesn't specify a restricted port
- Streamlit Cloud will automatically assign the correct port

#### Animation Performance
The animation is optimized for cloud deployment with:
- Reduced frame rate to prevent excessive reruns
- Built-in delays to prevent server overload
- Efficient data handling

#### Dependencies
All required packages are listed in `requirements.txt`:
- streamlit==1.51.0
- numpy==2.3.4
- scipy==1.16.3
- plotly==6.4.0
- matplotlib==3.10.7
- streamlit-extras==0.7.8

### Features
- Real-time harmonic oscillator simulation
- Interactive parameter controls
- Laplace transform analysis
- Real-time animation
- Professional UI with dark theme

### Support
For issues or questions, please check the Streamlit documentation or create an issue in the repository.