from hex import Params


def run(params: Params) -> dict[str, str]:
    print("ECHO:", params.inputs["message"])
    return {}
