#!/usr/bin/env python3
"""
Simple repository management script
"""

import os
import shutil
import glob
from pathlib import Path


def add_package_to_repo(package_name, dist_dir="dist"):
    """
    Add a package from dist/ directory to the simple repository
    
    Args:
        package_name (str): The package name (e.g., 'payo-cli')
        dist_dir (str): Directory containing distribution files
    """
    # Normalize package name (lowercase, hyphens)
    normalized_name = package_name.lower().replace('_', '-')
    
    # Create package directory
    package_dir = Path(normalized_name)
    package_dir.mkdir(exist_ok=True)
    
    # Find distribution files
    dist_files = []
    for pattern in [f"{package_name.replace('-', '_')}*.whl", f"{package_name.replace('-', '_')}*.tar.gz"]:
        dist_files.extend(glob.glob(os.path.join(dist_dir, pattern)))
    
    if not dist_files:
        print(f"❌ No distribution files found for {package_name} in {dist_dir}/")
        return False
    
    # Copy files to repository
    copied_files = []
    for file_path in dist_files:
        filename = os.path.basename(file_path)
        dest_path = package_dir / filename
        shutil.copy2(file_path, dest_path)
        copied_files.append(filename)
        print(f"✅ Copied {filename}")
    
    # Create package index.html
    create_package_index(normalized_name, copied_files)
    
    # Update main index.html
    update_main_index()
    
    print(f"🎉 Successfully added {package_name} to repository")
    return True


def create_package_index(package_name, files):
    """Create index.html for a specific package"""
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{package_name} - Python Package Repository</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        .file {{ margin: 10px 0; padding: 10px; border: 1px solid #eee; border-radius: 3px; }}
        .file a {{ color: #0066cc; text-decoration: none; font-weight: bold; }}
        .file a:hover {{ text-decoration: underline; }}
        .back {{ margin-bottom: 20px; }}
        .back a {{ color: #666; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="back">
        <a href="../">← Back to repository index</a>
    </div>
    
    <h1>{package_name}</h1>
    
    <h2>Available Files:</h2>"""
    
    for file in files:
        file_type = "Wheel distribution" if file.endswith('.whl') else "Source distribution"
        html_content += f"""
    <div class="file">
        <a href="{file}">{file}</a>
        <br><small>{file_type}</small>
    </div>"""
    
    html_content += """
    
    <hr>
    <p><em>Install with:</em></p>
    <code>pip install """ + package_name + """</code>
</body>
</html>"""
    
    with open(f"{package_name}/index.html", 'w') as f:
        f.write(html_content)


def update_main_index():
    """Update the main index.html with all packages"""
    # Find all package directories
    package_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]
    
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Simple Python Package Repository</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        .package { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .package h2 { margin-top: 0; color: #0066cc; }
        .file { margin: 5px 0; }
        .file a { color: #0066cc; text-decoration: none; }
        .file a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Simple Python Package Repository</h1>
    <p>This is a simple Python package repository containing the following packages:</p>"""
    
    for package_dir in package_dirs:
        # Get files in package directory
        package_files = [f for f in os.listdir(package_dir) if f.endswith(('.whl', '.tar.gz'))]
        
        html_content += f"""
    
    <div class="package">
        <h2><a href="{package_dir}/">{package_dir}</a></h2>
        <p><strong>Files:</strong></p>"""
        
        for file in package_files:
            file_type = "Wheel distribution" if file.endswith('.whl') else "Source distribution"
            html_content += f"""
        <div class="file">
            <a href="{package_dir}/{file}">{file}</a> ({file_type})
        </div>"""
        
        html_content += """
    </div>"""
    
    html_content += """
    
    <hr>
    <p><em>To install packages from this repository, use:</em></p>
    <code>pip install --extra-index-url https://your-server.com/ package-name</code>
</body>
</html>"""
    
    with open('index.html', 'w') as f:
        f.write(html_content)


def main():
    """Main function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python manage_repo.py <package_name> [dist_directory]")
        print("Example: python manage_repo.py payo-cli")
        return
    
    package_name = sys.argv[1]
    dist_dir = sys.argv[2] if len(sys.argv) > 2 else "dist"
    
    # Change to repository directory
    repo_dir = Path(__file__).parent
    os.chdir(repo_dir)
    
    add_package_to_repo(package_name, dist_dir)


if __name__ == "__main__":
    main() 