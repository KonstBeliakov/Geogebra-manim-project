import streamlit as st
import streamlit.components.v1 as components
import os
import subprocess
import tempfile
import time
from pathlib import Path
import base64
import shutil
import sys
import zipfile
import re
import uuid

# Set page config
st.set_page_config(
    page_title="GeoGebra to Manim Converter",
    page_icon="🧮",
    layout="wide"
)

# --- UTILITY FUNCTIONS ---

def color_hex_to_name(hex_color):
    """Convert hex color to Manim color name if available, otherwise return the hex value"""
    # Dictionary mapping common hex colors to Manim color constants
    color_map = {
        "#FFFFFF": "WHITE",
        "#000000": "BLACK",
        "#FF0000": "RED",
        "#00FF00": "GREEN",
        "#0000FF": "BLUE",
        "#FFFF00": "YELLOW",
        "#FF00FF": "MAGENTA",
        "#00FFFF": "CYAN",
        "#FFA500": "ORANGE",
        "#800080": "PURPLE",
        "#808080": "GRAY",
        "#A52A2A": "BROWN",
        "#FFC0CB": "PINK"
    }
    
    # Convert to uppercase for matching
    hex_upper = hex_color.upper()
    
    # Return the Manim color name if it exists, otherwise return the hex
    return color_map.get(hex_upper, f'"{hex_color}"')

