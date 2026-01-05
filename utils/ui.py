import streamlit as st


def apply_global_layout(max_width: int = 1750):
    """
    ✅ Layout global responsivo.
    - Desktop: deixa a página bem mais larga
    - Mobile: mantém padding confortável
    - Não altera lógica, só CSS
    """

    st.markdown(
        f"""
        <style>
        /* ✅ Conteúdo principal mais largo (DESKTOP) */
        @media (min-width: 900px) {{
            .main .block-container {{
                max-width: {max_width}px !important;
                padding-left: 4rem !important;
                padding-right: 4rem !important;
                padding-top: 2rem !important;
                padding-bottom: 2rem !important;
            }}
        }}

        /* ✅ Mobile confortável */
        @media (max-width: 899px) {{
            .main .block-container {{
                max-width: 100% !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                padding-top: 1.2rem !important;
                padding-bottom: 1.2rem !important;
            }}
        }}

        /* ✅ Dataframes e tabelas sempre ocupam tudo */
        div[data-testid="stDataFrame"],
        div[data-testid="stTable"] {{
            width: 100% !important;
        }}

        /* ✅ espaço melhor entre colunas */
        div[data-testid="stHorizontalBlock"] {{
            gap: 1.2rem !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
