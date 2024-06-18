#Detailed Version of the QA Approach from Hugging Face#
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

import torch
# question_answerer = pipeline("question-answering")
context = "ENSIAS, the National School of Computer Science and Systems Analysis, is a premier engineering institution located in Rabat, Morocco. Founded in 1992, ENSIAS offers a diverse range of undergraduate and graduate programs covering computer science, information technology, and systems analysis. With nine distinct study fields available to engineering students starting from the second year, ENSIAS provides a tailored educational experience catering to various interests and career paths. These study fields include GL, IDSIT, IDF, BI&A, GD, 2IA, SSI, 2SCL, and SSE. These study fields are Business Intelligence & Analytics (BI&A), Data Engineering (GD), Software Engineering (GL), Engineering in Data Science and IoT (IDSIT), Digital Engineering for Finance (IDF), Artificial Intelligence Engineering (2IA), Information Systems Security (SSI), Smart Supply Chain & Logistics (2SCL), and Smart System Engineering (SSE). Admission to ENSIAS is highly competitive and is determined by performance in the national entrance exam for engineering schools in Morocco. ENSIAS boasts state-of-the-art facilities, a rigorous academic curriculum, and numerous opportunities for research and entrepreneurship. Under the leadership of Ms. Ilham Berrada, who assumed the role of director in 2020, the school remains dedicated to fostering innovation, diversity, and excellence in education and research."
question = "where is ENSIAS?"
# question_answerer(question=question, context=context)
model_checkpoint = "distilbert-base-cased-distilled-squad"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForQuestionAnswering.from_pretrained(model_checkpoint)

inputs = tokenizer(question, context, return_tensors="pt")
outputs = model(**inputs)
start_logits = outputs.start_logits
end_logits = outputs.end_logits
# print(start_logits.shape, end_logits.shape)

sequence_ids = inputs.sequence_ids()
# Mask everything apart from the tokens of the context
mask = [i != 1 for i in sequence_ids]
# Unmask the [CLS] token and question tokens
mask[0] = False
mask = torch.tensor(mask)[None]

start_logits[mask] = -10000
end_logits[mask] = -10000
# Now that we have properly masked the logits corresponding to positions we don’t want to predict, we can apply the softmax:
start_probabilities = torch.nn.functional.softmax(start_logits, dim=-1)[0]
end_probabilities = torch.nn.functional.softmax(end_logits, dim=-1)[0]

scores = start_probabilities[:, None] * end_probabilities[None, :]
scores = torch.triu(scores)

max_index = scores.argmax().item()
start_index = max_index // scores.shape[1]
end_index = max_index % scores.shape[1]
print(scores[start_index, end_index])


inputs_with_offsets = tokenizer(question, context, return_offsets_mapping=True)
offsets = inputs_with_offsets["offset_mapping"]

start_char, _ = offsets[start_index]
_, end_char = offsets[end_index]
answer = context[start_char:end_char]


result = {
    "answer": answer,
    "start": start_char,
    "end": end_char,
    "score": scores[start_index, end_index],
}
print(result)
