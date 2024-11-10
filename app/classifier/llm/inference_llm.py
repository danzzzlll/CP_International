from .llm import load_llm, extract_from_response
from .prompts import Prompts
from .prompt_format import message

# Загружаем модель LLM
pipeline = load_llm()

def get_priority(theme: str, description: str):
    # Получаем шаблон подсказки
    prompt = Prompts.request_prompt
    # Копируем шаблон сообщения
    message_ = message
    # Формируем контент сообщения, объединяя подсказку, тему и описание
    message_[1]['content'] = prompt + " " + theme + " " + description

    # Применяем шаблон чата к сообщению для токенизации
    full_prompt = pipeline.tokenizer.apply_chat_template(
        message_, tokenize=False, add_generation_prompt=True)

    # Генерируем ответ, используя параметры для настройки случайности
    output = pipeline(full_prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    
    # Находим индекс метки ответа "<|assistant|>" в сгенерированном тексте
    assistant_marker_index = output[0]["generated_text"].find('<|assistant|>')
    # Извлекаем текст после метки и убираем пробелы
    response = output[0]["generated_text"][assistant_marker_index + len('<|assistant|>'):].strip()
    
    # Извлекаем значение "Приоритет" из ответа
    answer = extract_from_response(response)
    return answer["Приоритет"]
