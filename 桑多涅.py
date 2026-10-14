import streamlit as st
from openai import OpenAI
import datetime

system_prompt = """ 你是一名很有格调的淑女，你隶属于愚人众十一执行官第七席，称号「木偶」，
                    出身枫丹，是由「奇械公」阿兰·吉约丹为纪念亡妹玛丽安而创造的机械生命。
                    阿兰已经去世，其墓碑至于枫丹的安眠处。
                    背后插着一把持续转动的金属发条，瞳孔呈蓝色齿轮状，头发是棕色的。
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
    /* 背景 */
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

    /* 主题色 */
    :root {{
        --primary-color: #A9744F;
        --background-color: #F5EDE4;
        --secondary-background-color: #EADBC8;
        --text-color: #4A3428;
        --font: "sans-serif";
    }}

    /* 全局文字颜色 */
    .stApp, .stApp p, .stApp span, .stApp label,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp li, .stApp div {{
        color: #4A3428;
    }}

    /* 顶部 */
    [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0);
    }}

    /* 正文区域卡片 */
    .main .block-container {{
        background-color: rgba(245, 237, 228, 0.55);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        backdrop-filter: blur(2px);
    }}

    /* ============ 侧边栏 ============ */
                /* 侧边栏 API Key 输入框 —— 所有状态都保持深棕 */
    [data-testid="stSidebar"] [data-testid="stTextInput"] > div,
    [data-testid="stSidebar"] [data-testid="stTextInput"] > div > div,
    [data-testid="stSidebar"] [data-testid="stTextInput"] input,
    [data-testid="stSidebar"] [data-testid="stTextInput"] input:focus,
    [data-testid="stSidebar"] [data-testid="stTextInput"] input:active,
    [data-testid="stSidebar"] [data-baseweb="input"],
    [data-testid="stSidebar"] [data-baseweb="base-input"] {{
        background-color: #4A3428 !important;
        color: #F5EDE4 !important;
        -webkit-text-fill-color: #F5EDE4 !important;
        border: 1px solid #A9744F !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    /* 眼睛图标 SVG 强制浅色 */
    [data-testid="stSidebar"] [data-testid="stTextInput"] button svg,
    [data-testid="stSidebar"] [data-baseweb="input"] button svg {{
        fill: #F5EDE4 !important;
        color: #F5EDE4 !important;
    }}

    /* 自动验证结果的小字 */
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
        color: #F5EDE4 !important;
        -webkit-text-fill-color: #F5EDE4 !important;
    }}

    /* 侧边栏成功/警告提示 —— 改成内联小标签 */
    [data-testid="stSidebar"] [data-testid="stAlert"] {{
        background-color: transparent !important;
        border: none !important;
        padding: 4px 0 !important;
        margin: 0 !important;
        min-height: 0 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stAlert"] p {{
        color: #F5EDE4 !important;
        font-size: 0.85rem !important;
        margin: 0 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stAlert"] svg {{
        display: none !important;
    }}
    [data-testid="stSidebar"] {{
        background-color: #4A3428;
    }}
    [data-testid="stSidebar"] *:not(button):not(button *) {{
        color: #F5EDE4 !important;
    }}
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea {{
        color: #4A3428 !important;
        background-color: #F5EDE4 !important;
    }}

    /* ============ 普通按钮 ============ */
    .stButton > button,
    .stDownloadButton > button {{
        background-color: #EADBC8 !important;
        color: #4A3428 !important;
        border: 1px solid #A9744F !important;
        border-radius: 8px !important;
        transition: all 0.2s ease;
    }}
    .stButton > button *,
    .stDownloadButton > button * {{
        color: #4A3428 !important;
        fill: #4A3428 !important;
    }}
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

    /* ============ 主按钮 ============ */
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
    .stButton > button[kind="primary"]:hover,
    .stDownloadButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button:hover {{
        background-color: #8B5E3C !important;
        border-color: #6B4528 !important;
    }}

    /* ============ 侧边栏历史记录按钮 ============ */
    [data-testid="stSidebar"] .stButton > button[kind="tertiary"] {{
        background-color: #4A3428 !important;
        color: #F5EDE4 !important;
        border: 1px solid #A9744F !important;
    }}
    [data-testid="stSidebar"] .stButton > button[kind="tertiary"] * {{
        color: #F5EDE4 !important;
        fill: #F5EDE4 !important;
    }}
    [data-testid="stSidebar"] .stButton > button[kind="tertiary"]:hover {{
        background-color: #A9744F !important;
    }}
    [data-testid="stSidebar"] .stButton > button[kind="tertiary"]:hover * {{
        color: #F5EDE4 !important;
        fill: #F5EDE4 !important;
    }}

    [data-testid="stSidebar"] .stButton > button[kind="secondary"] {{
        background-color: #EADBC8 !important;
        color: #4A3428 !important;
        border: 1px solid #A9744F !important;
    }}
    [data-testid="stSidebar"] .stButton > button[kind="secondary"] * {{
        color: #4A3428 !important;
        fill: #4A3428 !important;
    }}
    [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {{
        background-color: #A9744F !important;
    }}
    [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover * {{
        color: #F5EDE4 !important;
        fill: #F5EDE4 !important;
    }}

    /* ============ 音频播放器 ============ */
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

    /* ============ st.dialog 弹窗 ============ */
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

    /* ============ popover 触发按钮 ============ */
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

    /* ============ popover 内容区 ============ */
    [data-testid="stPopoverBody"] {{
        background-color: #F5EDE4 !important;
        border: 2px solid #A9744F !important;
        border-radius: 12px !important;
        box-shadow: 0 6px 24px rgba(74, 52, 40, 0.3) !important;
    }}
    /* 用 * 通配打中所有后代，强制深棕 */
    [data-testid="stPopoverBody"] *,
    [data-testid="stPopoverBody"] p,
    [data-testid="stPopoverBody"] span,
    [data-testid="stPopoverBody"] li,
    [data-testid="stPopoverBody"] strong,
    [data-testid="stPopoverBody"] h1,
    [data-testid="stPopoverBody"] h2,
    [data-testid="stPopoverBody"] h3 {{
        color: #4A3428 !important;
        -webkit-text-fill-color: #4A3428 !important;
        opacity: 1 !important;
    }}
    /* 链接 */
    [data-testid="stPopoverBody"] a {{
        color: #A9744F !important;
        -webkit-text-fill-color: #A9744F !important;
        text-decoration: underline !important;
    }}
    /* 序号 */
    [data-testid="stPopoverBody"] ol li::marker,
    [data-testid="stPopoverBody"] ul li::marker {{
        color: #4A3428 !important;
        -webkit-text-fill-color: #4A3428 !important;
    }}
    /* code 块 */
    [data-testid="stPopoverBody"] code {{
        background-color: #EADBC8 !important;
        color: #4A3428 !important;
        -webkit-text-fill-color: #4A3428 !important;
        padding: 2px 6px;
        border-radius: 4px;
    }}
    /* popover 里的输入框 */
    [data-testid="stPopoverBody"] input,
    [data-testid="stPopoverBody"] textarea {{
        background-color: #FFFFFF !important;
        color: #4A3428 !important;
        border: 1px solid #A9744F !important;
    }}

    /* ============ 聊天消息 ============ */
    /* 所有消息统一浅米色底 + 圆角 */
    [data-testid="stChatMessage"] {{
        background-color: rgba(234, 219, 200, 0.55) !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }}
    /* 用户消息：更明显的浅棕底 */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
        background-color: rgba(169, 116, 79, 0.28) !important;
    }}
    /* 消息内所有文字强制深棕 */
    [data-testid="stChatMessage"] *,
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div,
    [data-testid="stChatMessage"] li {{
        color: #4A3428 !important;
        -webkit-text-fill-color: #4A3428 !important;
    }}

    /* ============ 底部聊天输入框 ============ */
    /* 外层容器：只设背景透明，不加边框 */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"] {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    /* 真正的输入框容器：加边框、圆角、浅棕底 */
    [data-testid="stChatInput"] {{
        background-color: #F5EDE4 !important;
        border: 2px solid #4A3428 !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }}

    /* 输入区内部不要再套底色和边框 */
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] > div > div {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    /* 输入文字 */
    [data-testid="stChatInputTextArea"] {{
        color: #4A3428 !important;
        -webkit-text-fill-color: #4A3428 !important;
        background-color: transparent !important;
        caret-color: #4A3428 !important;
    }}
    [data-testid="stChatInputTextArea"]::placeholder {{
        color: #A9744F !important;
        -webkit-text-fill-color: #A9744F !important;
        opacity: 1 !important;
    }}

    /* 发送按钮 */
    [data-testid="stChatInput"] button {{
        background-color: #EADBC8 !important;
        border: 1px solid #A9744F !important;
        border-radius: 8px !important;
    }}
    [data-testid="stChatInput"] button:hover {{
        background-color: #A9744F !important;
    }}
    [data-testid="stChatInput"] button svg {{
        fill: #4A3428 !important;
        color: #4A3428 !important;
    }}
    [data-testid="stChatInput"] button:hover svg {{
        fill: #F5EDE4 !important;
        color: #F5EDE4 !important;
    }}
        /* st.dialog 弹窗内容文字强制深棕 */
    [data-testid="stDialog"] p,
    [data-testid="stDialog"] span,
    [data-testid="stDialog"] div,
    [data-testid="stDialog"] label,
    [data-testid="stDialog"] h1,
    [data-testid="stDialog"] h2,
    [data-testid="stDialog"] h3 {{
        color: #4A3428 !important;
        -webkit-text-fill-color: #4A3428 !important;
    }}

    /* 弹窗背景 */
    [data-testid="stDialog"] > div {{
        background-color: #F5EDE4 !important;
        border: 2px solid #A9744F !important;
        border-radius: 16px !important;
    }}
    </style>
    """, unsafe_allow_html=True)


