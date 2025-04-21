import ujson

# Define the path
LOCAL_SETTINGS_FILE = "fermenter_settings.ujson"


def debug_json_file():
    try:
        # First, let's try reading the raw bytes
        print("=== Reading raw bytes ===")
        with open(LOCAL_SETTINGS_FILE, "rb") as f:
            raw_content = f.read()
            print("Raw bytes length:", len(raw_content))
            print("First 50 bytes:", raw_content[:50])
            print()

        # Now read as text and check content
        print("=== Reading as text ===")
        with open(LOCAL_SETTINGS_FILE, "r") as f:
            text_content = f.read()
            print("Text length:", len(text_content))
            print("First 50 characters:", text_content[:50])
            print()

        # Try parsing with ujson
        print("=== Attempting JSON parse ===")
        try:
            with open(LOCAL_SETTINGS_FILE, "r") as f:
                json_content = ujson.load(f)
                print("Successfully parsed JSON!")
                print("Keys found:", list(json_content.keys()))
                print("Number of key-value pairs:", len(json_content))
        except Exception as e:
            print("JSON parsing error:", str(e))
            print("Error type:", type(e))

    except Exception as e:
        print("File reading error:", str(e))
        print("Error type:", type(e))


# Run the debug function
if __name__ == "__main__":
    print("Starting JSON file debug")
    print("Target file:", LOCAL_SETTINGS_FILE)
    print("-" * 40)
    debug_json_file()
