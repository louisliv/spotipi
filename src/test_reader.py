from mfrc522 import SimpleMFRC522

def main():
    reader = SimpleMFRC522()
    try:
        while True:
            id, text = reader.read()
            print("Card Value is:", id)
    finally:
        reader.close()

if __name__ == "__main__":
    main()