def generate_manim_code(input_file, output_file, 
                     bg_color="#000000", 
                     dot_color="#FFFFFF", 
                     line_color="#FFFFFF", 
                     dashed_line_color="#FFFFFF",
                     circle_color="#FFFFFF", 
                     polygon_color="#FFFFFF", 
                     angle_color="#FFFFFF", 
                     text_color="#FFFFFF",
                     arrow_color="#FFFFFF",
                     dot_radius=0.08,
                     line_thickness=2):
    """Run the manim_code_generator.py script to convert .ggb to manim code and add styling options"""
    try:
        # First generate the basic code
        cmd = ["python", "manim_code_generator.py", input_file, "-o", output_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return False, result.stdout, result.stderr
            
        # Now read the generated file and add styling options
        with open(output_file, 'r', encoding='utf-8') as file:
            code_content = file.read()
        
        # Convert hex colors to Manim color constants where possible
        bg_color_val = color_hex_to_name(bg_color)
        dot_color_val = color_hex_to_name(dot_color)
        line_color_val = color_hex_to_name(line_color)
        dashed_line_color_val = color_hex_to_name(dashed_line_color)
        circle_color_val = color_hex_to_name(circle_color)
        polygon_color_val = color_hex_to_name(polygon_color)
        angle_color_val = color_hex_to_name(angle_color)
        text_color_val = color_hex_to_name(text_color)
        arrow_color_val = color_hex_to_name(arrow_color)
        
        # Create the header with imports and comprehensive styling defaults
        header = f"""from manim import *

# Set background color and global defaults
config.background_color = {bg_color_val}
Dot.set_default(color={dot_color_val}, radius={dot_radius}, z_index=5)
Line.set_default(color={line_color_val}, stroke_width={line_thickness}, z_index=4)
DashedLine.set_default(color={dashed_line_color_val}, stroke_width={line_thickness}, z_index=4)
Circle.set_default(color={circle_color_val}, stroke_width={line_thickness}, z_index=3)
Tex.set_default(color={text_color_val})
MarkupText.set_default(color={text_color_val})
Text.set_default(color={text_color_val})
MathTex.set_default(color={text_color_val})
Polygon.set_default(color={polygon_color_val}, stroke_width={line_thickness}, z_index=0)
Angle.set_default(color={angle_color_val}, radius=0.2, stroke_width={line_thickness}, z_index=3)
RightAngle.set_default(color={angle_color_val}, radius=0.2, stroke_width={line_thickness}, z_index=3)
Arrow.set_default(color={arrow_color_val}, stroke_width={line_thickness}, tip_length=0.2, buff=0.015, z_index=4)
"""
        
        # Split by the class MyScene line to inject our code before it
        class_line_pattern = r"class\s+MyScene\s*\(\s*Scene\s*\)\s*:"
        class_line_match = re.search(class_line_pattern, code_content)
        
        if class_line_match:
            # Extract the imports section
            imports_section = code_content[:class_line_match.start()]
            
            # Extract class section
            class_section = code_content[class_line_match.start():]
            
            # Create our combined header (imports + our styling)
            merged_header = imports_section + "\n" + header
            
            # Combine and write
            modified_code = merged_header + class_section
            
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(modified_code)
                
            return True, result.stdout, result.stderr
        else:
            # Fallback - just add our header and hope it works
            merged_code = header + code_content
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(merged_code)
                
            return True, result.stdout, result.stderr
    except Exception as e:
        return False, "", f"Error executing manim_code_generator.py or adding styling: {str(e)}"

def copy_required_modules(temp_dir, debug_mode=False):
    """Copy all necessary module files to the temporary directory"""
    # Copy all Python files from the current directory to ensure all dependencies are included
    python_files = [f for f in os.listdir() if f.endswith('.py')]
    
    # Add any other non-Python files that might be needed
    other_required_files = []
    
    copied_count = 0
    for py_file in python_files:
        try:
            # Skip the app.py file itself and any examples or tests
            if py_file == 'app.py' or 'example' in py_file.lower() or 'test' in py_file.lower():
                continue
                
            shutil.copy(py_file, os.path.join(temp_dir, py_file))
            copied_count += 1
            if debug_mode:
                st.success(f"Copied module: {py_file}")
        except Exception as e:
            if debug_mode:
                st.warning(f"Could not copy module {py_file}: {str(e)}")
    
    # Copy any other required files
    for other_file in other_required_files:
        if os.path.exists(other_file):
            try:
                shutil.copy(other_file, os.path.join(temp_dir, os.path.basename(other_file)))
                copied_count += 1
                if debug_mode:
                    st.success(f"Copied file: {other_file}")
            except Exception as e:
                if debug_mode:
                    st.warning(f"Could not copy file {other_file}: {str(e)}")
    
    # Create an empty __init__.py file to make the directory a package
    try:
        with open(os.path.join(temp_dir, "__init__.py"), "w") as f:
            f.write("# Generated package file")
    except Exception as e:
        if debug_mode:
            st.warning(f"Could not create __init__.py: {str(e)}")
        
    # Add the temp directory to Python's path
    if temp_dir not in sys.path:
        sys.path.insert(0, temp_dir)
        
    if debug_mode:
        st.success(f"Copied {copied_count} Python files to temporary directory")
    else:
        st.info(f"Copied module files to temporary directory")

def run_manim(script_path, quality, preview, bg_color, resolution, frame_rate, debug_mode=False):
    """Run manim to generate the video"""
    try:
        # Get the directory of the script and the filename
        script_dir = os.path.dirname(script_path)
        script_name = os.path.basename(script_path)
        
        # Copy the script to the current directory
        local_script_path = os.path.join(os.getcwd(), script_name)
        shutil.copy(script_path, local_script_path)
        
        # Construct the manim command
        cmd = ["manim"]
        
        # Add quality flag
        if quality == "Low":
            cmd.append("-ql")
        elif quality == "Medium":
            cmd.append("-qm")
        elif quality == "High":
            cmd.append("-qh")
        
        # Add preview flag if needed
        if preview:
            cmd.append("-p")
        
        # Add custom resolution if provided
        if resolution != "Default":
            width, height = map(int, resolution.split("x"))
            cmd.extend(["--resolution", f"{width},{height}"])
        
        # Add frame rate
        cmd.extend(["--frame_rate", str(frame_rate)])
        
        # Note: We don't need to add background color here as it's set in the styling options
        
        # Add the script and scene
        cmd.extend([local_script_path, "MyScene"])
        
        # Print the command being run (for debugging)
        if debug_mode:
            st.write(f"Running command: {' '.join(cmd)}")
        
        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Clean up the temporary script in the current directory
        if os.path.exists(local_script_path):
            os.remove(local_script_path)
        
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        st.error(f"Error executing manim: {str(e)}")
        return False, "", f"Error executing manim: {str(e)}"

def get_video_path(script_path, quality):
    """Determine the path where manim will output the video"""
    try:
        # When we run manim from the current directory, the video will be in the local media directory
        script_name = os.path.basename(script_path).split('.')[0]
        quality_suffix = {"Low": "480p15", "Medium": "720p30", "High": "1080p60"}[quality]
        
        # The video should be in the current directory's media folder
        video_dir = os.path.join(os.getcwd(), "media", "videos", script_name, quality_suffix)
        video_path = os.path.join(video_dir, f"MyScene.mp4")
        
        if os.path.exists(video_path):
            return video_path
            
        # If not found, let's search for any videos with a similar name
        for root, dirs, files in os.walk(os.path.join(os.getcwd(), "media")):
            for file in files:
                if file.endswith(".mp4") and "MyScene" in file:
                    return os.path.join(root, file)
        
        # If still not found, return the expected path anyway
        return video_path
    except Exception as e:
        st.warning(f"Error finding video path: {str(e)}")
        return os.path.join(os.getcwd(), "media", "videos", "MyScene.mp4")

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """Generate a download link for a binary file"""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(bin_file)}">{file_label}</a>'
        return href
    except Exception as e:
        st.error(f"Error creating download link: {str(e)}")
        return "Download error"

