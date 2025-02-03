# ai-test-generator/ai_engine/prompt_manager/prompt_composer.py

from jinja2 import Template


class PromptComposer:
    """
    Composes prompts using Jinja2 templating.

    This class is responsible for rendering a given template string with
    the provided context data.
    """

    def compose(self, template_str: str, context: dict) -> str:
        """
        Renders the provided template string using the given context.

        :param template_str: A Jinja2 template as a string.
        :param context: A dictionary of values to substitute into the template.
        :return: A rendered prompt string.
        """
        try:
            template = Template(template_str)
            rendered_prompt = template.render(**context)
            return rendered_prompt
        except Exception as e:
            raise RuntimeError(f"Failed to render template: {e}") from e


# --- Example Usage ---
# if __name__ == "__main__":
#     sample_template = (
#         "Generate tests for the API titled '{{ spec.title }}'. "
#         "The endpoints to cover are: {{ spec.endpoints | tojson }}."
#     )
#     context = {
#         "spec": {
#             "title": "User API",
#             "endpoints": [
#                 {"path": "/login", "method": "POST"},
#                 {"path": "/logout", "method": "POST"}
#             ]
#         }
#     }
#     composer = PromptComposer()
#     prompt = composer.compose(sample_template, context)
#     print("Rendered Prompt:")
#     print(prompt)
