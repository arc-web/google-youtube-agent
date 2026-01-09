#!/usr/bin/env python3
"""
YouTube Content Management Agent Setup Script

Automated setup for the YouTube agent including dependencies and configuration.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_youtube_agent():
    """Main setup function"""
    print("🎬 Setting up YouTube Content Management Agent")
    print("=" * 50)

    # Check if we're in the right directory
    current_dir = Path.cwd()
    if not (current_dir / "README.md").exists() or "google_youtube_agent" not in str(current_dir):
        print("❌ Please run this script from the google_youtube_agent directory")
        return False

    # Create necessary directories
    dirs_to_create = [
        "config",
        "logs",
        "data",
        "tests",
        "docs"
    ]

    for dir_name in dirs_to_create:
        dir_path = current_dir / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"📁 Created directory: {dir_name}")

    # Install dependencies
    deps_file = current_dir.parent.parent / "admin" / "shared" / "dependencies" / "google_youtube_agent.txt"
    if deps_file.exists():
        if not run_command(f"pip install -r {deps_file}", "Installing dependencies"):
            return False
    else:
        print("⚠️  Shared dependencies file not found, installing from local requirements.txt")
        if not run_command("pip install -r requirements.txt", "Installing dependencies from requirements.txt"):
            return False

    # Copy environment file
    env_example = current_dir / "env.example"
    env_file = current_dir / ".env"

    if env_example.exists() and not env_file.exists():
        shutil.copy(env_example, env_file)
        print("📋 Copied environment configuration file")
        print("⚠️  Please edit .env file with your actual configuration values")
    elif env_file.exists():
        print("📋 Environment file already exists")

    # Create basic configuration files
    config_files = {
        "config/settings.yaml": {
            "google_youtube_agent": {
                "channel_id": "${YOUTUBE_CHANNEL_ID}",
                "default_privacy": "public",
                "auto_optimization": True,
                "analytics_cache_hours": 24
            },
            "mcp": {
                "server_url": "${MCP_YOUTUBE_SERVER_URL}",
                "timeout_seconds": 30,
                "retry_attempts": 3
            },
            "ai": {
                "provider": "openai",  # or "anthropic"
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 2000
            }
        },
        "config/logging.yaml": {
            "version": 1,
            "formatters": {
                "detailed": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "detailed"
                },
                "file": {
                    "class": "logging.FileHandler",
                    "level": "DEBUG",
                    "filename": "logs/google_youtube_agent.log",
                    "formatter": "detailed"
                }
            },
            "root": {
                "level": "INFO",
                "handlers": ["console", "file"]
            }
        }
    }

    import yaml
    for config_file, config_data in config_files.items():
        config_path = current_dir / config_file
        if not config_path.exists():
            with open(config_path, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False)
            print(f"📄 Created configuration file: {config_file}")

    # Make scripts executable
    scripts = ["setup.py"]
    for script in scripts:
        script_path = current_dir / script
        if script_path.exists():
            script_path.chmod(0o755)

    # Test basic imports
    print("🧪 Testing basic imports...")
    try:
        import fastapi
        import streamlit
        import aiohttp
        import pandas
        print("✅ Core dependencies imported successfully")
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

    print("\n🎉 YouTube Agent setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit the .env file with your configuration")
    print("2. Set up YouTube MCP server (see MCP setup instructions)")
    print("3. Run the agent: streamlit run app/interface/streamlit_app.py")
    print("4. Or start API server: python -m uvicorn app.main:app --reload")

    return True

if __name__ == "__main__":
    success = setup_youtube_agent()
    sys.exit(0 if success else 1)
