#!/usr/bin/env python3
"""
Mental Math Trainer - CLI Client
Точка входа
"""
import sys
from mm_api import MentalMathAPI
from mm_screens import ScreenManager


def main():
    try:
        api = MentalMathAPI()
        screens = ScreenManager(api)
        
        if screens.ensure_auth():
            screens.flow_main_menu()
            
    except KeyboardInterrupt:
        print("\n👋 До встречи!")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
