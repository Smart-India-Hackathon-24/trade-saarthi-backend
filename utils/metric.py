import random
import csv
import sys
import os
import asyncio
# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Now import the required modules
from app import unified_endpoint
def select_random_titles_from_csv(file_path):
    # Read titles from CSV
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        titles = [row[1] for row in reader]  # Assuming titles are in the first column

    if len(titles) < 15000:
        raise ValueError("The CSV file must contain at least 15,000 titles.")

    selected_titles = []

    for i in range(0, len(titles), 300):
        batch = titles[i:i+100]  # Take 100 consecutive titles
        selected_titles.append(random.choice(batch))  # Select one random title

    return selected_titles

def write_titles_to_file(titles, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("\n".join(titles))



# Example usage
# file_path = '../dataFiles/final.csv'  # Replace with the path to your CSV file
# output_file="titles.txt"
# result = select_random_titles_from_csv(file_path)
# write_titles_to_file(result,output_file)
# print(result)

async def check_with_apis(file_name,output_csv):
    # with open(file_name,encoding='utf-8') as f:
    #     title=f.read()
    #     print(title)
    with open(file_name, encoding='utf-8') as f:
        titles = f.read().splitlines()
    
    header = [
        'Title', 
        'Restricted Words Check',
        'Restricted Prefix/Suffix Check', 
        'Title Combination Check', 
        'Space No Space Check', 
        'Minimum Title Length Check', 
        'Special Characters Check',
        'Same Title Probability',
        'Similar Title Probability', 
        'Similar Sounding Title Probability'
        ]
    
    output_data = []
    
    for title in titles:
        try:
    
            result =await  unified_endpoint(title)
            print(result)
            same_title_prob = result.get('results', {}).get('Same Title', {}).get('rejectance probability', 'N/A')
            similar_title_prob = result.get('results', {}).get('Similar Title', {}).get('rejectance probability', 'N/A')
            similar_sound_prob = result.get('results', {}).get('Similar Sounding Title', {}).get('rejectance probability', 'N/A')
            
            # Extract validation results
            final_output = result.get('final_output', {})
            
            # Prepare row data
            row_data = [
                title,
                final_output.get('RESTRICTED WORDS', 'N/A'),
                final_output.get('RESTRICTED PREFIX/SUFFIX', 'N/A'),
                final_output.get('TITLE COMBINATION', 'N/A'),
                final_output.get('SPACE NO_SPACE', 'N/A'),
                final_output.get('CHECK MINIMUM TITLE LENGTH', 'N/A'),
                final_output.get('CHECK SPECIAL CHARACTERS', 'N/A'),
                same_title_prob,
                similar_title_prob,
                similar_sound_prob
            ]
            
            output_data.append(row_data)
            # output_data.append([title,result["final_output"]])
        except Exception as e:

            output_data.append([title, f"Error: {str(e)}"])
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)
        csv_writer.writerow(['Title', 'API Result'])
        csv_writer.writerows(output_data)
    
    print(f"Results written to {output_csv}")

# check_with_apis("titles.txt","output.csv")
async def main():
    
    output_file = "test_titles.txt"
    # output_file = "titles.txt"
    output_csv = "test_output.csv"

    await check_with_apis(output_file, output_csv)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())