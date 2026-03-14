"""
Debug Server Startup Script
Shows detailed errors and keeps window open
"""

import sys
import traceback
import uvicorn
from main import app

def main():
    print("=" * 60)
    print("EV Charging Scheduler - Backend Debug Server")
    print("=" * 60)
    print()
    
    try:
        print("Starting server on http://0.0.0.0:8000")
        print("API Documentation: http://localhost:8000/docs")
        print()
        print("Press Ctrl+C to stop")
        print("=" * 60)
        print()
        
        # Start uvicorn with detailed logging
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print()
        print("=" * 60)
        print("ERROR: Server failed to start!")
        print("=" * 60)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print()
        print("Full traceback:")
        print("-" * 60)
        traceback.print_exc()
        print("-" * 60)
        print()
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
