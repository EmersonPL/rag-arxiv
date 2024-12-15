from io import BytesIO

import yaml

from pkgutil import get_data


def get_prompt_template() -> tuple[str, str]:
    """Return the System prompt and the user prompt, loaded from a yml file."""
    template = BytesIO(get_data(__package__, "template.yml"))
    prompt_template = yaml.safe_load(template)

    system_prompt = prompt_template["system_prompt"]
    prompt = prompt_template["prompt"]

    return system_prompt, prompt
