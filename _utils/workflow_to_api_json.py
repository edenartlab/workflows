#!/usr/bin/env python3
"""
ComfyUI Workflow API Format Converter

This script converts ComfyUI workflow JSON files into their API format equivalent using browser automation.
It launches a headless browser (or visible with --show-browser), loads the ComfyUI interface, and uses
the frontend's export functionality to generate the API format.

Key Features:
- Automatic ComfyUI server management (start/stop)
- Direct API export using graphToPrompt
- Browser automation with Playwright
- Detailed logging and diagnostics
- Configurable timeout and retry logic

Usage:
    python workflow_to_api_browser.py --workflow input.json [options]

Common Options:
    --workflow       Input workflow JSON file (default: workflow.json)
    --output        Output API format JSON file (default: workflow_api.json)
    --show-browser  Show browser window during conversion
    --verbose       Show detailed logs including browser console and ComfyUI output
    --run           Run the converted workflow after successful conversion
"""

import sys
import json
import argparse
import logging
import os
import time
import asyncio
import subprocess
import tempfile
from pathlib import Path

# Set up logging with more verbose output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Global persistent browser data directory
BROWSER_DATA_DIR = Path(tempfile.gettempdir()) / "comfy_browser_data"

def parse_args():
    parser = argparse.ArgumentParser(description='Convert ComfyUI workflow to API format using browser automation')
    parser.add_argument('--workflow', 
                       type=Path, 
                       default=Path('workflow.json'),
                       help='Input workflow.json path (default: workflow.json)')
    parser.add_argument('--output', 
                       type=Path, 
                       default=Path('workflow_api.json'),
                       help='Output workflow_api.json path (default: workflow_api.json)')
    parser.add_argument('--port',
                       type=int,
                       default=8188,
                       help='ComfyUI server port (default: 8188)')
    parser.add_argument('--show-browser',
                       action='store_true',
                       help='Show browser window during conversion')
    parser.add_argument('--timeout',
                       type=int,
                       default=120,
                       help='Timeout for server and browser operations (seconds)')
    parser.add_argument('--verbose',
                       action='store_true',
                       help='Show detailed logs including browser console and ComfyUI output')
    parser.add_argument('--no-server-start',
                       action='store_true',
                       help='Do not start ComfyUI server automatically')
    parser.add_argument('--export-method',
                       choices=['graph-to-prompt'],
                       default='graph-to-prompt',
                       help='Export method to use (currently only graph-to-prompt is supported)')
    parser.add_argument('--keep-browser',
                       action='store_true',
                       help='Keep browser running between script executions')
    parser.add_argument('--run',
                       action='store_true',
                       help='Run the converted workflow after successful conversion')
    parser.add_argument('--skip-deps',
                       action='store_true',
                       help='Skip installing workflow dependencies before starting server')
    parser.add_argument('--skip-downloads',
                       action='store_true',
                       help='Skip downloading models specified in workflow.json models section')
    return parser.parse_args()

