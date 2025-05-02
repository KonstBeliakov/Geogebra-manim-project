from openai import OpenAI

from create_header_list import extract_function_headers_and_docs


with open('open_ai_key', 'r', encoding='utf-8') as f:
    key = f.read()

list_of_functions = extract_function_headers_and_docs()
usage_examples = 'There is no usage examples yet.'

# I tried to parse math book for 7 grade automatically, but I didn't manage to do it yet.
task_description = '''
Дано:
ABC - равнобедренный треугольник.
АМ и BN биссектрисы угла.
Доказать: AM = BN.
'''

prompt = f'''
I need to create an animation solving a geometry problem using a list of functions I have written for geometric animations.

```python
{list_of_functions}
```

Here are a few examples of how these functions are used:

```python
{usage_examples}
```

Here is the task description:

```
{task_description}
```
Don't write anything other than the python solution, as in the example.
Comments (outside the code) and descriptions of how you solved the problem are unnecessary.'''

client = OpenAI(api_key=key)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

solution = completion.choices[0].message.content


with open('generation_attempt/prompt.md', 'w', encoding='utf-8') as file:
    file.write(prompt)

print(solution)
with open('generation_attempt/solution.py', 'w', encoding='utf-8') as file:
    file.write(solution)
