from typing import List, Dict

from app.lib.codegen.utils import SUCCESS_SCORE_THRESHOLD

EXAMPLE_CODE_DIFF = '''
diff --git a/src/main.py b/src/main.py
index 58d38b6..23b0827 100644
--- a/src/main.py
+++ b/src/main.py
@@ -19,7 +19,10 @@ def run_bash_file_from_string(s: str):
     """Runs a bash script from a string"""
     with open('temp.sh', 'w') as f:
         f.write(s)
-    os.system('bash temp.sh')
+    if os.name == 'nt':  # Windows systems
+        os.system('powershell.exe .\\temp.sh')
+    else:  # Unix/Linux systems
+        os.system('bash temp.sh')
     os.remove('temp.sh')
'''


def generate_review_and_plan_prompt(
        prompt: str,
        repo_file_map: Dict,
        code_diff: str,
        steps: List[str]
) -> str:
    """Generate a review and plan prompt based on various input parameters.

    Args:
        prompt (str): The user prompt.
        repo_file_map (Dict): The repository file map.
        code_diff (str): The previously generated code difference.
        steps (List[str]): The previously generated steps.

    Returns:
        str: The generated review and plan prompt.
    """
    return f"""Generate a review and plan for implementing a code diff based on the provided user prompt.

    Call the get_codegen_review_and_plan function with the following parameters:
    - review: None if the previously generated code diff is an empty string, or a CodeGenReview object with the following fields:
        - score: an integer between 0 and 10 (inclusive) representing the quality of the code diff. A score of 7 indicates the code diff is an acceptable implementation of the provided prompt. 
        - comment: a string with more detailed feedback describing the quality of the code diff and why the score was given. 
    - plan: None if the generated review score is at least {SUCCESS_SCORE_THRESHOLD}, or a CodeGenPlan object with the following fields:
        - steps: a list of strings describing the steps needed to implement the code diff to best satisfy the provided prompt. Return an empty list if no steps are needed or if unable to determine the steps needed.
        - file_paths: a list of strings representing file paths from the Repository File Map that need to be modified to implement a code diff satisfying the provided prompt. The file paths should be relative to the root of the repository, and include any files if unsure if they should be included so they can be further examined. If the plan requires new files to be created, include the paths and filenames of the new files to be created. Return an empty list if no files need to be modified or if unable to determine the files needed.

    User Prompt:
    ```
    {prompt}
    ```

    Previously Generated Code Diff:
    ```
    {code_diff}
    ```

    Previously Generated Steps:
    ```
    {steps}
    ```

    Repository File Map:
    ```
    {repo_file_map}
    ```

    If the code diff above is an empty string or steps is an empty array, the "review" value should be None.

    If the generated review score is at least {SUCCESS_SCORE_THRESHOLD}, the "plan" value should be None.

    """  # noqa: E501


def generate_code_diff_prompt(content_chunk: str, steps: List[str]) -> str:
    """Generate a code diff prompt based on a code chunk and steps.

    Args:
        content_chunk (str): The content chunk.
        steps (List[str]): The list of steps.

    Returns:
        str: The generated code diff prompt.
    """
    return f"""Generate a code diff for the provided code chunk based on the provided steps. Return an empty string if no code diff is needed.

The code diff should use the same format as this example code diff:
```
{EXAMPLE_CODE_DIFF}
```

Code Chunk:
```
{content_chunk}
```

Steps:
```
{steps}
```
    """  # noqa: E501
