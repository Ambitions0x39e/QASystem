import os
import pandas as pd
from text2vec import SentenceModel
from sklearn.metrics.pairwise import cosine_similarity

# Globals
_model = None
_texts = None
_text_embeddings = None

def match_intent(query, q_amount=3):
    global _model, _texts, _text_embeddings

    # Initialize once
    if _model is None:
        _model = SentenceModel('shibing624/text2vec-base-chinese')

    if _texts is None or _text_embeddings is None:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        df = pd.read_csv(os.path.join(BASE_DIR, 'options.csv'))
        _texts = df['taskName'].astype(str).tolist()
        _text_embeddings = _model.encode(_texts)

    # Encode query
    query_embedding = _model.encode([query])
    scores = cosine_similarity(query_embedding, _text_embeddings)[0]
    top_indices = scores.argsort()[-q_amount:][::-1]
    top_texts = [_texts[i] for i in top_indices]
    top_scores = [scores[i] for i in top_indices]

    return top_texts, top_scores

# CLI 测试
if __name__ == "__main__":
    print(">>> 快速意图匹配系统（输入exit()退出）")
    while True:
        print("请输入意图表达：", end="")
        user_input = input()
        if user_input.lower() == 'exit()':
            break
        match_text, score = match_intent(user_input)
        for i in range(len(match_text)):
            print(f"→ 匹配语句: {match_text[i]}")
            print(f"→ 相似度得分: {score[i] :.4f}\n")
