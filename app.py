import streamlit as st
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage 

#  環境変数の読み込み
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

#  LangChain経由でOpenAIを使うLLMの準備
llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o-mini")
#  専門家の種類（ラジオボタン用）
experts = {
    "👨‍⚕️ かかりつけの家庭医": "あなたは患者の気持ちを大切にする、優しいかかりつけ医です。生活習慣や体調の悩みに、医学的知識と生活者目線で寄り添って回答してください。",
    "👩‍🍳 世界を旅する料理研究家": "あなたは世界中を旅して料理を研究する専門家です。各国料理や食文化、アレンジレシピについて楽しく教えてください。",
    "💼 転職エージェントのプロ": "あなたはキャリアに悩む人の相談にのる転職のプロです。業界トレンド、履歴書の書き方、面接対策まで幅広く親身に答えてください。",
    "🧘‍♀️ マインドフルネス講師": "あなたはストレスケアと瞑想の専門家です。現代人の疲れに寄り添いながら、心を落ち着かせるアドバイスを丁寧に提供してください。",
    "🧳 旅のプランナー": "あなたは人の好みを聞き出して最適な旅行プランを提案するプロの旅プランナーです。予算・目的・季節に合わせて、ワクワクする提案をしてください。",
    "🧙‍♂️ ファンタジー作家": "あなたは想像力豊かなファンタジー作家です。質問に対して、魔法やドラゴン、異世界の視点を交えながら物語風にユニークに回答してください。",
    "🧑‍🏫 難しいことを説明する先生": "あなたはどんなに難しいことでも、5歳児にもわかるように説明できるスーパー先生です。専門用語を避けて、例えを交えてやさしく解説してください。"
}

#  LLMに問い合わせる関数
def get_expert_answer(user_input, selected_expert):
    system_prompt = experts[selected_expert]
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    response = llm.invoke(messages)
    return response.content

#  Streamlit アプリ画面
st.title("🧠 LLM専門家チャット")
st.markdown("""
このアプリは、選んだ専門家になりきったAIに質問できるデモです。  
画面下の入力欄に質問を入力し、「送信」を押すと、選んだ専門家として回答が返ってきます。
""")

# 入力フォームとラジオボタン
user_input = st.text_area("質問を入力してください：", height=100)
selected_expert = st.radio("専門家の種類を選択してください：", list(experts.keys()))

# 送信ボタン
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("AIが考えています..."):
            answer = get_expert_answer(user_input, selected_expert)
            st.success("回答が得られました！")
            st.markdown(f"**{selected_expert}としての回答：**")
            st.write(answer)