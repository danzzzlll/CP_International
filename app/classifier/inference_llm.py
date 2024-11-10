from .llm import load_llm, extract_from_response
from .prompts import Prompts
from .prompt_format import message



pipeline = load_llm()

def get_priority(theme: str, description: str):
    prompt = Prompts.request_prompt
    message_ = message
    message_[1]['content'] = prompt + " " + theme + " " + description

    full_prompt = pipeline.tokenizer.apply_chat_template(
            message_, tokenize=False, add_generation_prompt=True)

    output = pipeline(full_prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    assistant_marker_index = output[0]["generated_text"].find('<|assistant|>')
    response = output[0]["generated_text"][assistant_marker_index + len('<|assistant|>'):].strip()
    answer = extract_from_response(response)
    return answer["Приоритет"]

