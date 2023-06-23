from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_path = "neverLife/nllb-200-distilled-600M-ja-zh"
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path, src_lang="jpn_Jpan", tgt_lang="zho_Hans")


def translate(text):
    input_ids = tokenizer.encode(text, max_length=128, padding=True, return_tensors='pt')
    outputs = model.generate(input_ids, num_beams=4, max_new_tokens=128)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)