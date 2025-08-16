import zlib
import os

def compress_file(input_file):
    # Read the file data
    with open(input_file, 'rb') as f:
        file_data = f.read()
    
    # Compress the data
    compressed_data = zlib.compress(file_data)
    
    # Create a new file name with .zip extension
    compressed_file_name = f"{input_file}.zip"
    
    # Write the compressed data to a new file
    with open(compressed_file_name, 'wb') as f:
        f.write(compressed_data)
    
    print(f"Compressed {input_file} to {compressed_file_name}")

def main():
    # Get user input for file to compress
    input_file = input("Enter the path of the file to compress: ")
    
    if os.path.isfile(input_file):
        compress_file(input_file)
    else:
        print("Invalid file path. Please try again.")

if __name__ == "__main__":
    main()