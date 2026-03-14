"""
Simple server test - starts server and keeps it running
"""
import uvicorn
from main import app

if __name__ == "__main__":
    print("=" * 60)
    print("Starting EV Charging Scheduler Backend")
    print("=" * 60)
    print()
    print("Server starting on http://127.0.0.1:8001")
    print("API Docs: http://localhost:8001/docs")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        uvicorn.run(app, host="127.0.0.1", port=8001, reload=False, log_level="info")
    except Exception as e:
        print(f"\nERROR: {e}")
        input("\nPress Enter to exit...")
