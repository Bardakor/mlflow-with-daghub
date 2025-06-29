import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import sys

def run_notebook(notebook_path):
    """Execute a Jupyter notebook"""
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    
    try:
        ep.preprocess(nb, {'metadata': {'path': './'}})
        print("Notebook executed successfully!")
        return True
    except Exception as e:
        print(f"Error executing notebook: {e}")
        return False

if __name__ == "__main__":
    success = run_notebook("MLFlowSetup.ipynb")
    sys.exit(0 if success else 1) 