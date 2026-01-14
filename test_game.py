"""
Test script to validate game.py structure and components without requiring a camera.
This script performs static analysis and basic unit tests.
"""

import sys
import ast

def test_imports():
    """Test that all required imports can be identified in the code"""
    print("Testing imports...")
    with open('game.py', 'r') as f:
        content = f.read()
    
    required_imports = ['pygame', 'cv2', 'mediapipe', 'random', 'sys']
    for imp in required_imports:
        if imp in content:
            print(f"  ✓ {imp} import found")
        else:
            print(f"  ✗ {imp} import NOT found")
            return False
    return True

def test_class_structure():
    """Test that all required classes are defined"""
    print("\nTesting class structure...")
    with open('game.py', 'r') as f:
        tree = ast.parse(f.read())
    
    required_classes = ['HandTracker', 'Player', 'Ball', 'RedCard', 'Game']
    found_classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    
    for cls in required_classes:
        if cls in found_classes:
            print(f"  ✓ Class {cls} defined")
        else:
            print(f"  ✗ Class {cls} NOT defined")
            return False
    return True

def test_game_constants():
    """Test that game constants are defined"""
    print("\nTesting game constants...")
    with open('game.py', 'r') as f:
        content = f.read()
    
    required_constants = [
        'WINDOW_WIDTH', 'WINDOW_HEIGHT', 'FPS',
        'PLAYER_WIDTH', 'PLAYER_HEIGHT',
        'BALL_RADIUS', 'RED_CARD_WIDTH', 'RED_CARD_HEIGHT',
        'INITIAL_HEALTH', 'SPAWN_INTERVAL', 'FALL_SPEED'
    ]
    
    for const in required_constants:
        if const in content:
            print(f"  ✓ Constant {const} defined")
        else:
            print(f"  ✗ Constant {const} NOT defined")
            return False
    return True

def test_main_function():
    """Test that main function exists"""
    print("\nTesting main function...")
    with open('game.py', 'r') as f:
        tree = ast.parse(f.read())
    
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    if 'main' in functions:
        print("  ✓ Main function defined")
        return True
    else:
        print("  ✗ Main function NOT defined")
        return False

def test_syntax():
    """Test Python syntax validity"""
    print("\nTesting Python syntax...")
    try:
        with open('game.py', 'r') as f:
            ast.parse(f.read())
        print("  ✓ Syntax is valid")
        return True
    except SyntaxError as e:
        print(f"  ✗ Syntax error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Running Game Validation Tests")
    print("="*60)
    
    tests = [
        test_syntax,
        test_imports,
        test_class_structure,
        test_game_constants,
        test_main_function
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed! Game structure is valid.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
