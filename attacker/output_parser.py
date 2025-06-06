import base64

def process_file(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    processed_lines = []
    for line_num, line in enumerate(lines, 1):
        
        if ':' in line:
            # Split at last occurrence of ':' (after timestamp)
            parts = line.rsplit(':', 1)
            if len(parts) == 2:
                prefix, encoded_part = parts
                encoded_clean = encoded_part.split('\n')[0].strip().strip('"').strip("'")
                
                try:
                    # Add padding if needed
                    padding_needed = len(encoded_clean) % 4
                    if padding_needed:
                        encoded_clean += '=' * (4 - padding_needed)
                    
                    decoded = base64.b64decode(encoded_clean).decode('utf-8')
                    
                    processed_line = f"{prefix}: {decoded}\n"
                    processed_lines.append(processed_line)
                except Exception as e:
                    processed_lines.append(line)
            else:
                processed_lines.append(line)
        else:
            processed_lines.append(line)
    
    return processed_lines


def parse(filename):

    processed = process_file(filename)
    with open(filename, 'w') as out_file:
        out_file.writelines(processed)

    



