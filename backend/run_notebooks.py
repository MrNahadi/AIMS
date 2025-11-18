"""
Script to execute all Jupyter notebooks in sequence.
This ensures the ML pipeline runs in the correct order and generates all required artifacts.
"""
import os
import sys
import subprocess
from pathlib import Path

# Define notebook execution order (relative to project root)
NOTEBOOKS = [
    "../notebooks/01_Data_Exploration_Cleaning.ipynb",
    "../notebooks/02_Feature_Engineering_Preprocessing.ipynb",
    "../notebooks/03_Model_Training_Tuning.ipynb",
    "../notebooks/04_Model_Explainability_Export.ipynb"
]

# Expected output artifacts (relative to backend directory)
ARTIFACTS = [
    "artifacts/preprocessor.pkl",
    "artifacts/lgbm_model.pkl",
    "artifacts/shap_explainer.pkl"
]

def check_jupyter_installed():
    """Check if jupyter is installed."""
    try:
        subprocess.run(["jupyter", "--version"], 
                      capture_output=True, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def create_artifacts_dir():
    """Ensure artifacts directory exists."""
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Artifacts directory ready: {artifacts_dir}")

def run_notebook(notebook_path):
    """Execute a single Jupyter notebook."""
    print(f"\n{'='*60}")
    print(f"Executing: {notebook_path}")
    print(f"{'='*60}")
    
    try:
        # Use nbconvert to execute the notebook
        result = subprocess.run(
            [
                "jupyter", "nbconvert",
                "--to", "notebook",
                "--execute",
                "--inplace",
                notebook_path
            ],
            capture_output=True,
            text=True,
            check=True
        )
        
        print(f"✓ Successfully executed: {notebook_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error executing {notebook_path}")
        print(f"Error output:\n{e.stderr}")
        return False

def verify_artifacts():
    """Check if all expected artifacts were created."""
    print(f"\n{'='*60}")
    print("Verifying artifacts...")
    print(f"{'='*60}")
    
    all_exist = True
    for artifact in ARTIFACTS:
        artifact_path = Path(artifact)
        if artifact_path.exists():
            size_mb = artifact_path.stat().st_size / (1024 * 1024)
            print(f"✓ {artifact} ({size_mb:.2f} MB)")
        else:
            print(f"✗ Missing: {artifact}")
            all_exist = False
    
    return all_exist

def main():
    """Main execution function."""
    print("="*60)
    print("AIMS Notebook Execution Pipeline")
    print("="*60)
    
    # Check if jupyter is installed
    if not check_jupyter_installed():
        print("\n✗ ERROR: Jupyter is not installed or not in PATH")
        print("Install with: pip install jupyter notebook")
        return 1
    
    print("✓ Jupyter is installed")
    
    # Create artifacts directory
    create_artifacts_dir()
    
    # Check if all notebooks exist
    print("\nChecking notebooks...")
    for notebook in NOTEBOOKS:
        if not Path(notebook).exists():
            print(f"✗ ERROR: Notebook not found: {notebook}")
            return 1
        print(f"✓ Found: {notebook}")
    
    # Execute notebooks in sequence
    print("\n" + "="*60)
    print("Starting notebook execution...")
    print("="*60)
    
    for i, notebook in enumerate(NOTEBOOKS, 1):
        print(f"\n[{i}/{len(NOTEBOOKS)}] Processing {notebook}...")
        
        if not run_notebook(notebook):
            print(f"\n✗ Pipeline failed at: {notebook}")
            print("Please check the notebook for errors and try again.")
            return 1
    
    # Verify all artifacts were created
    if not verify_artifacts():
        print("\n⚠ Warning: Some artifacts are missing!")
        print("The notebooks may not have completed successfully.")
        return 1
    
    print("\n" + "="*60)
    print("✓ All notebooks executed successfully!")
    print("✓ All artifacts generated!")
    print("="*60)
    print("\nThe ML pipeline is ready. Backend can now use the trained models.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
