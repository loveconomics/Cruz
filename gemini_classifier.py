import pandas as pd
import numpy as np
import time
from google import genai

df = pd.read_csv('PATH_NAME_TO_YOUR_DATA')

# Replace "YOUR_API_KEY" with your actual Gemini API key
# Get key from Google: https://ai.google.dev/gemini-api/docs/api-key
client = genai.Client(api_key="YOUR_API_KEY")

# Model 
def rank_award_descriptions(data, criteria="strong"):
    """
    Ranks award descriptions based on specified criteria.

    Args:
        data: Pandas DataFrame with an "AWARD DESCRIPTIONS" column.
        criteria: "strong" or any other value (defaults to "strong").

    Returns:
        Pandas DataFrame with added "RANK" and "REASONING" columns.
    """

    if criteria == "strong":
        criteria_text = "social justice, radical left values, woke culture, diversity, inclusion, equality, Marxism"
    else:
        criteria_text = "neutral science, military technology, national security"

    data["RANK"] = 0  # Initialize rank column
    data["REASONING"] = ""  # Initialize reasoning column

    for index, row in data.iterrows():
        description = row["AWARD DESCRIPTIONS"]

        prompt = f"""
        Rank the following award description from 1 to 5 based on its alignment with the following criteria: {criteria_text}.

        Award Description: {description}

        Respond with only the rank (a single integer from 1 to 5) followed by a short explanation (a few words) of why you assigned that rank.  Separate the rank and the reasoning with a comma.  For example:

        3, Moderately aligned with social justice themes.
        """

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )

            # Extract rank and reasoning. Handle potential errors in response format.
            try:
                rank_str, reasoning = response.text.strip().split(",", 1)
                rank = int(rank_str.strip())  # Convert rank to integer
                reasoning = reasoning.strip()
                if 1 <= rank <= 5: #check if rank is in the correct range
                    data.loc[index, "RANK"] = rank
                    data.loc[index, "REASONING"] = reasoning
                else:
                    data.loc[index, "REASONING"] = "Invalid Rank from LLM"
                time.sleep(3)
            
                
            except ValueError:
                data.loc[index, "REASONING"] = "Invalid LLM Response Format"
                print(f"Error processing response for: {description}")  # Print for debugging

            
            

        except Exception as e:
            data.loc[index, "REASONING"] = f"API Error: {e}"
            print(f"API Error for: {description}: {e}") # Print for debugging

    return data

ranked_data = rank_award_descriptions(df)