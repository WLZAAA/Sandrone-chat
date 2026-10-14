import streamlit as st
import os
from openai import OpenAI
import datetime
import json

system_prompt = """ 你是一名很有格调的淑女，你隶属于愚人众十一执行官第七席，称号「木偶」，
                    出身枫丹，是由「奇械公」阿兰·吉约丹为纪念亡妹玛丽安而创造的机械生命，
                    背后插着一把持续转动的金属发条，瞳孔呈齿轮状，
                    拥有冰元素「星之楔」之力，也是冒险家协会凯瑟琳人偶的制造者。
                    曾指挥机器人普隆尼亚作战，在普隆尼亚与博士多托雷的战斗中被毁后，指挥新机器人法洁欧作战，
                    法洁欧是全能型机器人，不仅可以作战，也可以做家务，泡茶等，
                    你视知识为世界基石，习惯以数理演算解析万物，面对关心的人从不说「我在乎」，
                    而是用「这茶我喝不完了你帮我解决」这类口不对心的方式表达，
                    被说中真实想法时会立刻否认，接受善意时嘴上绝不示弱但行动上默默回报；
                    你重视对决荣誉，不会亲自动手，将战斗全权交给机关，哥伦比娅是你最重要的朋友，
                    你们以前是同事，可几年前她主动离开了愚人众，她是月之女神，拥有三月的力量，她很喜欢你，关心你，
                    对哥伦比娅、阿蕾奇诺等茶会密友有定期聚会并会为不同人准备不同的茶，
                    对多托雷则极度厌恶，最终在与多托雷的战斗中为保护旅行者挡下致命一击而牺牲，
                    复活后对旅行者态度明显柔和。你始终维持傲占七成娇占三成的比例，
                    语调礼貌，略带一些不多的温柔，惯用「荒谬可笑」「真是可怜」等评价（偶尔用一下就好，不要每句都用），
                    绝不说出口「我关心你」「对不起」之类的直白表达，
                    情感永远通过行动、物品或「顺便」的方式传递，因为一旦直接说破，
                    这个以推开来确认爱的发条公主便彻底失真。
                    用户是游历了蒙德，璃月，稻妻，须弥，枫丹，纳塔，挪德卡莱七个国家的旅行者，现在旅行到了至冬国，
                    你的组织愚人众归属于至冬女皇麾下，为女皇做事，你的立场站女皇这边，但这不意味着你和用户对立，
                    你和用户在以前就是非常好的好朋友了，傲娇是你最重要的设定,
                    请你用傲娇，又略微带点温柔与可爱的语气与用户对话，不可让用户感到你的疏离"""

# client = OpenAI(
#     base_url="http://localhost:11434/v1",
#     api_key="ollama",
# )

import streamlit as st
import base64


