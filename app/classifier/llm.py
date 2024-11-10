import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import logging
import re


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# model_name = "Qwen/Qwen2.5-7B-Instruct"
model_name = "Qwen/Qwen2.5-0.5B-Instruct"

def load_llm(model_name=model_name):
    tokenizer = AutoTokenizer.from_pretrained(
        model_name
    )
    logger.info(f"Loading model '{model_name}'...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        device_map='auto', 
        torch_dtype=torch.float16
    )
    logger.info("Model loaded successfully.")

    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

    return generator


def extract_from_response(tmp):
    fault_point_pattern = r'"Приоритет":\s*"([^"]*)"'
    fault_point = re.search(fault_point_pattern, tmp)
    
    result = {
        "Приоритет": fault_point.group(1) if fault_point else "Средний"
    }
    
    return result