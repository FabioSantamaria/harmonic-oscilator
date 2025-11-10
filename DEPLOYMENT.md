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

- **`requirements.txt`**: Python dependencies (simplified for compatibility)
- **No custom Streamlit config**: Using default Streamlit Cloud settings for maximum compatibility

### Troubleshooting

#### Port Permission Error
If you encounter "Permission denied" errors, ensure:
- No hardcoded port numbers in the code
- No custom Streamlit configuration that specifies ports
- Streamlit Cloud will automatically assign the correct port

#### Animation Performance
The animation is optimized for cloud deployment with:
- Reduced frame rate to prevent excessive reruns
- Built-in delays to prevent server overload
- Efficient data handling

#### Dependencies
All required packages are listed in `requirements.txt`:
- streamlit (latest compatible version)
- numpy (latest compatible version)
- scipy (latest compatible version)
- plotly (latest compatible version)
- matplotlib (latest compatible version)

### Features
- Real-time harmonic oscillator simulation
- Interactive parameter controls
- Laplace transform analysis
- Real-time animation
- Professional UI with dark theme

### Support
For issues or questions, please check the Streamlit documentation or create an issue in the repository.