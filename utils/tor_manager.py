import subprocess
import sys

def is_tor_installed():
    """Check if Tor is installed by running tor --version."""
    try:
        subprocess.check_output(['tor', '--version'], stderr=subprocess.STDOUT)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_tor():
    """Install Tor using apt on Debian-based systems."""
    try:
        # Update package list
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        # Install Tor
        subprocess.run(['sudo', 'apt', 'install', '-y', 'tor'], check=True)
        print("Tor installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")
        return False

def is_tor_running():
    """Check if Tor process is running using pgrep."""
    try:
        subprocess.check_output(['pgrep', 'tor'], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def start_tor():
    """Start the Tor service using systemctl."""
    try:
        subprocess.run(['sudo', 'systemctl', 'start', 'tor'], check=True)
        print("Tor started successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Tor: {e}")
        return False

def run_tor_manager():
    """Main function to check, install, and start Tor if needed."""
    print("Checking Tor status...")
    
    if not is_tor_installed():
        print("Tor is not installed. Installing...")
        if not install_tor():
            sys.exit(1)
    
    if not is_tor_running():
        print("Tor is not running. Starting...")
        if not start_tor():
            sys.exit(1)
    
    print("Tor is installed and running.")