def copy_video_to_accessible_location(video_path, output_filename):
    """Copy the generated video to an accessible location in the app directory"""
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.getcwd(), "output_videos")
        os.makedirs(output_dir, exist_ok=True)
        
        # Copy the video
        output_path = os.path.join(output_dir, output_filename)
        shutil.copy(video_path, output_path)
        st.success(f"Video saved to: {output_path}")
        return output_path
    except Exception as e:
        st.warning(f"Could not copy video to accessible location: {str(e)}")
        return None

def display_debug_info(temp_dir, script_path, video_path):
    """Display helpful debugging information when video isn't found"""
    with st.expander("Debugging Information"):
        st.markdown("### Temporary Directory Structure")
        try:
            temp_dir_files = os.listdir(temp_dir)
            st.code("\n".join(temp_dir_files))
        except Exception as e:
            st.warning(f"Could not list temp directory: {str(e)}")
            
        st.markdown("### Media Directory Structure")
        try:
            # Check main media directory
            media_paths = []
            for root, dirs, files in os.walk("media"):
                for file in files:
                    media_paths.append(os.path.join(root, file))
            
            if media_paths:
                st.code("\n".join(media_paths))
            else:
                st.warning("No files found in media directory")
                
            # Check temporary media directory
            temp_media_dir = os.path.join(temp_dir, "media")
            if os.path.exists(temp_media_dir):
                st.markdown("### Temporary Media Directory")
                temp_media_paths = []
                for root, dirs, files in os.walk(temp_media_dir):
                    for file in files:
                        temp_media_paths.append(os.path.join(root, file))
                
                if temp_media_paths:
                    st.code("\n".join(temp_media_paths))
                else:
                    st.warning("No files found in temporary media directory")
        except Exception as e:
            st.warning(f"Could not list media directory: {str(e)}")
            
        st.markdown("### Paths")
        st.code(f"Script path: {script_path}\nExpected video path: {video_path}")
        
        # Check Python path
        st.markdown("### Python Path")
        st.code("\n".join(sys.path))

def extract_geogebra_preview(ggb_file_path):
    """
    Extract details from GeoGebra file to help with preview
    """
    try:
        # Create a unique ID for the div that will contain the GeoGebra applet
        applet_id = f"ggb-applet-{uuid.uuid4().hex[:8]}"
        
        # Get file name for display
        file_name = os.path.basename(ggb_file_path)
        
        # Return basic information
        return {
            "file_name": file_name,
            "applet_id": applet_id,
            "file_size": os.path.getsize(ggb_file_path),
            "file_path": ggb_file_path
        }
    except Exception as e:
        st.warning(f"Could not extract GeoGebra details: {str(e)}")
        return None