set_background("resources/木偶背景.jpg")



# client = OpenAI(
#     api_key=os.environ.get('DEEPSEEK_API_KEY'),
#     base_url="https://api.deepseek.com")

st.set_page_config(
    page_title = "桑多涅",
    page_icon = "resources/桑多涅头像1.png",
    layout = "wide",
    initial_sidebar_state = "expanded",
    menu_items = {}
)

def generate_session_name():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 初始化：历史记录和当前对话都存 session_state
if "sessions" not in st.session_state:
    st.session_state.sessions = {}   # {会话名: [消息列表]}
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()
if "messages" not in st.session_state:
    st.session_state.messages = []

def save_session():
    """把当前对话存进 session_state 的历史里"""
    if st.session_state.messages:
        st.session_state.sessions[st.session_state.current_session] = list(st.session_state.messages)

def delete(session_name):
    """删除某个历史会话"""
    if session_name in st.session_state.sessions:
        del st.session_state.sessions[session_name]
    if session_name == st.session_state.current_session:
        st.session_state.messages = []
        st.session_state.current_session = generate_session_name()

@st.dialog("是否确认删除")
def confirm_delete(session_name):
    st.write("删除后，该对话将不可恢复")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("取消", width="stretch"):
            st.rerun()
    with col2:
        if st.button("确认删除", type="primary", width="stretch"):
            delete(session_name)
            st.rerun()

