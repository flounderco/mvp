import os
import subprocess
import json
import sys

# Get the system's PATH environment variable
system_path = os.environ.get('PATH', '')

# Prepend the Node.js installation directory to the PATH
# Adjust the Node.js installation directory as needed
nodejs_path = r"C:\Program Files\nodejs"  # Example path - Change this to your actual Node.js directory

# Ensure that the path is correct by manually finding the directory path

# Check if the Node.js path is already in the system path to avoid duplicates
if nodejs_path not in system_path:
    os.environ['PATH'] = nodejs_path + os.pathsep + system_path

# Determine Node.js and npm executable paths based on the OS
if sys.platform == 'win32':
    nodejs_executable = os.path.join(nodejs_path, 'node.exe')
    npm_executable = os.path.join(nodejs_path, 'npm.cmd')
else:
    nodejs_executable = 'node'
    npm_executable = 'npm'

# Check if Node.js and npm are installed
try:
    subprocess.run([nodejs_executable, '-v'], check=True, capture_output=True)
    subprocess.run([npm_executable, '-v'], check=True, capture_output=True)
except FileNotFoundError:
    print("Error: Node.js and/or npm not found. Please install Node.js and ensure it's in your PATH.")
    sys.exit(1)

# Create requirements.txt for Flask backend
backend_packages = ['flask', 'pandas', 'flask-cors']
with open('requirements.txt', 'w') as f:
    f.write('\n'.join(backend_packages))

# Install backend packages
subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

# Create client/package.json for React frontend
client_dir = 'client'
os.makedirs(client_dir, exist_ok=True)

# Create default package.json file in client directory if not present
package_json_path = os.path.join(client_dir, 'package.json')

if not os.path.exists(package_json_path):
    package_json = {
        "name": "client",
        "version": "1.0.0",
        "private": True,
        "dependencies": {
            "react": "^18.0.0",
            "react-dom": "^18.0.0",
            "chart.js": "^4.0.0",
            "cors": "^2.8.5",
            "react-scripts": "5.0.1"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject"
        },
        "eslintConfig": {
            "extends": [
                "react-app",
                "react-app/jest"
            ]
        },
        "browserslist": {
            "production": [
                ">0.2%",
                "not dead",
                "not op_mini all"
            ],
            "development": [
                "last 1 chrome version",
                "last 1 firefox version",
                "last 1 safari version"
            ]
        }
    }
    with open(package_json_path, 'w') as f:
        json.dump(package_json, f, indent=4)

# Install frontend packages (only if node_modules doesn't exist)
if not os.path.exists(os.path.join(client_dir, 'node_modules')):
    os.chdir(client_dir)
    try:
        subprocess.run([npm_executable, 'install'], check=True)
        print("Frontend packages have been installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing frontend packages: {e}")
        sys.exit(1)
else:
    print("node_modules directory already exists, skipping npm install.")

print("All necessary packages have been installed successfully.")