def embed_geogebra_viewer(ggb_file_path):
    """Create an embedded GeoGebra viewer in Streamlit"""
    try:
        # Get the base64 encoded content of the GGB file
        try:
            with open(ggb_file_path, 'rb') as f:
                file_content = f.read()
                ggb_base64 = base64.b64encode(file_content).decode('utf-8')
        except Exception as encode_error:
            st.error(f"Failed to read or encode GeoGebra file: {str(encode_error)}")
            return False
        
        st.markdown("### GeoGebra Construction Preview")
        
        # Create a unique element ID
        element_id = f"ggb-element-{uuid.uuid4().hex[:8]}"
        
        # Create HTML content with direct GeoGebra API embedding
        applet_html = f"""
        <div style="width: 100%; height: 650px; margin: 10px auto; padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px;">
            <script src="https://www.geogebra.org/apps/deployggb.js"></script>
            <div id="{element_id}" style="width: 100%; height: 600px;"></div>
            <script>
                var parameters = {{
                    "appName": "classic", 
                    "width": 800,
                    "height": 600,
                    "showToolBar": false,
                    "showAlgebraInput": false,
                    "showAlgebraView": false,
                    "showMenuBar": false,
                    "showToolBarHelp": false,
                    "showResetIcon": true,
                    "enableLabelDrags": false,
                    "enableShiftDragZoom": true,
                    "enableRightClick": true,
                    "showAxes": true,
                    "showGrid": true,
                    "borderColor": null,
                    "ggbBase64": "{ggb_base64}",
                    "preventFocus": false,
                    "perspective": "G",
                    "useBrowserForJS": false
                }};

                var ggbApplet = new GGBApplet(parameters, true);
                window.onload = function() {{ 
                    ggbApplet.inject('{element_id}');
                }};
            </script>
        </div>
        """
        
        # Display the HTML using Streamlit's components.v1.html
        st.components.v1.html(applet_html, height=650, scrolling=True)
        
        # Also add a link to download the original GGB file
        st.download_button(
            label="Download GeoGebra File",
            data=file_content,
            file_name=os.path.basename(ggb_file_path),
            mime="application/vnd.geogebra.file"
        )
            
        return True
    except Exception as e:
        st.error(f"Could not embed GeoGebra viewer: {str(e)}")
        # Fallback to simple file information if preview fails
        st.info(f"GeoGebra file: {os.path.basename(ggb_file_path)} ({os.path.getsize(ggb_file_path) / 1024:.1f} KB)")
        return False

