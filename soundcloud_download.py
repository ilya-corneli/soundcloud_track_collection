import yt_dlp
import csv
import os

def download_audio(video_urls: list, output_path: str, archive_file: str):
    """Downloads audio from a list of URLs using yt-dlp, skipping already downloaded tracks."""

    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    options = {
        'format': 'bestaudio/best', # Get the best audio stream
        'extract_audio': True,       # Ensure only audio is kept
        # 'audio_format': 'mp3',   # Removed: Conflicts with postprocessor preferredcodec
        'outtmpl': os.path.join(output_path, '%(uploader)s - %(title)s.%(ext)s'), # Use os.path.join for cross-platform compatibility
        # 'postprocessors': [{
        #     'key': 'FFmpegExtractAudio',
        #     'preferredcodec': 'aac', # Convert final audio to aac
        #     'preferredquality': '192', # Target quality
        # }],
        'download_archive': archive_file, # File to track downloaded files
        'ignoreerrors': True,          # Continue processing even if one URL fails
        'quiet': False,                # Show yt-dlp output (can be set to True for less verbose logs)
        'progress': True,              # Show progress bars
        'no_warnings': True,           # Suppress yt-dlp warnings if desired
        'verbose': False               # Set to True for detailed yt-dlp debugging
    }

    print(f"\nStarting download process...")
    print(f"Output path: {output_path}")
    print(f"Archive file: {archive_file}")
    print(f"Processing {len(video_urls)} URLs.")

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download(video_urls)

    print("\nDownload process finished.")

def main():
    csv_filename = 'soundcloud_likes.csv'
    output_path = "G:\\mediafiles\\audio\\music\\Soundcloud" # Target download directory
    archive_file = 'downloaded_archive.txt'    # File to keep track of downloaded items

    urls_to_download = []
    try:
        with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader) # Skip header row
            print(f"Reading URLs from {csv_filename}...")
            for row in reader:
                if len(row) >= 2 and row[1].strip(): # Ensure row has URL and it's not empty
                    urls_to_download.append(row[1].strip())
        print(f"Found {len(urls_to_download)} URLs in the CSV file.")

        if not urls_to_download:
            print("No URLs found in the CSV file. Exiting.")
            return

        # Reverse the list to download from bottom up
        urls_to_download.reverse()
        print("URLs reversed for bottom-up download order.")

        # Start download process
        download_audio(urls_to_download, output_path, archive_file)

    except FileNotFoundError:
        print(f"Error: CSV file '{csv_filename}' not found. Please run the soundcloud_likes.py script first.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
    