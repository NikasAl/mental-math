#!/usr/bin/env python3 
import sys
from mv_api import MindVectorAPI
from mv_screens import ScreenManager

def main():
    try:
        api = MindVectorAPI()
        screens = ScreenManager(api)
        
        if screens.ensure_auth():
            screens.flow_main_menu()
            
    except KeyboardInterrupt:
        print("\n👋 Bye!")
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")

if __name__ == "__main__":
    main()