def custom_css():
    """Add custom CSS to the application"""
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        .stButton > button {
            width: 100%;
            height: 3rem;
            font-size: 1.2rem;
            margin-top: 1rem;
        }
        .success-message {
            padding: 1rem;
            background-color: #d4edda;
            color: #155724;
            border-radius: 0.25rem;
            margin: 1rem 0;
        }
        .error-message {
            padding: 1rem;
            background-color: #f8d7da;
            color: #721c24;
            border-radius: 0.25rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

# Apply custom CSS
custom_css()

# --- MAIN UI ---

# Main UI
st.markdown("<h1 class='main-header'>📐 GeoGebra to Manim Converter</h1>", unsafe_allow_html=True)
st.markdown("<p>Upload a GeoGebra (.ggb) file to convert it into a Manim animation.</p>", unsafe_allow_html=True)

# Debug mode toggle is hidden but still functional for developers
debug_mode = False

# Video quality settings
st.sidebar.markdown("<h3>Video Settings</h3>", unsafe_allow_html=True)
quality = st.sidebar.selectbox(
    "Video Quality",
    ["Low", "Medium", "High"],
    index=0,
    help="Higher quality takes longer to render"
)

# Define default styling parameters
bg_color = "#000000"  # Black background
dot_color = "#FFFFFF"  # White points for better visibility on black
line_color = "#FFFFFF"  # White lines for better visibility on black
dashed_line_color = "#FFFFFF"
circle_color = "#FFFFFF"
polygon_color = "#FFFFFF"
angle_color = "#FFFFFF"
text_color = "#FFFFFF"
arrow_color = "#FFFFFF"
dot_radius = 0.08
line_thickness = 2

# Resolution options
resolution_options = [
    "Default",
    "640x480",
    "1280x720",
    "1920x1080",
    "3840x2160"
]
resolution = st.sidebar.selectbox(
    "Resolution",
    resolution_options,
    index=0,
    help="Custom resolution (width x height)"
)

# Frame rate
frame_rate = st.sidebar.slider(
    "Frame Rate",
    min_value=15,
    max_value=60,
    value=30,
    step=1,
    help="Frames per second"
)

preview = st.sidebar.checkbox(
    "Open preview automatically",
    value=False,
    help="Automatically open the video after rendering (may not work in all environments)"
)

# Render settings explanation
with st.sidebar.expander("About Render Settings"):
    st.markdown("""
    - **Video Quality**: Affects resolution and frame rate preset
    - **Resolution**: Custom width and height (overrides quality preset)
    - **Frame Rate**: Number of frames per second
    - **Background Color**: The color behind the animation
    """)

# Create two columns for the main content area
left_col, right_col = st.columns([2, 3])

with left_col:
    st.markdown("""
    ### About This Tool
    
    This application converts GeoGebra constructions into Manim animations, allowing you to:
    
    - Create beautiful math animations from your GeoGebra files
    - Customize the animation's appearance with styling options
    - Generate high-quality videos for presentations or teaching
    
    ### How to Use
    
    1. Upload your GeoGebra (.ggb) file 
    2. Configure rendering settings in the sidebar
    3. Click "Generate Animation" to process
    4. View and download the rendered video
    """)

# File upload section in the left column
with left_col:
    st.markdown("<h2>Upload File</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload GeoGebra file", type=["ggb"])
    
    if uploaded_file is not None:
        # Create a temporary file to save the uploaded .ggb
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ggb") as tmp_ggb:
            tmp_ggb.write(uploaded_file.getvalue())
            ggb_path = tmp_ggb.name
        
        st.success(f"File uploaded: {uploaded_file.name}")
        
        # Create tabs in the right column
        with right_col:
            geogebra_tab, animation_tab = st.tabs(["GeoGebra Construction", "Manim Animation"])
            
            # Show GeoGebra preview in the GeoGebra tab
            with geogebra_tab:
                embed_geogebra_viewer(ggb_path)
            
            # The animation tab will be populated later when the animation is generated
            with animation_tab:
                st.info("Animation will appear here after processing. Click 'Generate Animation' to start.")
        
        # Create a temporary file for the generated Python code
        temp_dir = tempfile.mkdtemp()
        manim_script_path = os.path.join(temp_dir, "generated_script.py")
        
        # Process the file when the user clicks the button
        if st.button("Generate Animation"):
            with st.spinner("Converting GeoGebra to Manim code..."):
                try:
                    success, stdout, stderr = generate_manim_code(ggb_path, manim_script_path, 
                                                                 bg_color, 
                                                                 dot_color, 
                                                                 line_color, 
                                                                 dashed_line_color,
                                                                 circle_color, 
                                                                 polygon_color, 
                                                                 angle_color, 
                                                                 text_color,
                                                                 arrow_color,
                                                                 dot_radius,
                                                                 line_thickness)
                    
                    if success:
                        st.success("Manim code generated successfully!")
                        
                        # Copy all required modules to the temporary directory
                        with st.spinner("Setting up environment..."):
                            copy_required_modules(temp_dir, debug_mode)
                        
                        # Show the generated code in a collapsible section
                        with st.expander("View Generated Code"):
                            try:
                                with open(manim_script_path, 'r') as f:
                                    st.code(f.read(), language="python")
                            except Exception as e:
                                st.error(f"Error reading generated code: {str(e)}")
                        
                        # Run manim
                        with st.spinner("Rendering animation with Manim... (This may take a while)"):
                            start_time = time.time()
                            success, stdout, stderr = run_manim(
                                manim_script_path, 
                                quality, 
                                preview, 
                                bg_color, 
                                resolution, 
                                frame_rate,
                                debug_mode
                            )
                            render_time = time.time() - start_time
                            
                            if success:
                                # Show the animation in the animation tab
                                with right_col:
                                    # Switch to the animation tab
                                    animation_tab.markdown("<h2>Result</h2>", unsafe_allow_html=True)
                                    animation_tab.success(f"Animation rendered successfully in {render_time:.1f} seconds!")
                                    
                                    # Get the path to the generated video
                                    video_path = get_video_path(manim_script_path, quality)
                                    if os.path.exists(video_path):
                                        # Display the video
                                        animation_tab.video(video_path)
                                        
                                        # Provide a download link
                                        animation_tab.markdown(
                                            get_binary_file_downloader_html(video_path, 'Download Video'),
                                            unsafe_allow_html=True
                                        )
                                        
                                        # Option to save to a specific location
                                        output_filename = animation_tab.text_input(
                                            "Save as (filename)", 
                                            value=f"{os.path.basename(uploaded_file.name).split('.')[0]}.mp4"
                                        )
                                        
                                        # Copy video to accessible location
                                        copy_video_to_accessible_location(video_path, output_filename)
                                    else:
                                        animation_tab.error(f"Video file not found at expected path: {video_path}")
                                        animation_tab.code(f"Checked for video at: {video_path}")
                                        
                                        # Display debugging information if debug mode is enabled
                                        if debug_mode:
                                            display_debug_info(temp_dir, manim_script_path, video_path)
                            else:
                                with right_col:
                                    animation_tab.markdown("<h2>Error</h2>", unsafe_allow_html=True)
                                    animation_tab.error("Failed to render animation!")
                                    animation_tab.error(stderr)
                                    if debug_mode:
                                        with animation_tab.expander("Command Output"):
                                            animation_tab.code(stdout)
                    else:
                        with right_col:
                            animation_tab.markdown("<h2>Error</h2>", unsafe_allow_html=True)
                            animation_tab.error("Failed to generate Manim code!")
                            animation_tab.error(stderr)
                            if debug_mode:
                                with animation_tab.expander("Command Output"):
                                    animation_tab.code(stdout)
                except Exception as e:
                    with right_col:
                        animation_tab.markdown("<h2>Error</h2>", unsafe_allow_html=True)
                        animation_tab.error(f"An unexpected error occurred: {str(e)}")
                        if debug_mode:
                            with animation_tab.expander("Error Details"):
                                animation_tab.code(str(e))
            
            # Clean up temporary files
            try:
                os.unlink(ggb_path)
                # Don't immediately remove the temp_dir as it may contain the video
                # We'll let the OS clean it up later
            except Exception as e:
                st.warning(f"Could not clean up temporary files: {str(e)}")
    else:
        st.info("Please upload a GeoGebra (.ggb) file to get started.")
        
        # Example preview
        with right_col:
            st.markdown("<h2>Example</h2>", unsafe_allow_html=True)
            st.markdown("""
            After uploading a GeoGebra file, you'll see:
            
            1. **GeoGebra Construction** - View of your GeoGebra construction
            2. **Manim Animation** - The rendered animation after processing
            
            The rendering process converts your GeoGebra file into Python code,
            which is then processed by Manim to create the animation.
            
            The conversion may take a few minutes depending on the complexity
            and your selected quality settings.
            """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown(
    "**About**  \n"
    "This tool converts GeoGebra files to Manim animations.  \n"
    "Built with [Streamlit](https://streamlit.io) and [Manim](https://www.manim.community/)."
)

st.sidebar.markdown(
    "**Repository**  \n"
    "[GitHub: GeoGebra-Manim Project](https://github.com/KonstBeliakov/Geogebra-manim-project)"
) 