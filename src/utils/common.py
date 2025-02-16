import yaml
import re
import json

from src.utils.logger import logging


def read_yaml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)  
        return data
    except FileNotFoundError:
        logging.info(f"Error: The file {file_path} was not found.")
    except yaml.YAMLError as exc:
        logging.info(f"Error parsing YAML file: {exc}")
    except Exception as e:
        logging.info(f"An error occurred: {e}")


def find_valid_json(data):
    for i in range(-1, -len(data.history) - 1, -1): 
        try:
            extracted_content = str(data.history[i].result[0].extracted_content)
            if "```json" in extracted_content:
                return extracted_content  
        except (KeyError, IndexError, TypeError) as e:
            continue 

    return None  


def post_process_result(data):
    match = re.search(r'```json\n(.*?)\n```', data, re.DOTALL)
    if match:
        json_str = match.group(1)  
        data_dict = json.loads(json_str)  
        return data_dict
    else:
        return None


def write_json_to_text(data, output_text_file):
    try:
        first_transaction = data.get("First Transaction", "Unknown Date")
        wallet_age = data.get("Wallet Age", "Unknown Age")
        category = data.get("Category", "Unknown Category")
        analysis = data.get("Analysis", "No Analysis Available")

        formatted_text = f"""\
            First Transaction: {first_transaction}
            Wallet Age: {wallet_age}
            Category: {category}
            Analysis: {analysis}
            """
        with open(output_text_file, 'w', encoding='utf-8') as f:
            f.write(formatted_text)
        
        logging.info(f"Data successfully written to {output_text_file}")

    except Exception as e:
        logging.info(f"Error: {e}")


def save_trend_analysis_to_file(trend_results, conclusion, filename):
    with open(filename, "w") as file:
        file.write("30-Day Trend:\n")
        file.write(f"- Overall change: {trend_results['30_day_trend']['overall_change']}\n")
        file.write(f"- Notable changes: {trend_results['30_day_trend']['notable_changes']}\n")
        file.write(f"- Transaction patterns: {trend_results['30_day_trend']['transaction_patterns']}\n")

        file.write("\n90-Day Trend:\n")
        file.write(f"- Overall change: {trend_results['90_day_trend']['overall_change']}\n")
        file.write(f"- Notable changes: {trend_results['90_day_trend']['notable_changes']}\n")
        file.write(f"- Transaction patterns: {trend_results['90_day_trend']['transaction_patterns']}\n")

        file.write("\n180-Day Trend:\n")
        file.write(f"- Overall change: {trend_results['180_day_trend']['overall_change']}\n")
        file.write(f"- Notable changes: {trend_results['180_day_trend']['notable_changes']}\n")
        file.write(f"- Transaction patterns: {trend_results['180_day_trend']['transaction_patterns']}\n")

        file.write("\nConclusion:\n")
        file.write(conclusion)

    logging.info(f"Trend analysis results saved to {filename}")