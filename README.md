# GeoGebra-Manim Streamlit UI

This is a web interface for the GeoGebra-Manim project, allowing you to easily convert GeoGebra files (.ggb) to Manim animations without writing any code.

## Setup & Installation

1. **Clone the repository**  
   ```
   git clone https://github.com/KonstBeliakov/Geogebra-manim-project.git
   cd Geogebra-manim-project
   ```

2. **Create & activate a virtual environment**  
   - **Windows (PowerShell)**  
     ```
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **Unix / macOS**  
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**  
   ```
   pip install -r requirements.txt
   ```

## Running the Streamlit UI

Run the Streamlit application with:

```
streamlit run app.py
```

This will start a local web server and open the UI in your default browser.

## Using the UI

1. **Upload** your GeoGebra (.ggb) file using the file uploader.
2. **Configure** the Manim rendering options in the sidebar:
   - Select the video quality (Low, Medium, High)
   - Choose whether to automatically open the preview
3. **Click** the "Generate Animation" button to process the file.
4. **View** the generated animation directly in the UI.
5. **Download** the rendered video using the provided download link.

## Troubleshooting

- If the animation fails to render, check the error messages displayed in the UI.
- Ensure your GeoGebra file is compatible with the converter.
- For more complex issues, refer to the original GeoGebra-Manim project documentation.

## About the Project

This UI is part of the [GeoGebra-Manim Project](https://github.com/KonstBeliakov/Geogebra-manim-project), which provides tools to convert GeoGebra constructions to Manim animations. 