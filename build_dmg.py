import os
import subprocess
import shutil
import sys

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=True)
    return result

def clean():
    print("Cleaning up previous builds...")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("KeyboardClicks.spec"):
        os.remove("KeyboardClicks.spec")

def build_app():
    print("Building .app with PyInstaller...")
    # Add data: specific sound folders
    # We need to make sure 'sounds' folder is included. 
    # The format is 'source:dest'. 
    # In sound_manager.py we look for 'sounds' relative to resource path.
    
    # We will include the entire sounds directory.
    add_data = "--add-data 'sounds:sounds'"
    
    # Hidden imports - sometimes pynput or pygame needs them, but usually they are fine auto-detected.
    # We'll just try standard build first.
    
    cmd = f"pyinstaller --noconfirm --onedir --windowed --name 'KeyboardClicks' {add_data} main.py"
    run_command(cmd)

def create_dmg():
    print("Creating DMG...")
    
    app_path = "dist/KeyboardClicks.app"
    dmg_name = "KeyboardClicks.dmg"
    dist_dmg_path = os.path.join("dist", dmg_name)
    
    if os.path.exists(dist_dmg_path):
        os.remove(dist_dmg_path)

    # We will use hdiutil to create the dmg
    # 1. Create a temporary folder for the DMG content
    dmg_content = "dist/dmg_content"
    if os.path.exists(dmg_content):
        shutil.rmtree(dmg_content)
    os.makedirs(dmg_content)
    
    # 2. Copy .app to the content folder
    subprocess.run(f"cp -r '{app_path}' '{dmg_content}/'", shell=True, check=True)
    
    # 3. Create a link to Applications folder
    subprocess.run(f"ln -s /Applications '{dmg_content}/Applications'", shell=True, check=True)
    
    # 4. Create DMG using hdiutil
    cmd = f"hdiutil create -volname 'KeyboardClicks' -srcfolder '{dmg_content}' -ov -format UDZO '{dist_dmg_path}'"
    run_command(cmd)
    
    print(f"DMG created at: {dist_dmg_path}")
    
    # Cleanup dmg content folder
    shutil.rmtree(dmg_content)

def main():
    try:
        clean()
        build_app()
        create_dmg()
        print("Build process completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during build process: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
