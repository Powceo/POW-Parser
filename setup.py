import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 8):
        print("Error: Python 3.8 or higher is required.")
        print(f"Current Python version: {major}.{minor}")
        return False
    return True

def create_virtual_env():
    """Create a virtual environment"""
    try:
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("Virtual environment created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False

def install_dependencies():
    """Install required packages from requirements.txt"""
    try:
        print("Installing dependencies...")
        
        # Determine the correct pip and activation script based on the OS
        if platform.system() == "Windows":
            pip_path = os.path.join("venv", "Scripts", "pip")
            activate_script = os.path.join("venv", "Scripts", "activate")
        else:  # macOS and Linux
            pip_path = os.path.join("venv", "bin", "pip")
            activate_script = os.path.join("venv", "bin", "activate")

        # Update pip to the latest version
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
        print("Pip updated to the latest version.")
        
        # Install PyQt5 first
        subprocess.run([pip_path, "install", "PyQt5==5.15.9"], check=True)
        print("PyQt5 installed successfully.")
        
        # Install PyMuPDF using pre-compiled wheels (no building from source)
        subprocess.run([pip_path, "install", "PyMuPDF==1.22.5", "--only-binary=pymupdf"], check=True)
        print("PyMuPDF installed successfully.")
        
        # Install openai
        subprocess.run([pip_path, "install", "openai==0.28.1"], check=True)
        print("OpenAI installed successfully.")
        
        # Show instructions for activating the virtual environment
        if platform.system() == "Windows":
            print("\nTo activate the virtual environment, run:")
            print(f"    {activate_script}")
        else:
            print("\nTo activate the virtual environment, run:")
            print(f"    source {activate_script}")
            
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def main():
    """Main function to run the setup process"""
    print("=" * 60)
    print("P.O.W. Parser Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Create virtual environment
    if not create_virtual_env():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    print("\n" + "=" * 60)
    print("Setup completed successfully!")
    print("You can now run the application with:")
    
    if platform.system() == "Windows":
        print("    venv\\Scripts\\python main.py")
    else:
        print("    venv/bin/python main.py")
    print("=" * 60)

if __name__ == "__main__":
    main()