import os
import shutil
import random
from collections import defaultdict

def create_directory(path):
    """
    Creates a directory if it doesn't exist.
    """
    os.makedirs(path, exist_ok=True)

def get_all_classes(dataset_dir):
    """
    Retrieves all class names from the train directory.
    Assumes that each class has its own subdirectory in train.
    """
    train_dir = os.path.join(dataset_dir, 'train')
    classes = [d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))]
    return classes

def collect_videos(dataset_dir, classes):
    """
    Collects all video file paths for each class from both train and test directories.
    
    Returns:
    - A dictionary with class names as keys and lists of video file paths as values.
    """
    video_dict = defaultdict(list)
    for class_name in classes:
        # Paths for current class in train and test
        train_class_dir = os.path.join(dataset_dir, 'train', class_name)
        test_class_dir = os.path.join(dataset_dir, 'test', class_name)
        
        # Collect videos from train
        if os.path.exists(train_class_dir):
            for file in os.listdir(train_class_dir):
                file_path = os.path.join(train_class_dir, file)
                if os.path.isfile(file_path):
                    video_dict[class_name].append(file_path)
        
        # Collect videos from test
        if os.path.exists(test_class_dir):
            for file in os.listdir(test_class_dir):
                file_path = os.path.join(test_class_dir, file)
                if os.path.isfile(file_path):
                    video_dict[class_name].append(file_path)
                    
    return video_dict

def split_videos(video_list, train_ratio=0.8):
    """
    Splits the video list into train and test lists based on the specified ratio.
    
    Parameters:
    - video_list: List of video file paths.
    - train_ratio: Proportion of videos to include in the train split.
    
    Returns:
    - train_videos: List of video file paths for training.
    - test_videos: List of video file paths for testing.
    """
    total = len(video_list)
    train_size = int(total * train_ratio)
    random.shuffle(video_list)
    train_videos = video_list[:train_size]
    test_videos = video_list[train_size:]
    return train_videos, test_videos

def move_videos(videos, destination_dir):
    """
    Moves video files to the specified destination directory.
    
    Parameters:
    - videos: List of video file paths.
    - destination_dir: Directory where videos will be moved.
    """
    create_directory(destination_dir)
    for src_path in videos:
        filename = os.path.basename(src_path)
        dest_path = os.path.join(destination_dir, filename)
        try:
            shutil.move(src_path, dest_path)
            print(f"Moved {src_path} to {dest_path}")
        except Exception as e:
            print(f"Error moving {src_path} to {dest_path}: {e}")

def count_samples(dataset_dir, classes):
    """
    Counts the number of samples per class in train and test directories.
    
    Returns:
    - train_counts: Dictionary with class names as keys and train sample counts as values.
    - test_counts: Dictionary with class names as keys and test sample counts as values.
    """
    train_counts = defaultdict(int)
    test_counts = defaultdict(int)
    
    for class_name in classes:
        train_class_dir = os.path.join(dataset_dir, 'train', class_name)
        test_class_dir = os.path.join(dataset_dir, 'test', class_name)
        
        if os.path.exists(train_class_dir):
            train_counts[class_name] = len([f for f in os.listdir(train_class_dir) if os.path.isfile(os.path.join(train_class_dir, f))])
        
        if os.path.exists(test_class_dir):
            test_counts[class_name] = len([f for f in os.listdir(test_class_dir) if os.path.isfile(os.path.join(test_class_dir, f))])
    
    return train_counts, test_counts

def main():
    # Set random seed for reproducibility
    random.seed(42)
    
    # Define paths
    current_dir = os.getcwd()
    dataset_dir = os.path.join(current_dir, 'Dataset')
    
    # Check if Dataset directory exists
    if not os.path.exists(dataset_dir):
        print(f"Error: Dataset directory '{dataset_dir}' does not exist.")
        return
    
    # Get all class names
    classes = get_all_classes(dataset_dir)
    if not classes:
        print("Error: No classes found in the train directory.")
        return
    
    print(f"Found {len(classes)} classes.")
    
    # Collect all videos
    print("\nCollecting all video files...")
    video_dict = collect_videos(dataset_dir, classes)
    
    # Prepare directories
    print("\nPreparing directories for split...")
    for split in ['train', 'test']:
        for class_name in classes:
            class_dir = os.path.join(dataset_dir, split, class_name)
            create_directory(class_dir)
    
    # Initialize counters
    summary = {
        'train': defaultdict(int),
        'test': defaultdict(int)
    }
    
    # Split and move videos
    print("\nSplitting and moving videos...")
    for class_name, videos in video_dict.items():
        if not videos:
            print(f"Warning: No videos found for class '{class_name}'. Skipping.")
            continue
        
        train_videos, test_videos = split_videos(videos, train_ratio=0.8)
        
        # Define destination directories
        train_dest = os.path.join(dataset_dir, 'train', class_name)
        test_dest = os.path.join(dataset_dir, 'test', class_name)
        
        # Move train videos
        move_videos(train_videos, train_dest)
        summary['train'][class_name] = len(train_videos)
        
        # Move test videos
        move_videos(test_videos, test_dest)
        summary['test'][class_name] = len(test_videos)
    
    # Count samples after split
    print("\nCounting samples after split...")
    train_counts, test_counts = count_samples(dataset_dir, classes)
    
    # Display summary
    print("\n=== Split Summary ===\n")
    print("Class\tTrain Samples\tTest Samples")
    print("------------------------------------------")
    for class_name in classes:
        train_count = train_counts.get(class_name, 0)
        test_count = test_counts.get(class_name, 0)
        print(f"{class_name}\t{train_count}\t\t{test_count}")
    
    print("\nDataset splitting complete.")

if __name__ == "__main__":
    main()
