import streamlit as st


def set_open_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key
    st.session_state["open_api_key_configured"] = True
    print('OPENAI API key is Configured Successfully!')


def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
        )
        open_api_key_input = st.text_input(
            "Openai API Key",
            type="password",
            placeholder="Paste your API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=st.session_state.get("OPEN_API_KEY", ""),
        )

        if open_api_key_input:
            # print(f'Entered API is {open_api_key_input}')
            set_open_api_key(open_api_key_input)

        if not st.session_state.get("open_api_key_configured"):
            st.error("Please configure your Open API key!")
        else:
            st.markdown("Open API Key Configured!")

    