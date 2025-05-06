from transformers import MarianMTModel, MarianTokenizer
import logging

# Flag: Use pretrained models (True) or custom fine-tuned models (False)
usePretrained = False

# Pretrained Hugging Face models
pretrained_models = {
    "English to Hindi": "Helsinki-NLP/opus-mt-en-hi",
    "English to Bengali": "shhossain/opus-mt-en-to-bn",
    "English to Marathi": "Helsinki-NLP/opus-mt-en-mr",
    "Hindi to English": "Helsinki-NLP/opus-mt-hi-en",
    "Bengali to English": "Helsinki-NLP/opus-mt-bn-en",
    "Marathi to English": "Helsinki-NLP/opus-mt-mr-en"
}

# Custom fine-tuned models (local)
custom_models = {
    "English to Hindi": "Collab EN to HI/my_en_hi_model",
    "English to Bengali": "Collab EN to BN/my_en_bn_model",
    "English to Marathi": "Collab EN to MR/my_en_mr_model",
    "Hindi to English": "Collab HI to EN/my_hi_en_model",
    "Bengali to English": "Collab BN to EN/my_bn_en_model",
    "Marathi to English": "Collab MR to EN/my_mr_en_model"
}

# Cache loaded models
loaded_models = {}

def load_model(language_pair):
    """
    Load the model and tokenizer for the selected language pair.
    Uses a cached version if already loaded.
    """
    if language_pair not in loaded_models:
        # Get model path for pretrained or custom model
        model_path = pretrained_models.get(language_pair) if usePretrained else custom_models.get(language_pair)
        
        if not model_path:
            raise ValueError(f"Unsupported language pair: {language_pair}")

        try:
            # Load tokenizer and model
            tokenizer = MarianTokenizer.from_pretrained(model_path)
            model = MarianMTModel.from_pretrained(model_path)

            # Set pad_token to avoid warning
            tokenizer.pad_token = tokenizer.eos_token
            
            loaded_models[language_pair] = (tokenizer, model)
        except Exception as e:
            logging.error(f"Error loading model for {language_pair}: {str(e)}")
            raise Exception(f"Error loading model for {language_pair}: {str(e)}")

    return loaded_models[language_pair]

def translate_text(text, source_lang, target_lang):
    """
    Translate input text from source_lang to target_lang.
    """
    try:
        # Construct the language pair string, e.g., "English to Hindi"
        language_pair = f"{source_lang} to {target_lang}"

        # Load the appropriate model for the language pair
        tokenizer, model = load_model(language_pair)
    except ValueError as e:
        raise e
    except Exception as e:
        logging.error(f"Model loading failed: {str(e)}")
        raise Exception(f"Model loading failed: {str(e)}")

    try:
        # Tokenize input text
        inputs = tokenizer([text], return_tensors="pt", padding=True, truncation=True)

        # Generate translated output
        output_tokens = model.generate(**inputs)

        # Decode the tokens back to a string, skipping special tokens including padding
        translated_text = tokenizer.decode(output_tokens[0], skip_special_tokens=True)
        
        # Remove any remaining pad token if needed
        translated_text = translated_text.replace("<pad>", "").strip()

        return translated_text

    except Exception as e:
        logging.error(f"Translation error: {str(e)}")
        raise Exception(f"Translation error: {str(e)}")


# For standalone testing (optional)
if __name__ == "__main__":
    sample = "Good morning!"
    source_language = "English"
    target_language = "Hindi"
    
    # Translate from English to Hindi
    translated = translate_text(sample, source_language, target_language)
    print(f"Original: {sample}")
    print(f"Translated ({source_language} to {target_language}): {translated}")
