from transformers import MarianMTModel, MarianTokenizer
import logging

# Local fine-tuned model paths
custom_models = {
    "Hindi": "Collab EN to HI/my_en_hi_model",
    "Bengali": "Collab EN to BN/my_en_bn_model"
}

# Cache to avoid reloading models repeatedly
loaded_models = {}

def load_model(language):
    """
    Loads the tokenizer and model for the given language.
    Uses a cached version if already loaded.
    """
    if language not in loaded_models:
        model_path = custom_models.get(language)
        if not model_path:
            raise ValueError(f"Unsupported language: {language}")
        
        try:
            tokenizer = MarianTokenizer.from_pretrained(model_path)
            model = MarianMTModel.from_pretrained(model_path)
            loaded_models[language] = (tokenizer, model)
        except Exception as e:
            logging.error(f"Error loading model for {language}: {str(e)}")
            raise Exception(f"Error loading model for {language}: {str(e)}")
    
    return loaded_models[language]

def translate_text(text, language):
    """
    Translates the given English text into the specified language.
    """
    try:
        tokenizer, model = load_model(language)
    except ValueError as e:
        raise e  # Re-raise to be caught by Flask error handler
    except Exception as e:
        logging.error(f"Error loading the model: {str(e)}")
        raise Exception(f"Error loading the model: {str(e)}")
    
    try:
        # Tokenize input
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

        # Generate translated output
        outputs = model.generate(**inputs)

        # Decode to readable text
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translated_text
    except Exception as e:
        logging.error(f"Translation error: {str(e)}")
        raise Exception(f"Translation error: {str(e)}")

# For standalone testing (optional)
if __name__ == "__main__":
    sample = "Good morning!"
    lang = "Hindi"
    translated = translate_text(sample, lang)
    print(f"English: {sample}")
    print(f"{lang}: {translated}")