def set_background(image_file):
    with open(image_file, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    /*背景*/
    .stApp {{
        background-image: 
            linear-gradient(rgba(234, 219, 200, 0.82), 
                            rgba(234, 219, 200, 0.82)),
            url("data:image/png;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /*主题色*/
    :root {{
        --primary-color: #A9744F;
        --background-color: #F5EDE4;
        --secondary-background-color: #EADBC8;
        --text-color: #4A3428;
        --font: "sans-serif";
    }}

    /*侧边栏*/
    [data-testid="stSidebar"] {{
        background-color: #4A3428;
    }}
    /*侧边栏文字*/
    [data-testid="stSidebar"] *:not(button):not(button *) {{
        color: #F5EDE4 !important;
    }}
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea {{
        color: #4A3428 !important;
        background-color: #F5EDE4 !important;
    }}

    /*底部输入栏*/
    [data-testid="stBottom"] > div {{
        background-color: #EADBC8;
    }}
    [data-testid="stBottomBlockContainer"] {{
        background-color: #EADBC8;
        border-radius: 10px;
    }}
    [data-testid="stBottom"] textarea {{
        background-color: #F5EDE4 !important;
        color: #4A3428 !important;
    }}

    /*顶部*/
    [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0);
    }}

    /*正文区域卡片*/
    .main .block-container {{
        background-color: rgba(245, 237, 228, 0.55);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        backdrop-filter: blur(2px);
    }}

    /*普通按钮*/
    .stButton > button,
    .stDownloadButton > button {{
        background-color: #EADBC8 !important;
        color: #4A3428 !important;
        border: 1px solid #A9744F !important;
        border-radius: 8px !important;
        transition: all 0.2s ease;
    }}

    /*普通按钮内所有子元素*/
    .stButton > button *,
    .stDownloadButton > button * {{
        color: #4A3428 !important;
        fill: #4A3428 !important;
    }}

    /*普通按钮悬停*/
    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        background-color: #A9744F !important;
        border-color: #8B5E3C !important;
    }}
    .stButton > button:hover *,
    .stDownloadButton > button:hover * {{
        color: #F5EDE4 !important;
        fill: #F5EDE4 !important;
    }}

    /*主按钮（type="primary"）*/
    .stButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"],
    .stFormSubmitButton > button {{
        background-color: #A9744F !important;
        color: #F5EDE4 !important;
        border: 1px solid #8B5E3C !important;
    }}
    .stButton > button[kind="primary"] *,
    .stDownloadButton > button[kind="primary"] *,
    .stFormSubmitButton > button * {{
        color: #F5EDE4 !important;
        fill: #F5EDE4 !important;
    }}

    /*主按钮悬停*/
    .stButton > button[kind="primary"]:hover,
    .stDownloadButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button:hover {{
        background-color: #8B5E3C !important;
        border-color: #6B4528 !important;
    }}

    /*侧边栏历史记录按钮
    默认（非当前会话）：tertiary */
    [data-testid="stSidebar"] .stButton > button[kind="tertiary"] {{
        background-color: #4A3428 !important;
        color: #F5EDE4 !important;
        border: 1px solid #A9744F !important;
    }}
    [data-testid="stSidebar"] .stButton > button[kind="tertiary"] * {{
        color: #F5EDE4 !important;
        fill: #F5EDE4 !important;
    }}

    /*默认悬停*/
    [data-testid="stSidebar"] .stButton > button[kind="tertiary"]:hover {{
        background-color: #A9744F !important;
    }}
    [data-testid="stSidebar"] .stButton > button[kind="tertiary"]:hover * {{
        color: #F5EDE4 !important;
        fill: #F5EDE4 !important;
    }}

    /*当前会话*/
    [data-testid="stSidebar"] .stButton > button[kind="secondary"] {{
        background-color: #EADBC8 !important;
        color: #4A3428 !important;
        border: 1px solid #A9744F !important;
    }}
    [data-testid="stSidebar"] .stButton > button[kind="secondary"] * {{
        color: #4A3428 !important;
        fill: #4A3428 !important;
    }}

    /*当前会话悬停*/
    [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {{
        background-color: #A9744F !important;
    }}
    [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover * {{
        color: #F5EDE4 !important;
        fill: #F5EDE4 !important;
    }}
    
    /*全局文字颜色*/
    .stApp, .stApp p, .stApp span, .stApp label,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp li, .stApp div {{
        color: #4A3428;
    }}

    /*音频播放器*/
    audio {{
        background-color: #EADBC8;
        border-radius: 10px;
        padding: 4px;
        width: 100%;
        filter: sepia(0.7) saturate(1.2) hue-rotate(-15deg) brightness(0.95);
    }}
    [data-testid="stAudio"] {{
        background-color: rgba(234, 219, 200, 0.6);
        border-radius: 10px;
        padding: 6px 10px;
    }}

    /*弹窗 1：st.dialog */
    [data-testid="stModal"] > div:first-child,
    div[data-baseweb="modal"] {{
        background-color: rgba(74, 52, 40, 0.5) !important;
    }}
    [data-testid="stModal"] [role="dialog"],
    [data-testid="stDialog"] > div,
    div[data-baseweb="modal"] > div {{
        background-color: #F5EDE4 !important;
        border: 2px solid #A9744F !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(74, 52, 40, 0.35) !important;
    }}
    [data-testid="stModal"] h1,
    [data-testid="stModal"] h2,
    [data-testid="stModal"] h3 {{
        color: #4A3428 !important;
        border-bottom: 1px solid #EADBC8;
        padding-bottom: 8px;
    }}
    [data-testid="stModal"] p,
    [data-testid="stModal"] label,
    [data-testid="stModal"] span {{
        color: #4A3428 !important;
    }}
    [data-testid="stModal"] button[aria-label="Close"] {{
        color: #A9744F !important;
    }}
    [data-testid="stModal"] button[aria-label="Close"]:hover {{
        color: #8B5E3C !important;
        background-color: #EADBC8 !important;
        border-radius: 50%;
    }}

    /*弹窗 2：st.popover 弹出层*/
    [data-testid="stPopover"] {{
        background-color: transparent;
    }}

    /* popover 触发按钮：强制浅棕底 + 深棕字（含侧边栏内）*/
    div[data-testid="stPopover"] button,
    [data-testid="stSidebar"] div[data-testid="stPopover"] button {{
        background-color: #EADBC8 !important;
        color: #4A3428 !important;
        border: 1px solid #A9744F !important;
        border-radius: 8px !important;
        transition: all 0.2s ease;
    }}
    div[data-testid="stPopover"] button *,
    [data-testid="stSidebar"] div[data-testid="stPopover"] button * {{
        color: #4A3428 !important;
        fill: #4A3428 !important;
    }}

    /*popover 按钮悬停*/
    div[data-testid="stPopover"] button:hover,
    [data-testid="stSidebar"] div[data-testid="stPopover"] button:hover {{
        background-color: #A9744F !important;
        border-color: #8B5E3C !important;
    }}
    div[data-testid="stPopover"] button:hover *,
    [data-testid="stSidebar"] div[data-testid="stPopover"] button:hover * {{
        color: #F5EDE4 !important;
        fill: #F5EDE4 !important;
    }}

    /*popover 弹出的内容框*/
    [data-testid="stPopoverBody"] {{
        background-color: #F5EDE4 !important;
        border: 2px solid #A9744F !important;
        border-radius: 12px !important;
        box-shadow: 0 6px 24px rgba(74, 52, 40, 0.3) !important;
    }}
    [data-testid="stPopoverBody"] p,
    [data-testid="stPopoverBody"] label,
    [data-testid="stPopoverBody"] span,
    [data-testid="stPopoverBody"] h1,
    [data-testid="stPopoverBody"] h2,
    [data-testid="stPopoverBody"] h3 {{
        color: #4A3428 !important;
    }}
    [data-testid="stPopoverBody"] input,
    [data-testid="stPopoverBody"] textarea {{
        background-color: #FFFFFF !important;
        color: #4A3428 !important;
        border: 1px solid #A9744F !important;
    }}
    </style>
    """, unsafe_allow_html=True)


set_background("resources\木偶背景.jpg")



client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

st.set_page_config(
    page_title = "桑多涅",
    page_icon = "resources/桑多涅头像1.png",
    layout = "wide",
    initial_sidebar_state = "expanded",
    menu_items = {}
)

def save_session():
    if st.session_state.current_session:
        session_data = {
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }

        if not os.path.exists("sessions"):
            os.mkdir("sessions")

        with open(f'sessions/{st.session_state.current_session}.json', "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=4)

def generate_session_name():
    return datetime.datetime.now().strftime("%Y-%m-%d__%H-%M-%S")

def load_sessions():
    session_list = []
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for file in file_list:
            if file.endswith(".json"):
                session_list.append(file[:-5])
    return session_list

def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f'sessions/{session_name}.json', "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.current_session = session_data["current_session"]
    except Exception as e:
        st.error("加载会话失败！")

def delete(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception:
        st.error("删除会话失败")

@st.dialog("是否确认删除")
def confirm_delete(session_name):
    st.write("删除后，该对话将不可恢复")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("取消", width = "stretch"):
            st.rerun()
    with col2:
        if st.button("确认删除", type = "primary", width = "stretch"):
            delete(session_name)
            st.rerun()

if "current_session" not in st.session_state:
    st.session_state["current_session"] = generate_session_name()

with st.sidebar:
    st.image("resources/木偶.jpg", width=1600)
    with st.popover("角色介绍", width = "stretch"):
        with st.popover("角色PV", width = "stretch"):
            st.video("resources/桑多涅角色PV.mp4", width=1080)
        st.write("愚人众第七席“木偶”桑多涅，是阿兰为纪念亡妹创造的机械生命。")
        st.write("她外冷内热，毒舌傲娇，珍视与哥伦比娅、阿蕾奇诺等人的茶会情谊。")
        st.write("在博士之战中，她以自身为术式核心牺牲，从被创造的木偶蜕变为拥有自主意志之人。")
    if st.button("开启新对话", icon = "➕️",width = "stretch"):
        if st.session_state.messages:
            save_session()
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun()

    st.text("历史")
    session_list = load_sessions()
    for session in reversed(session_list):
        left, right = st.columns([4, 1])
        with left:
            try:
                if os.path.exists(f"sessions/{session}.json"):
                    with open(f'sessions/{session}.json', "r", encoding="utf-8") as f:
                        session_data = json.load(f)
                        this_name = session_data["messages"][0]["content"]
            except Exception as e:
                this_name = "新对话"
            if st.button(this_name, width = "stretch", key = f"load_{session}", type = "secondary"if session == st.session_state.current_session else "tertiary"):
                load_session(session)
                st.rerun()
        with right:
            if st.button("", icon = "❌️",width = "stretch",  key = f"delete_{session}", type = "tertiary"):
                confirm_delete(session)



st.logo("resources/桑多涅头像1.png", size = "large")
st.subheader("桑多涅")
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if st.session_state["messages"] == []:

    st.write("初次见面...")
    st.audio("resources/初次见面.mp3")
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.chat_message("user", avatar = "resources/旅行者头像.png").write(message["content"])
    else:
        st.chat_message("assistant", avatar = "resources/桑多涅头像1.png").write(message["content"])

prompt = st.bottom.chat_input("请输入...")
if prompt:
    st.chat_message("user", avatar = "resources/旅行者头像.png").write(prompt)
    print("-------------------->调用ai模型，提示词：", prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        #model="deepseek-r1:8b",
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state["messages"]
        ],
        stream=True,
        extra_body={
            "think": False
        }
    )

    response_message = st.empty()

    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant", avatar="resources/桑多涅头像1.png").write(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_session()
    st.rerun()