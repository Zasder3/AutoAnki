import os
import getpass


def main():
    # Check if SECRET file exists
    if os.path.exists("SECRET"):
        overwrite = input(
            "SECRET file already exists. Do you want to overwrite it? (y/n): "
        )
        overwrite = overwrite.lower()

        if overwrite == "n":
            print("Exiting...")
            return
    # Ask user for GPT-3.5 API key
    secret = getpass.getpass("Enter your GPT-3.5 API key: ")
    # Write secret to file
    with open("SECRET", "w") as f:
        f.write(secret)


if __name__ == "__main__":
    main()