def is_port_open(port, host='127.0.0.1'):
    """
    Check if a port is open on the specified host.
    
    Args:
        port (int): Port number to check
        host (str): Hostname to check (default: 127.0.0.1)
    
    Returns:
        bool: True if port is open, False otherwise
    """
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def start_comfy_server(workflow_path=None, install_deps=False, verbose=False):
    """
    Start the ComfyUI server using comfy launch command in a thread.
    
    Args:
        workflow_path (Path): Path to workflow file for dependency installation
        install_deps (bool): Whether to install workflow dependencies first
        verbose (bool): Whether to show ComfyUI server output in terminal
    
    Returns:
        bool: True if server started successfully, False otherwise
    """
    logger.info("Starting ComfyUI server...")
    
    try:
        import threading
        import subprocess
        import sys
        
        # Install dependencies if requested
        if install_deps and workflow_path:
            logger.info("Installing workflow dependencies...")
            try:
                if verbose:
                    subprocess.run(['comfy', 'node', 'install-deps', '--workflow', str(workflow_path)])
                else:
                    subprocess.run(
                        ['comfy', 'node', 'install-deps', '--workflow', str(workflow_path)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                logger.info("Dependencies installed successfully")
            except Exception as e:
                logger.error(f"Failed to install dependencies: {e}")
                return False
        
        # Set environment variables
        os.environ['COMFY_SERVE_FRONTEND'] = '1'
        
        # Create a thread to run the server
        def run_server():
            try:
                if verbose:
                    subprocess.run(['comfy', 'launch'])
                else:
                    subprocess.run(['comfy', 'launch'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                logger.error(f"Server thread error: {e}")
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait a bit to check if thread is still running
        time.sleep(2)
        if not server_thread.is_alive():
            logger.error("ComfyUI server thread died")
            return False
            
        logger.info("ComfyUI server started via comfy launch")
        return True
            
    except Exception as e:
        logger.error(f"Failed to start ComfyUI server: {e}")
        return False

async def wait_for_server(port=8188, max_wait=120):
    """
    Wait for ComfyUI server to become accessible.
    
    Args:
        port (int): Port to check for ComfyUI server
        max_wait (int): Maximum time to wait in seconds
    
    Returns:
        bool: True if server is accessible, False if timeout
    """
    logger.info(f"Waiting for ComfyUI server on port {port}...")
    start_time = time.time()
    
    while not is_port_open(port):
        if time.time() - start_time > max_wait:
            logger.error(f"Timeout waiting for server to start on port {port}")
            return False
        await asyncio.sleep(1)
    
    logger.info("ComfyUI server is accessible")
    
    # Additional waiting to ensure server is fully initialized
    # ComfyUI can take some time to fully initialize even after port is open
    await asyncio.sleep(5)
    
    return True

async def wait_for_app_init(page, timeout=60):
    """
    Wait for ComfyUI app to be fully initialized in browser.
    
    Checks for:
    - window.app presence
    - Graph functionality
    - graphToPrompt method
    - loadGraphData method
    
    Args:
        page: Playwright page object
        timeout (int): Maximum time to wait in seconds
    
    Returns:
        bool: True if app is initialized, False if timeout
    """
    logger.info("Waiting for ComfyUI app initialization...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        app_state = await page.evaluate("""
            () => {
                const state = {
                    hasApp: !!window.app,
                    hasGraph: !!(window.app?.graph),
                    hasGraphToPrompt: typeof window.app?.graphToPrompt === 'function',
                    hasLoadGraph: typeof window.app?.loadGraphData === 'function'
                };
                console.log('ComfyUI app state:', state);
                
                if (window.app) {
                    console.log('Available app methods:', Object.keys(window.app));
                }
                
                return state;
            }
        """)
        
        if (app_state.get('hasApp') and 
            app_state.get('hasGraph') and 
            app_state.get('hasGraphToPrompt') and 
            app_state.get('hasLoadGraph')):
            logger.info("ComfyUI app fully initialized")
            return True
            
        await asyncio.sleep(2)
        
    logger.error("ComfyUI app initialization timed out")
    return False

def remove_null_values(obj):
    """
    Recursively remove all null values from a dictionary or list.
    
    Args:
        obj: Dictionary or list to process
        
    Returns:
        Cleaned dictionary or list with null values removed
    """
    if isinstance(obj, dict):
        return {
            key: remove_null_values(value)
            for key, value in obj.items()
            if value is not None
        }
    elif isinstance(obj, list):
        return [remove_null_values(item) for item in obj if item is not None]
    return obj

async def convert_workflow_with_js(workflow_path, output_path, port=8188, show_browser=False, timeout=120, export_method='graph-to-prompt', keep_browser=False, verbose=False):
    """
    Convert a ComfyUI workflow to API format using browser automation.
    
    This function:
    1. Launches a browser (headless by default)
    2. Loads the ComfyUI interface
    3. Waits for app initialization
    4. Loads the workflow
    5. Exports it using the specified method
    6. Saves the API format to the output file
    
    Args:
        workflow_path (str/Path): Path to input workflow JSON
        output_path (str/Path): Path to save API format JSON
        port (int): ComfyUI server port
        show_browser (bool): Whether to show browser window
        timeout (int): Operation timeout in seconds
        export_method (str): Export method to use (currently only graph-to-prompt is supported)
        keep_browser (bool): Keep browser running between executions
        verbose (bool): Whether to show detailed logs including browser console output
    
    Returns:
        bool: True if conversion successful, False otherwise
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        logger.error("Playwright not found. Please install with: pip install playwright")
        logger.error("Then install browsers with: playwright install")
        return False
    
    # Enable detailed logging if verbose mode is on
    if verbose:
        os.environ['DEBUG'] = 'pw:api,pw:browser'
        logger.info("Verbose mode enabled: showing detailed operation logs")
    
    workflow_abs_path = os.path.abspath(workflow_path)
    logger.info(f"Converting workflow: {workflow_abs_path}")
    logger.info(f"Export method: {export_method}")
    
    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow_content = f.read()
            logger.info("Successfully read workflow file")
    except Exception as e:
        logger.error(f"Failed to read workflow file: {e}")
        return False
    
    logger.info("Initializing browser...")
    async with async_playwright() as p:
        try:
            browser_type = p.chromium
            browser_args = [] if show_browser else ["--window-size=1280,900"]
            
            # Create persistent browser data directory if keeping browser
            if keep_browser:
                BROWSER_DATA_DIR.mkdir(parents=True, exist_ok=True)
                logger.info(f"Using persistent browser data at: {BROWSER_DATA_DIR}")
                
                # Launch persistent context
                context = await browser_type.launch_persistent_context(
                    str(BROWSER_DATA_DIR),
                    headless=not show_browser,
                    args=browser_args,
                    viewport={"width": 1280, "height": 900}
                )
                browser = None
                logger.info("Launched persistent browser context")
            else:
                # Regular non-persistent browser
                logger.info("Launching new browser instance...")
                browser = await browser_type.launch(headless=not show_browser, args=browser_args)
                context = await browser.new_context(viewport={"width": 1280, "height": 900})
                logger.info("Browser launched successfully")

            try:
                # Get existing page or create new one
                pages = context.pages
                page = pages[0] if pages else await context.new_page()
                logger.info("Browser page initialized")

                # Custom console handler to filter noise
                def handle_console(msg):
                    if not verbose:  # Only show console messages in verbose mode
                        return
                        
                    text = msg.text
                    # Skip known noise
                    if any(x in text for x in [
                        "defaultValue is deprecated",
                        "efficiency.widgethider",
                        "Failed to load resource",
                        "load and start tracking"
                    ]):
                        return
                    
                    # Log errors and export-related messages
                    if msg.type == "error" or "Export" in text:
                        logger.info(f"BROWSER: {text}")

                page.on("console", handle_console)
                page.on("pageerror", lambda err: logger.error(f"BROWSER ERROR: {err}") if verbose else None)

                # Check if we need to navigate
                current_url = page.url
                target_url = f"http://127.0.0.1:{port}"
                if not current_url.startswith(target_url):
                    logger.info(f"Navigating to ComfyUI interface at {target_url}...")
                    try:
                        await page.goto(target_url, timeout=timeout * 1000)
                        logger.info("Successfully loaded ComfyUI interface")
                        # Initial wait only needed for fresh page load
                        await asyncio.sleep(5)
                    except Exception as e:
                        logger.error(f"Failed to load ComfyUI interface: {e}")
                        return False
                else:
                    logger.info("Reusing existing ComfyUI page")

                logger.info("Checking ComfyUI initialization...")
                
                # Wait for app to be initialized
                app_ready = await wait_for_app_init(page, timeout=60)
                if not app_ready:
                    logger.error("ComfyUI app failed to initialize")
                    return False

                # Load workflow
                logger.info("Loading workflow...")
                load_result = await page.evaluate(f'''
                    () => {{
                        try {{
                            if (!window.app?.loadGraphData) {{
                                throw new Error("loadGraphData not available on window.app");
                            }}
                            
                            const workflow = {json.dumps(workflow_content)};
                            const parsed = JSON.parse(workflow);
                            
                            console.log("Loading workflow data:", parsed);
                            window.app.loadGraphData(parsed);
                            
                            // Verify graph was loaded
                            const graphState = window.app.graph.serialize();
                            console.log("Graph state after load:", {{
                                nodeCount: graphState.nodes.length,
                                linkCount: graphState.links.length
                            }});
                            
                            return {{success: true}};
                        }} catch(e) {{
                            console.error("Load error:", e);
                            return {{
                                success: false,
                                error: String(e),
                                appState: {{
                                    hasApp: !!window.app,
                                    methods: window.app ? Object.keys(window.app) : []
                                }}
                            }};
                        }}
                    }}
                ''')

                if not load_result['success']:
                    logger.error(f"Failed to load workflow: {load_result.get('error')}")
                    if 'appState' in load_result:
                        logger.error(f"App state: {json.dumps(load_result['appState'], indent=2)}")
                    return False
                
                await asyncio.sleep(5)
                logger.info("Starting export process...")

                # Try export up to 3 times
                for attempt in range(3):
                    logger.info(f"Export attempt {attempt + 1}/3")
                    
                    api_workflow = await page.evaluate(f'''
                        async () => {{
                            try {{
                                // Log available methods
                                const appState = {{
                                    hasApp: !!window.app,
                                    graphToPromptType: typeof window.app?.graphToPrompt,
                                    methods: window.app ? Object.keys(window.app) : [],
                                    vueReady: window.app?.vueAppReady
                                }};
                                console.log("App state:", appState);
                                
                                if (typeof window.app?.graphToPrompt !== 'function') {{
                                    throw new Error(`graphToPrompt not available: ${{JSON.stringify(appState)}}`);
                                }}
                                
                                // Try direct graphToPrompt method
                                console.log("Using graphToPrompt export...");
                                const result = await window.app.graphToPrompt();
                                console.log("Export result:", result);
                                
                                if (!result || !result.output) {{
                                    throw new Error("Export returned invalid result: " + JSON.stringify(result));
                                }}

                                // Return only the output part which contains the API format
                                return {{success: true, data: result.output}};
                            }} catch (e) {{
                                console.error("Export error:", e);
                                return {{
                                    success: false,
                                    error: e.message,
                                    stack: e.stack
                                }};
                            }}
                        }}
                    ''')
                    
                    if api_workflow.get('success'):
                        logger.info("Export successful")
                        # Clean the data by removing null values
                        cleaned_data = remove_null_values(api_workflow['data'])
                        with open(output_path, 'w', encoding='utf-8') as f:
                            json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
                        return True

                    error_msg = api_workflow.get('error', 'Unknown error')
                    logger.error(f"Export failed: {error_msg}")

                    if attempt < 2:  # Don't wait after last attempt
                        logger.info("Waiting before next attempt...")
                        await asyncio.sleep(10)

                logger.error("All export attempts failed")
                await page.screenshot(path="debug_export_fail.png")

                # Diagnostic check for app state and available methods
                logger.info("Running app diagnostics...")
                app_diagnostics = await page.evaluate("""
                    () => {
                        const diagnostics = {
                            // Window app state
                            windowApp: {
                                hasApp: !!window.app,
                                appKeys: window.app ? Object.keys(window.app) : [],
                                hasGraph: !!window.app?.graph,
                                hasGraphToPrompt: typeof window.app?.graphToPrompt === 'function'
                            },
                            // DOM state
                            domState: {
                                appElement: !!document.querySelector('#app'),
                                menuMounted: !!document.querySelector('.comfy-menu')
                            }
                        };
                        
                        // Log full diagnostics
                        console.log('App Diagnostics:', JSON.stringify(diagnostics, null, 2));
                        return diagnostics;
                    }
                """)
                
                logger.info("App Diagnostics Results:")
                logger.info(json.dumps(app_diagnostics, indent=2))
                return False
                    
            finally:
                if keep_browser:
                    # Keep context alive if requested
                    if not show_browser:
                        logger.info("Browser window kept alive for next run")
                else:
                    # Close everything if not keeping
                    await context.close()
                    if browser:
                        await browser.close()
                    logger.info("Browser session ended")
        except Exception as e:
            logger.error(f"Browser automation error: {e}")
            return False
    
    return False

def get_comfyui_path():
    """
    Get the ComfyUI installation path using comfy which.
    
    Returns:
        Path: Path to ComfyUI installation directory
    """
    try:
        result = subprocess.run(['comfy', 'which'], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        comfy_path = Path(result.stdout.strip())
        return comfy_path
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get ComfyUI path: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting ComfyUI path: {e}")
        return None

def run_workflow(workflow_path, verbose=False):
    """
    Run a workflow using comfy-cli.
    
    Args:
        workflow_path (Path): Path to the workflow API JSON file
        verbose (bool): Whether to show detailed comfy-cli output
    
    Returns:
        bool: True if workflow ran successfully, False otherwise
    """
    logger.info(f"Running workflow: {workflow_path}")
    
    try:
        # Get ComfyUI path first
        comfy_path = get_comfyui_path()
        if not comfy_path:
            logger.error("Could not determine ComfyUI path")
            return False
            
        # Start the workflow process
        process = subprocess.Popen(
            ["comfy", "run", "--workflow", str(workflow_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered
            universal_newlines=True
        )
        
        # Track outputs
        final_outputs = []  # For saved files
        error_lines = []
        prompt_received = False
        
        def process_output_line(line):
            nonlocal prompt_received
            # Check for key events in the output
            if "Prompt received" in line:
                prompt_received = True
                if not verbose:
                    sys.stdout.write("\r✓ Prompt received by ComfyUI" + " " * 20 + "\n")
                    sys.stdout.flush()
            elif "http://" in line and "/view?" in line:
                # Extract filename and type from preview URL
                try:
                    import urllib.parse
                    url_parts = urllib.parse.urlparse(line.strip())
                    query_params = dict(urllib.parse.parse_qsl(url_parts.query))
                    filename = query_params.get('filename', '')
                    
                    # Skip temp files
                    if any(temp in filename for temp in ['ComfyUI_temp_', 'PBL-_temp_']):
                        return
                        
                    # Construct proper output path using ComfyUI path
                    if filename:
                        output_path = comfy_path / 'output' / filename
                        final_outputs.append(output_path)
                except Exception as e:
                    if verbose:
                        logger.error(f"Error parsing output URL: {e}")
            elif any(x in line.lower() for x in ["error", "exception", "failed"]):
                error_lines.append(line.strip())
        
        if verbose:
            # In verbose mode, show all output but still track important lines
            while True:
                output = process.stdout.readline()
                error = process.stderr.readline()
                
                if output == '' and error == '' and process.poll() is not None:
                    break
                    
                if output:
                    logger.info(output.strip())
                    process_output_line(output)
                if error:
                    logger.error(error.strip())
                    error_lines.append(error.strip())
        else:
            # In non-verbose mode, show progress and key information
            progress_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            idx = 0
            last_update = time.time()
            
            while True:
                # Check for new output
                output = process.stdout.readline()
                error = process.stderr.readline()
                
                if output == '' and error == '' and process.poll() is not None:
                    break
                    
                if output:
                    process_output_line(output)
                if error:
                    error_lines.append(error.strip())
                
                # Update progress indicator every 100ms
                current_time = time.time()
                if current_time - last_update > 0.1:
                    if not prompt_received:
                        sys.stdout.write(f"\r{progress_chars[idx]} Processing..." + " " * 20)
                        sys.stdout.flush()
                        idx = (idx + 1) % len(progress_chars)
                    last_update = current_time
        
        # Wait for process to complete
        process.wait()
        
        if process.returncode == 0:
            if not verbose:
                # Clear the progress line
                sys.stdout.write("\r" + " " * 50 + "\r")
                sys.stdout.flush()
            
            # Show outputs
            if final_outputs:
                logger.info("Generated files:")
                for file in final_outputs:
                    logger.info(f"Output: {file}")
            
            logger.info("Workflow execution completed successfully")
            return True
        else:
            # Always show error information regardless of verbose mode
            sys.stdout.write("\r" + " " * 50 + "\r")  # Clear progress line
            sys.stdout.flush()
            
            logger.error(f"Workflow execution failed with return code {process.returncode}")
            
            # Show collected error lines
            if error_lines:
                logger.error("Error details:")
                for line in error_lines:
                    logger.error(line)
            
            # If no error lines were collected, try to get them from stderr
            remaining_stderr = process.stderr.read()
            if remaining_stderr and not error_lines:
                logger.error("Error output:")
                logger.error(remaining_stderr)
            
            return False
            
    except Exception as e:
        # Always show exception details regardless of verbose mode
        sys.stdout.write("\r" + " " * 50 + "\r")  # Clear progress line
        sys.stdout.flush()
        logger.error(f"Error running workflow: {str(e)}")
        import traceback
        logger.error("Exception details:")
        logger.error(traceback.format_exc())
        return False

def download_workflow_models(workflow_path, verbose=False):
    """
    Download models specified in a workflow's models section.
    
    Args:
        workflow_path (Path): Path to the workflow JSON file
        verbose (bool): Whether to show detailed download output
    
    Returns:
        bool: True if all models downloaded successfully, False if any failed
    """
    try:
        # Get ComfyUI path first
        comfy_path = get_comfyui_path()
        if not comfy_path:
            logger.error("Could not determine ComfyUI path")
            return False
            
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
            
        if 'models' not in workflow:
            logger.info("No models section found in workflow")
            return True
            
        models = workflow['models']
        if not models:
            logger.info("No models to download")
            return True
            
        logger.info(f"Found {len(models)} models to download")
        success = True
        
        # Image and video file extensions
        media_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.mp4', '.webm', '.mkv'}
        
        for model in models:
            name = model.get('name')
            url = model.get('url')
            directory = model.get('directory')
            
            if not all([name, url, directory]):
                logger.error(f"Invalid model specification: {model}")
                success = False
                continue
                
            # Check if this is a media file
            is_media = any(name.lower().endswith(ext) for ext in media_extensions)
            
            # Construct appropriate path
            if is_media or directory == 'input':
                # Media files and input directory files go directly to input
                target_path = Path('input')
                logger.info(f"Downloading file {name} to input directory")
            else:
                # Models go to models/directory
                target_path = Path('models') / directory
                logger.info(f"Downloading model {name} to {target_path}")
            
            try:
                if verbose:
                    subprocess.run(['comfy', 'model', 'download', 
                                 '--url', url, 
                                 '--relative-path', str(target_path),
                                 '--filename', name], check=True)
                else:
                    subprocess.run(
                        ['comfy', 'model', 'download', 
                         '--url', url, 
                         '--relative-path', str(target_path),
                         '--filename', name],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        check=True
                    )
                logger.info(f"Successfully downloaded {name}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to download model {name}: {e}")
                success = False
                
        return success
        
    except Exception as e:
        logger.error(f"Error downloading models: {e}")
        return False

async def main_async():
    """
    Main async function that orchestrates the workflow conversion process.
    
    This function:
    1. Parses command line arguments
    2. Verifies input file existence
    3. Manages ComfyUI server lifecycle
    4. Initiates workflow conversion
    5. Handles errors and cleanup
    
    Returns:
        int: 0 for success, 1 for failure
    """
    args = parse_args()
    
    # Set verbose logging if requested
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Verbose mode enabled: showing detailed operation logs")
    
    logger.info("Starting workflow conversion process...")
    
    # Handle relative/absolute paths
    workflow_path = args.workflow if args.workflow.is_absolute() else Path.cwd() / args.workflow
    output_path = args.output if args.output.is_absolute() else Path.cwd() / args.output
    
    logger.info(f"Input workflow path: {workflow_path}")
    logger.info(f"Output path: {output_path}")
    
    # Verify input file exists
    if not workflow_path.exists():
        logger.error(f"Workflow file not found at: {workflow_path.absolute()}")
        return 1
    
    logger.info("Input file verified successfully")
    
    # Download models by default unless skipped
    if not args.skip_downloads:
        logger.info("Downloading workflow models...")
        if not download_workflow_models(workflow_path, args.verbose):
            logger.error("Failed to download all models")
            return 1
        logger.info("Model downloads completed")
    else:
        logger.info("Skipping model downloads (--skip-downloads)")
    
    # Check if server is running and start it if needed
    server_running = is_port_open(args.port)
    logger.info(f"ComfyUI server status on port {args.port}: {'running' if server_running else 'not running'}")
    
    if not server_running:
        if args.no_server_start:
            logger.error("ComfyUI server is not running and --no-server-start was specified")
            logger.error("Either start ComfyUI manually or remove --no-server-start")
            return 1
            
        logger.info("Attempting to start ComfyUI server...")
        # Try to start the server
        if not start_comfy_server(workflow_path=workflow_path, install_deps=not args.skip_deps, verbose=args.verbose):
            logger.error("Failed to start ComfyUI server")
            return 1
        
        logger.info("Waiting for server to become available...")
        # Wait for server to become available
        server_running = await wait_for_server(args.port, args.timeout)
        if not server_running:
            logger.error("ComfyUI server did not start properly")
            return 1
        
        logger.info("Server started and ready")
    
    logger.info("Beginning workflow conversion...")
    # Convert the workflow
    success = await convert_workflow_with_js(
        workflow_path, output_path, args.port, args.show_browser, args.timeout,
        args.export_method, args.keep_browser, args.verbose
    )
    
    if not success:
        logger.error("Failed to convert workflow to API format")
        return 1
    
    logger.info(f"Workflow conversion completed successfully. Output saved to: {output_path}")
    
    # Run the workflow if requested
    if args.run:
        if not run_workflow(output_path, args.verbose):
            logger.error("Failed to run converted workflow")
            return 1
    
    return 0

def main():
    return asyncio.run(main_async())

if __name__ == "__main__":
    sys.exit(main())