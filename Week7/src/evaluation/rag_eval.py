def faithfulness_score(answer, context):
    answer_words = set(answer.lower().split())
    context_words = set(context.lower().split())

    overlap = len(answer_words & context_words)
    score = overlap / max(len(answer_words), 1)

    return round(score, 3)


def hallucination_detected(answer, context):
    answer_words = set(answer.lower().split())
    context_words = set(context.lower().split())

    overlap = len(answer_words & context_words)

    if overlap < 3:
        return True
    return False
