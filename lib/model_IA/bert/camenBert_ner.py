from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

def get_city_name(input_user: str) -> list:
    """
    get the city from the input_user
    using camenBert model. based on bert model finetuned for french lexique => camenBert
    NER with CamemBERT: The camembert-ner model has been specifically fine-tuned for the task of Named Entity Recognition (NER)
    using annotated data for this task. This means it has been trained to identify and classify named entities in French texts.
    
    user_input : user request :string
    return : list
    """
    tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
    model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")
    nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    city = nlp(input_user)
    return [loc['word'].lower().capitalize() for loc in city if loc['entity_group']=='LOC'] # can have city and region, we want to try both to get the city


