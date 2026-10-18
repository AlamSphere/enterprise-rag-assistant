
import streamlit as st

from src.retriever import search_documents
from src.access_control import VALID_ROLES


st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🔎",
)

st.title("Enterprise Knowledge Assistant")
st.caption("Role-filtered company knowledge search — prototype")

st.warning(
    "Demo only: role selection is simulated, not authenticated. "
    "Do not use real confidential documents."
)

role = st.selectbox(
    "Demo user role",
    sorted(VALID_ROLES),
)

query = st.text_input(
    "Ask a question about company policies",
    placeholder="How do I submit an expense claim?",
)

if st.button("Search", type="primary"):
    if not query.strip():
        st.info("Enter a question to search the knowledge base.")
    else:
        try:
            results = search_documents(query, role)

            if not results:
                st.info("No relevant authorized information was found.")
            else:
                st.subheader("Retrieved evidence")

                for result in results:
                    with st.expander(result["title"], expanded=True):
                        st.write(result["text"])
                        st.caption(
                            f"Source: {result['document_id']} | "
                            f"Similarity score: {result['score']:.3f}"
                        )

        except (ValueError, FileNotFoundError) as error:
            st.error(str(error))
