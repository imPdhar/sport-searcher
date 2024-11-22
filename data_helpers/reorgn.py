import os
import shutil
import pandas as pd
from collections import defaultdict

def create_directory(path):
    """
    Creates a directory if it doesn't exist.
    """
    os.makedirs(path, exist_ok=True)

def find_video(video_name, source_dirs):
    """
    Searches for the video in the provided source directories.

    Parameters:
    - video_name: Name of the video file to find.
    - source_dirs: List of directories to search in.

    Returns:
    - The path to the video if found, else None.
    """
    for source_dir in source_dirs:
        potential_path = os.path.join(source_dir, video_name)
        if os.path.exists(potential_path):
            return potential_path
    return None

def organize_dataset(csv_file, target_dir, source_dirs, split_name, class_counts):
    """
    Organizes videos into class-specific directories based on the CSV mapping.

    Parameters:
    - csv_file: Path to the CSV file containing video names and their classes.
    - target_dir: Directory where the organized videos will be placed.
    - source_dirs: List of directories where the original videos might be stored.
    - split_name: Name of the split ('train' or 'test') for logging purposes.
    - class_counts: Dictionary to keep count of samples per class.
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Iterate over each row in the CSV
    for index, row in df.iterrows():
        video_name = row['video_name'].strip()
        class_name = row['tag'].strip()
        
        # Define class directory
        class_dir = os.path.join(target_dir, class_name)
        create_directory(class_dir)
        
        # Search for the video in the provided source directories
        src_path = find_video(video_name, source_dirs)
        
        if src_path is None:
            print(f"Warning: {video_name} not found in any of the source directories. Skipping.")
            continue
        
        # Define destination path
        dest_path = os.path.join(class_dir, video_name)
        
        # Move the video file
        try:
            shutil.move(src_path, dest_path)
            print(f"Moved {src_path} to {dest_path}")
            class_counts[split_name][class_name] += 1
        except Exception as e:
            print(f"Error moving {src_path} to {dest_path}: {e}")

def count_samples(directory):
    """
    Counts the number of samples per class in the given directory.

    Parameters:
    - directory: Path to the directory (train or test).

    Returns:
    - A dictionary with class names as keys and sample counts as values.
    """
    counts = defaultdict(int)
    if not os.path.exists(directory):
        return counts
    
    for class_name in os.listdir(directory):
        class_dir = os.path.join(directory, class_name)
        if os.path.isdir(class_dir):
            counts[class_name] = len([file for file in os.listdir(class_dir) if os.path.isfile(os.path.join(class_dir, file))])
    return counts

def main():
    # Define paths
    current_dir = os.getcwd()
    dataset_dir = os.path.join(current_dir, 'Dataset')
    
    # Paths for original splits
    train_source = os.path.join(current_dir, 'train')
    test_source = os.path.join(current_dir, 'test')
    
    # Paths for CSV files
    train_csv = os.path.join(current_dir, 'train.csv')
    test_csv = os.path.join(current_dir, 'test.csv')
    
    # Define target directories
    train_target = os.path.join(dataset_dir, 'train')
    test_target = os.path.join(dataset_dir, 'test')
    
    # Create Dataset/train and Dataset/test directories
    create_directory(train_target)
    create_directory(test_target)
    
    # Dictionary to keep count of samples per class
    class_counts = {
        'train': defaultdict(int),
        'test': defaultdict(int)
    }
    
    print("Organizing training data...")
    organize_dataset(
        csv_file=train_csv,
        target_dir=train_target,
        source_dirs=[train_source, test_source],  # Search in both train and test
        split_name='train',
        class_counts=class_counts
    )
    
    print("\nOrganizing testing data...")
    organize_dataset(
        csv_file=test_csv,
        target_dir=test_target,
        source_dirs=[train_source, test_source],  # Search in both train and test
        split_name='test',
        class_counts=class_counts
    )
    
    # Display summary of samples
    print("\nDataset reorganization complete.\n")
    print("Sample counts per class:")
    
    print("\nTraining Set:")
    train_counts = count_samples(train_target)
    if train_counts:
        for class_name, count in train_counts.items():
            print(f"  {class_name}: {count} samples")
    else:
        print("  No samples found in training set.")
    
    print("\nTesting Set:")
    test_counts = count_samples(test_target)
    if test_counts:
        for class_name, count in test_counts.items():
            print(f"  {class_name}: {count} samples")
    else:
        print("  No samples found in testing set.")

if __name__ == "__main__":
    main()
