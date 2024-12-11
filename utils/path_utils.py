import os

def get_project_root():
    """Get the absolute path to the project root directory"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_data_file_path(filename: str) -> str:
    """
    Get the absolute path for a data file
    
    Args:
        filename: Name of the file in the dataFiles directory
    
    Returns:
        str: Absolute path to the file
    """
    root_dir = get_project_root()
    data_dir = os.path.join(root_dir, "dataFiles")
    
    # Create dataFiles directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    return os.path.join(data_dir, filename) 