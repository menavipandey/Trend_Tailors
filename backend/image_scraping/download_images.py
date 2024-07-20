import requests
import os

def download_images(outfits, output_folder):
    # Create the directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for i, url in enumerate(outfits, start=1):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Save the image file
                file_path = os.path.join(output_folder, f"outfit_{i}.jpg")
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                    print(f"Downloaded {url} as {file_path}")
            else:
                print(f"Failed to download {url}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
    # List of image URLs (replace these with the URLs you have collected)
    outfits = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
        "https://example.com/image3.jpg",
        # Add more URLs here
    ]

    # Output folder to save the images
    output_folder = "downloaded_outfits"

    # Download and save the images
    download_images(outfits, output_folder)