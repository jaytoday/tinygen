from typing import List
import re
from decouple import config

MAX_PLANNING_ATTEMPTS = config("MAX_PLANNING_ATTEMPTS", 2, cast=int)
SUCCESS_SCORE_THRESHOLD = config("SUCCESS_SCORE_THRESHOLD", 7, cast=int)  # out of 10
MAX_CHARACTERS_PER_CHUNK = config("MAX_CHARACTERS_PER_CHUNK", 10000, cast=int)


def chunk_file_contents(repo_contents: str) -> List[str]:
    
    # break up repo_contents into chunks of MAX_CHARACTERS_PER_CHUNK
    # do not split up files into multiple chunks unless the entire file is larger than MAX_CHARACTERS_PER_CHUNK

    current_chunk = ""
    all_chunks = []
    
    for file_content in repo_contents.split("\n--- File: "):

        if file_content == "":
            continue
        else:
            file_content = f"\n--- File: {file_content}"

        # Check if the file is empty using regex pattern
        # An empty file will have its own dedicated chunk
        empty_file_match = re.fullmatch(r"\n--- File: .+ ---\n", file_content)
        if empty_file_match:
            # If there's a current chunk, save it first
            if current_chunk:
                all_chunks.append(current_chunk)
                current_chunk = ""
                
            all_chunks.append(file_content)
            continue
        
        # If adding this file content exceeds the max chunk size, add current chunk to all_chunks
        if len(current_chunk) + len(file_content) > MAX_CHARACTERS_PER_CHUNK:
            all_chunks.append(current_chunk)
            current_chunk = ""
        
        # If the file itself is larger than the max chunk size, it needs to be its own chunk
        if len(file_content) > MAX_CHARACTERS_PER_CHUNK:
            # If there's a current chunk, save it first
            if current_chunk:
                all_chunks.append(current_chunk)
                current_chunk = ""
            
            all_chunks.append(file_content)
        else:
            # Otherwise, append this file's content to the current chunk
            if current_chunk:
                current_chunk += "\n---\n"
            current_chunk += file_content
    
    # Add any remaining content as a chunk
    if current_chunk:
        all_chunks.append(current_chunk)
        
    return all_chunks