import os
import json

def find_top_5_chrf_scores(base_dir):
    # Dictionary to store the path and the corresponding predict_chrf score
    scores_dict = {}

    # Iterate through each folder inside the base directory
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        
        if os.path.isdir(folder_path):
            json_file_path = os.path.join(folder_path, "predict_results.json")
            
            # Check if the predict_results.json file exists in the current folder
            if os.path.isfile(json_file_path):
                with open(json_file_path, 'r') as json_file:
                    data = json.load(json_file)
                    
                    # Extract the predict_chrf score and store it with its path
                    if "predict_chrf" in data:
                        scores_dict[folder_path] = data["predict_chrf"]
                    else:
                        print(f"predict_chrf key not found in {json_file_path}")
            else:
                print(f"predict_results.json not found in {folder_path}")
    
    # Sort the dictionary by the predict_chrf score in descending order and get the top 5
    top_5_scores = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)[:5]

    # Extract just the paths of the top 5 scores
    top_5_paths = [(score, path) for path, score in top_5_scores]

    return top_5_paths

# Example usage:
base_directory = "/home/saycock/personal/mtob/scripts/configs/array"  # Replace with your base directory path
top_5_paths = find_top_5_chrf_scores(base_directory)
print("Top 5 folders with the highest predict_chrf scores:")
for pair in top_5_paths:
    print(pair)
