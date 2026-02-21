import zipfile
import os

def zip_project():
    filename = 'StatPage_Deploy.zip'
    print(f"Zipping project to {filename}...")
    
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Root files
        files = ['app.py', 'data_loader.py', 'requirements.txt', '.env', 'trivia_engine.py', 'current_trivia.json', 'stats_config.py']
        for f in files:
            if os.path.exists(f):
                print(f"  Adding {f}")
                zipf.write(f)
            else:
                print(f"  WARNING: {f} not found!")
        
        # Directories to include recursively
        dirs = ['templates', 'static', 'charts', 'chatbot', 'data']
        for d in dirs:
            for root, _, filenames in os.walk(d):
                for f in filenames:
                    # Skip pycache
                    if '__pycache__' in root:
                        continue
                    file_path = os.path.join(root, f)
                    print(f"  Adding {file_path}")
                    zipf.write(file_path)
    
    print(f"Done! {filename} created successfully.")

if __name__ == "__main__":
    zip_project()
