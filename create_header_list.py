import ast


def get_type_name(annotation):
    """Extracting a complex type from annotation"""
    if isinstance(annotation, ast.Name):
        return annotation.id
    elif isinstance(annotation, ast.Subscript):
        value = get_type_name(annotation.value)
        slice_ = get_type_name(annotation.slice)
        return f"{value}[{slice_}]"
    elif isinstance(annotation, ast.Tuple):
        return f"({', '.join([get_type_name(elt) for elt in annotation.elts])})"
    elif isinstance(annotation, ast.BinOp):
        # for unions of types (for example: str | Figure)
        left = get_type_name(annotation.left)
        right = get_type_name(annotation.right)
        return f"{left} | {right}"
    return "Any"


def extract_function_headers_and_docs(input_file='utils.py'):
    with open(input_file, 'r') as f:
        code = f.read()

    tree = ast.parse(code)

    function_details = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            docstring = ast.get_docstring(node) or "No documentation"

            args = []
            for arg in node.args.args:
                arg_type = None
                if arg.annotation:
                    arg_type = get_type_name(arg.annotation)
                args.append(f"{arg.arg}: {arg_type if arg_type else 'Any'}")

            args_str = ",\n\t".join(args)

            function_details.append(f"{func_name}({args_str})\n'''{docstring}'''\n")

    #with open(output_file, 'w') as f:
    #    f.write("\n".join(function_details))

    return "\n".join(function_details)
