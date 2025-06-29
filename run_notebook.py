import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import sys
import time

def run_notebook(notebook_path):
    """Execute a Jupyter notebook with progress tracking"""
    print(f"🚀 Starting notebook execution: {notebook_path}")
    start_time = time.time()
    
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    print(f"📄 Notebook loaded with {len(nb.cells)} cells")
    
    # Configure executor with longer timeout for CI/CD
    ep = ExecutePreprocessor(
        timeout=900,  # 15 minutes max
        kernel_name='python3',
        allow_errors=False
    )
    
    try:
        print("⏳ Executing notebook cells...")
        ep.preprocess(nb, {'metadata': {'path': './'}})
        
        elapsed = time.time() - start_time
        print(f"✅ Notebook executed successfully in {elapsed:.2f} seconds!")
        return True
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Error executing notebook after {elapsed:.2f} seconds: {e}")
        
        # Print more details about the error
        if hasattr(e, 'cell_index'):
            print(f"Error occurred in cell {e.cell_index}")
        
        return False

if __name__ == "__main__":
    success = run_notebook("MLFlowSetup.ipynb")
    sys.exit(0 if success else 1) 