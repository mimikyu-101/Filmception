# summary translator
from transformers import MarianMTModel, MarianTokenizer
import os

# Supported language models
LANGUAGE_MODELS = {
    "ur": "Helsinki-NLP/opus-mt-en-ur",
    "ar": "Helsinki-NLP/opus-mt-en-ar",
    "ko": "Helsinki-NLP/opus-mt-tc-big-en-ko"
}

# Load and cache models + tokenizers
def load_model_and_tokenizer(target_lang):
    model_name = LANGUAGE_MODELS[target_lang]
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return model, tokenizer

# Translate one sentence
def translate_text(text, model, tokenizer):
    inputs = tokenizer([text], return_tensors="pt", padding=True)
    translated_tokens = model.generate(**inputs)
    return tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

# Translate a list of texts and write to file
def translate_and_save(texts, target_lang, output_dir="translations"):
    print(f"Translating to {target_lang}...")
    os.makedirs(output_dir, exist_ok=True)
    model, tokenizer = load_model_and_tokenizer(target_lang)

    translated_list = []
    for i, text in enumerate(texts, 1):
        translated = translate_text(text, model, tokenizer)
        translated_list.append(translated)
        print(f"Translated [{i}/{len(texts)}]")

    # Save to file
    filename = os.path.join(output_dir, f"translations_{target_lang}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        for translation in translated_list:
            f.write(translation + "\n")

    print(f"Saved {len(texts)} translations to {filename}")
    return translated_list

# Main function to be called with text and target language
def translate_texts(texts, target_lang):
    """
    Translate a list of texts to the target language.
    
    Args:
        texts (list): List of strings to be translated
        target_lang (str): Target language code (ur, ar, or ko)
    
    Returns:
        list: List of translated texts
    """
    if target_lang not in LANGUAGE_MODELS:
        raise ValueError(f"Unsupported target language. Supported languages are: {list(LANGUAGE_MODELS.keys())}")
    
    return translate_and_save(texts, target_lang)

# Example usage:
if __name__ == "__main__":
    # Sample texts
    sample_texts = [
        "A young boy discovers he has magical powers and attends a school for wizards.",
        "A detective investigates a series of mysterious murders in a small town.",
        "An astronaut is stranded on Mars and must find a way to survive until rescue."
    ]
    
    # Translate to Urdu
    urdu_translations = translate_texts(sample_texts, "ur")
    
    # Translate to Arabic
    arabic_translations = translate_texts(sample_texts, "ar")
    
    # Translate to Korean
    korean_translations = translate_texts(sample_texts, "ko")