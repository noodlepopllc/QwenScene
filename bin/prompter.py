import ollama, sys, argparse
qwen = "alibayram/Qwen3-30B-A3B-Instruct-2507:latest"
gemma = "gemma3:27b"
llava = "llava:34b"


def main(template, images, prompt, model, host):
    client = ollama.Client(host=f'http://{host}:11434')
    client.generate(model=model, keep_alive=0)
    # Build messages in the correct hierarchy
    messages = [
        {
            "role": "system",
            "content": template
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    # Attach images to the user message (Qwen3-VL expects this)
    if images:
        messages[1]["images"] = images

    # Call Ollama with expanded context
    response = client.chat(
        model=model,
        messages=messages,
        options={
            'num_ctx': 64000,
            'keep_alive': 1
        }
    )

    return response


if __name__ == '__main__':
    models = {"qwen": qwen, "gemma": gemma, "llava": llava}

    parser = argparse.ArgumentParser(
        prog='Create prompts',
        description='Create video or image prompts',
        epilog=''
    )

    parser.add_argument('-t', '--template', type=str, default=None, help='user template')
    parser.add_argument('-i', '--image', action='append', help='image(s) to use (repeat flag for multiple images)')
    parser.add_argument('-p', '--prompt', type=str, default='', help='user prompt')
    parser.add_argument('-P', '--fileprompt', action='append',  help='user prompt(s) in a file (repeat flag for multiple prompts)')
    parser.add_argument('-G', '--globaltemplate', type=str, default=None, help='top level to be included')
    parser.add_argument('-m', '--model', type=str, default='qwen', help='model [qwen, gemma, llava]')
    parser.add_argument('-H', '--host', type=str, default='192.168.1.178', help='host ollama server is on')

    args = parser.parse_args()

    # Load global template
    g_template = ''
    if args.globaltemplate is not None:
        with open(args.globaltemplate, 'r') as fp:
            g_template = fp.read()

    # Load template
    template = ''
    if args.template is not None:
        with open(args.template, 'r') as fp:
            template = fp.read()

    # Combine templates
    template = g_template + template

    # Load prompt
    prompt = ''

    if args.fileprompt is not None:
        for pr in args.fileprompt:
            with open(pr, 'r') as fp:
                prompt += fp.read() + '\n'

    prompt = prompt + args.prompt

    # Images list (or None)
    images = args.image if args.image else None

    # Run
    response = main(template, images, prompt, models[args.model], args.host)

    print(response["message"]['content'])

