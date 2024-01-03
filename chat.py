from os import getenv
import re
import openai
from time import time, sleep
from halo import Halo
import textwrap
import yaml
from utils import save_file, open_file
from chatbot import chatbot
import marvin
from marvin import ai_fn

# marvin.settings.llm_model = "openai/gpt-3.5-turbo"
marvin.settings.llm_temperature = 0.1
# marvin.settings.openai.api_base = "https://openrouter.ai/api/v1/chat/completions"
# marvin.settings.openai.api_key = getenv("OPENROUTER_API_KEY")
marvin.settings.llm_model = "openai/gpt-4-1106-preview"


def chat_print(text):
    formatted_lines = [
        textwrap.fill(line, width=120, initial_indent="    ", subsequent_indent="    ")
        for line in text.split("\n")
    ]
    formatted_text = "\n".join(formatted_lines)
    print("\n\n\nCHATBOT:\n\n%s" % formatted_text)


def ask_for_context():
    context = input("Please provide the context for the article: ")
    return context


@ai_fn
def generate_title_and_outline(context: str) -> str:
    """
    Generates a title and outline for an article based on the provided `context`.
    """


@ai_fn
def generate_article_content(title_and_outline: str) -> str:
    """
    Generates the content of an article based on the provided `title_and_outline`.
    """


@ai_fn
def split_into_parts(article_content: str) -> list[str]:
    """
    Splits `article_content` into multiple article chapters, each with a title and content.
    """


@ai_fn
def add_links_and_details(section: str) -> str:
    """
    Adds reference links, image placeholders, and styling improvements(like quotation, list, bold, italic, etc.) to a given `section` of text.
    """


@ai_fn
def adjust_tone_and_style(section: str) -> str:
    """
    ## RULES:
    - Enhance creativity by using idiomatic expressions and unique styles.
    - Incorporate personal anecdotes to add a human touch, as AI lacks personal experiences.
    - Ensure cohesion so that text flows logically and connects ideas well.
    - Capture sentiment nuances which AI may struggle with, especially in complex emotional contexts.
    - Maintain consistency to avoid the randomness that can occur in AI-generated text.
    - Structure content with short paragraphs, white spaces, and images for better readability.
    - Diversify vocabulary, avoid repetition, and use conversational language to engage readers.
    - Paraphrase AI-generated content to ensure uniqueness and match the brand's tone and style.
    - Use "in the style of" prompts to tailor AI outputs to a specific voice or perspective.
    - Add human-like elements to make AI content more conversational and natural.
    - Introduce intentional variations in writing to bypass AI detection while avoiding errors.
    - Regularly update strategies to keep pace with evolving AI tools and maintain content quality.
    - Prioritize ethical use of AI, ensuring content quality and value, and avoid spreading misinformation.
    - Fact-check all AI-generated content to prevent the dissemination of inaccuracies.
    - Use machine learning tools and natural language processing to refine AI-generated text.
    - Paraphrase AI output and rewrite for a natural flow, removing non-human patterns and odd transitions.
    - Adjust the focus of AI-generated content by omitting or adding information where necessary.
    - Recognize that human post-editing is crucial to fully humanize AI text, as tools alone are insufficient.
    - Incorporate personal stories, idioms, varied sentence structures, and humor to humanize AI content.
    - Use tools like Grammarly for natural language and paraphrasing tools like GPTInf to enhance text.
    - Understand that no AI can fully replicate human writing; the best results come from enhancing AI with human input.
    - Aim for unique and insightful AI content that adheres to Google's helpful content system.
    - Customize AI models and ensure contextual relevance for content that appears human-written.
    - Avoid predictable patterns by using randomness and diverse data sources in AI-generated content.
    - Manually edit AI content to adjust syntax, vary sentence lengths, and employ higher-level vocabulary for authenticity.
    - Balance sophistication with readability to ensure the audience's understanding of the content.

    ## TASK:
    Adjusts the tone and style of a given `section` following the rules above.
    """


if __name__ == "__main__":
    import logging

    logging.basicConfig(
        filename="chat.log",
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(message)s",
    )

    context = ask_for_context()
    logging.info("Context received for article generation.")
    title_and_outline = generate_title_and_outline(context)
    logging.info("Title and outline generated.")
    article_content = generate_article_content(title_and_outline)
    logging.info("Article content generated.")
    sections = split_into_parts(article_content)
    logging.info(f"Article content split into {len(sections)} sections.")

    from utils import read_prompt_from_file

    outline_prompt = read_prompt_from_file("prompts/3_outline_prompt.txt")
    logging.info("Outline prompt read from file.")
    brainstorm_prompt = read_prompt_from_file("prompts/4_brainstorm_prompt.txt")
    logging.info("Brainstorm prompt read from file.")
    expanded_outline_prompt = read_prompt_from_file(
        "prompts/5_expanded_outline_prompt.txt"
    )
    logging.info("Expanded outline prompt read from file.")
    draft_prompt = read_prompt_from_file("prompts/6_draft_prompt.txt")
    logging.info("Draft prompt read from file.")

    prompts = [outline_prompt, brainstorm_prompt, expanded_outline_prompt, draft_prompt]
    new_sections = []

    for section in sections:
        logging.info(f"Processing {section}")
        conversation = []
        new_section = section
        for p in prompts:
            conversation.append(
                {"role": "user", "content": f"Section:\n{section}\n\nPrompt:\n{p}"},
            )
            logging.info("Added user prompt to conversation.")
            print("\n\n\nUSER: %s" % p)
            print(f"\nConversing with chatbot... {conversation}")
            response, tokens = chatbot(conversation)
            conversation.append({"role": "assistant", "content": response})
            logging.info("Received chatbot response.")
            print("\n\n\nCHATBOT:\n%s" % response)
            new_section = response

        new_section = add_links_and_details(new_section)
        new_section = adjust_tone_and_style(new_section)
        new_sections.append(new_section)
        logging.info("Section tone and style adjusted.")

    article_content = "\n\n".join(new_sections)
    save_file("output.txt", article_content)
    logging.info("Article content saved to output.txt.")
