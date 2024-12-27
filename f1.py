import pandas as pd
import matplotlib.pyplot as plt

def calculate_avg_f1(file_path):
    """
    Calculate the average F1 score from a results.csv file.
    """
    # Load the CSV file
    data = pd.read_csv(file_path)
    
    # Extract precision and recall columns (ensure column names match the CSV)
    precision = data['   metrics/precision']  # Replace with exact column name for precision
    recall = data['      metrics/recall']    # Replace with exact column name for recall
    
    # Calculate F1 Score for each epoch
    f1_scores = 2 * (precision * recall) / (precision + recall)
    
    # Calculate and return the average F1 score
    return f1_scores.mean()

# List of file paths for results.csv
file_paths = ['C:/Users/rawat/Documents/proramming/final_ocr/yolov5/yolov5-training/invoice_experiment4/results.csv','C:/Users/rawat/Documents/proramming/final_ocr/yolov5/yolov5-training/experiment14/results.csv',
              'C:/Users/rawat/Documents/proramming/final_ocr/yolov5/runs/train/exp/results.csv'  # Add more file paths as needed
]

# List to store average F1 scores
avg_f1_scores = []
labels = []  # Labels for the bars

# Calculate average F1 scores for each file
for i, file_path in enumerate(file_paths):
    avg_f1 = calculate_avg_f1(file_path)
    avg_f1_scores.append(avg_f1)
    labels.append(f'Experiment {i + 1}')  # Label each bar as "Experiment 1", "Experiment 2", etc.

# Plot the bar graph
plt.figure(figsize=(10, 6))
plt.bar(labels, avg_f1_scores, color='skyblue')
plt.xlabel('Experiments')
plt.ylabel('Average F1 Score')
plt.title('Average F1 Score Across Multiple Experiments')
plt.ylim(0, 1)  # Assuming F1 Score ranges from 0 to 1
plt.tight_layout()

# Show the plot
plt.show()
