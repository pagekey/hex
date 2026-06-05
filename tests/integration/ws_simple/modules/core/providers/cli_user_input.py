from hex import Params


def run(params: Params) -> dict[str, str]:
    prompt = params.inputs["prompt"]
    print(f"{prompt}: ", end="")
    user_input = input()
    return {"user_input": user_input}
