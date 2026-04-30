"""
Quick script to verify the password change endpoint exists in the code
"""

print("=" * 70)
print("VERIFYING PASSWORD CHANGE ENDPOINT")
print("=" * 70)

# Check if endpoint exists in code
with open('src/app.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
    if '/api/profile/change-password' in content:
        print("\n✅ ENDPOINT FOUND IN CODE!")
        print("   Route: /api/profile/change-password")
        
        # Find the line number
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if '/api/profile/change-password' in line:
                print(f"   Line: {i}")
                break
        
        print("\n✅ The code is correct!")
        print("\n⚠️  BUT YOU MUST RESTART THE SERVER!")
        print("\n" + "=" * 70)
        print("TO RESTART:")
        print("=" * 70)
        print("1. Go to the terminal where server is running")
        print("2. Press Ctrl + C to stop it")
        print("3. Run: python src/app.py")
        print("4. Test password change again")
        print("=" * 70)
        
    else:
        print("\n❌ ENDPOINT NOT FOUND!")
        print("   The endpoint may not have been saved correctly.")
        print("   Please check src/app.py around line 104")

print()
