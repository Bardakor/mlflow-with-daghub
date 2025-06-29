import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import sys
import time
import os

def run_notebook(notebook_path):
    """Execute a Jupyter notebook with progress tracking"""
    print(f"Starting notebook execution: {notebook_path}")
    start_time = time.time()
    
    # Ensure output is flushed immediately
    sys.stdout.flush()
    
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    print(f"Notebook loaded with {len(nb.cells)} cells")
    sys.stdout.flush()
    
    # Configure executor with longer timeout for CI/CD
    ep = ExecutePreprocessor(
        timeout=900,  # 15 minutes max
        kernel_name='python3',
        allow_errors=False
    )
    
    try:
        print("Executing notebook cells...")
        sys.stdout.flush()
        
        # Execute with progress updates
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == 'code':
                print(f"Executing cell {i+1}/{len(nb.cells)}")
                sys.stdout.flush()
        
        ep.preprocess(nb, {'metadata': {'path': './'}})
        
        elapsed = time.time() - start_time
        print(f"Notebook executed successfully in {elapsed:.2f} seconds!")
        sys.stdout.flush()
        return True
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"Error executing notebook after {elapsed:.2f} seconds: {e}")
        sys.stdout.flush()
        
        # Print more details about the error
        if hasattr(e, 'cell_index'):
            print(f"Error occurred in cell {e.cell_index}")
        
        # Print environment info for debugging
        print("Environment debugging info:")
        print(f"MLFLOW_TRACKING_URI: {os.getenv('MLFLOW_TRACKING_URI', 'Not set')}")
        print(f"DAGSHUB_TOKEN set: {'Yes' if os.getenv('DAGSHUB_TOKEN') else 'No'}")
        sys.stdout.flush()
        
        return False

if __name__ == "__main__":
    # Ensure unbuffered output
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    success = run_notebook("MLFlowSetup.ipynb")
    sys.exit(0 if success else 1) 