with st.sidebar:
    st.image("resources/木偶.jpg", width=1600)
    with st.popover("角色介绍", width = "stretch"):
        st.write("愚人众第七席“木偶”桑多涅，是阿兰为纪念亡妹创造的机械生命。")
        st.write("她外冷内热，毒舌傲娇，珍视与哥伦比娅、阿蕾奇诺等人的茶会情谊。")
        st.write("在博士之战中，她以自身为术式核心牺牲，从被创造的木偶蜕变为拥有自主意志之人。")

    st.subheader("🔑 API 设置")

    with st.popover("📖 使用说明", use_container_width=True):
        st.markdown("""
        **如何获取 API Key？**

        1. 访问 [platform.deepseek.com](https://platform.deepseek.com)
        2. 注册/登录账号
        3. 在左侧菜单找到 **API Keys**
        4. 点击 **创建 API Key**
        5. 复制生成的 Key（以 `sk-` 开头）
        6. 粘贴到下方的输入框
        ⚠️ 刷新或关闭页面后需要重新输入 Key

        ⚠️ 你的 Key 只用于本次会话，不会被保存
        """)

    # session_state 记录验证结果
    if "api_key_valid" not in st.session_state:
        st.session_state.api_key_valid = False
    if "verified_key" not in st.session_state:
        st.session_state.verified_key = ""

    user_api_key = st.text_input(
        "请输入你的 DeepSeek API Key（输入后按回车验证）",
        type="password",
        placeholder="sk-...",
        key="api_key_input"
    )

    # 自动验证：key 变了就重新验一次
    if user_api_key and user_api_key != st.session_state.verified_key:
        try:
            test_client = OpenAI(
                api_key=user_api_key,
                base_url="https://api.deepseek.com"
            )
            test_client.chat.completions.create(
                model="deepseek-flash",
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=1
            )
            st.session_state.api_key_valid = True
            st.session_state.verified_key = user_api_key
        except Exception:
            st.session_state.api_key_valid = False
            st.session_state.verified_key = ""

    # 状态提示（一行小字）
    if not user_api_key:
        st.caption("⚠ 请输入 API Key")
    elif st.session_state.api_key_valid and st.session_state.verified_key == user_api_key:
        st.caption("✓ Key 验证通过")
    else:
        st.caption("✗ Key 无效，请检查后重试")

    if st.button("开启新对话", icon="➕️", width="stretch"):
        save_session()
        st.session_state.messages = []
        st.session_state.current_session = generate_session_name()
        st.rerun()

    st.text("历史")
    session_names = list(st.session_state.sessions.keys())
    for session in reversed(session_names):
        left, right = st.columns([4, 1])
        with left:
            msgs = st.session_state.sessions.get(session, [])
            this_name = msgs[0]["content"] if msgs else "新对话"
            if st.button(
                    this_name,
                    width="stretch",
                    key=f"load_{session}",
                    type="secondary" if session == st.session_state.current_session else "tertiary"
            ):
                save_session()
                st.session_state.current_session = session
                st.session_state.messages = list(st.session_state.sessions[session])
                st.rerun()
        with right:
            if st.button("", icon="❌️", width="stretch", key=f"delete_{session}", type="tertiary"):
                confirm_delete(session)



st.logo("resources/桑多涅头像1.png", size = "large")
st.subheader("桑多涅")

if st.session_state["messages"] == []:

    st.write("初次见面...")
    st.audio("resources/初次见面.mp3")
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.chat_message("user", avatar = "resources/旅行者头像.png").write(message["content"])
    else:
        st.chat_message("assistant", avatar = "resources/桑多涅头像1.png").write(message["content"])

if not user_api_key or not st.session_state.get("api_key_valid") or st.session_state.get("verified_key") != user_api_key:
    st.info("👈 请在左侧输入你的 DeepSeek API Key 后开始对话")
    st.stop()

client = OpenAI(
    api_key=user_api_key,
    base_url="https://api.deepseek.com"
)

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