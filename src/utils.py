from typing import Literal




def decide_tool_for_question(question: str) -> Literal['db','web']:
	"""Very simple heuristic to route question: if it contains words about numbers/statistics, prefer DB.

	This is naive: in production use an LLM classifier.
	"""
	q = question.lower()
	data_words = ["average","mean","median","count","how many","what is the","percentage","percent","distribution","std","stddev","correlation","correlate","rows","samples","value","statistic","frequency"]
	medical_words = ["symptom","symptoms","treatment","cure","definition","what is","causes","risk factor","signs","diagnosis","diagnose","how to treat"]
	if any(w in q for w in data_words):
		return 'db'
	if any(w in q for w in medical_words):
		return 'web'

	return 'web'