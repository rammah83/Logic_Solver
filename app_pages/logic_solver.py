import sympy as sp
from sympy.logic.boolalg import simplify_logic, to_cnf
from sympy.logic.inference import satisfiable, valid, PropKB, entails

# from string import ascii_lowercase
import streamlit as st

# st.subheader("Logic :blue[cool] :sunglasses:")


# Define symbolic variables
sp_symbols = sp.symbols("P Q R A B C D E G H")
# P, B, A, W, E, G = sp.symbols('P B A W E G')
all_symbols = [str(symbol) for symbol in sp_symbols]


st.write("### Choose symbols")
# Initialize session state for selectboxes and available options if not exists
if "selectboxes" not in st.session_state:
    st.session_state.selectboxes = []
    selected_symbols = [
        st.session_state[f"select_{i}"]
        for i in range(len(st.session_state.selectboxes))
    ]

if "available_options" not in st.session_state:
    st.session_state.available_options = set(all_symbols) - set(selected_symbols)


# Function to add a new selectbox
def add_selectbox():
    if len(st.session_state.selectboxes) < len(all_symbols):
        st.session_state.available_options = set(all_symbols) - set(selected_symbols)
        st.session_state.selectboxes.append(tuple(st.session_state.available_options))


# Function to remove the last selectbox
def remove_selectbox():
    if len(st.session_state.selectboxes) > 1:
        removed_option = st.session_state[
            f"select_{len(st.session_state.selectboxes) - 1}"
        ]
        st.session_state.available_options.add(removed_option)
        st.session_state.selectboxes.pop()


# Add and Remove buttons
col1, col2 = st.columns(2)
with col1:
    st.button("Add Selectbox", on_click=add_selectbox)
with col2:
    st.button("Remove Selectbox", on_click=remove_selectbox)

# Display selectboxes
col_symbol, col_sentence, col_check = st.columns(
    [1, 6, 1], gap="small", vertical_alignment="top"
)
for i, options in enumerate(st.session_state.selectboxes):
    selected = col_symbol.selectbox(
        f"Select Symbol {i+1}", sorted(options), key=f"select_{i}"
    )
    sentence = col_sentence.text_input(label=f"Sencence {i+1}", key=f"input_{i}")
    check_truth = col_check.selectbox(
        f"check {selected}", ["True", "False"], key=f"check_{selected}"
    )

# Submit button check if all selected sympbols are unique
selected_symbols = [
    st.session_state[f"select_{i}"] for i in range(len(st.session_state.selectboxes))
]
validites = {
    str(symbol): st.session_state[f"check_{symbol}"] for symbol in selected_symbols
}

if len(st.session_state.selectboxes) >= 1:
    # get non unique symbols in selected_symbols
    if col_symbol.button("CHECK", type="primary"):
        if len(set(selected_symbols)) < len(selected_symbols):
            col_sentence.error("You can't select same symbols twice!")
        else:
            col_sentence.success(f"You selected: {', '.join(selected_symbols)}")
    col_kb, col_entails, _ = st.columns(
        [2,1,3], gap="small", vertical_alignment="bottom"
    )
    logical_statement = col_kb.text_area(
        "*Knwoledge Base (KB) _Logical Statement_*",
        help="use '>>' for 'implies', '&' for 'and', '|' for 'or', '~' for 'not'",
    )

    symbol_to_entail = col_entails.selectbox(label="Entails", options=selected_symbols)
    if st.button("SOLVE"):
        container = st.container()
        expender = st.expander("## Details")
        col_sentence, col_result, col_validity = expender.columns(
            [2, 1, 1], gap="small", vertical_alignment="top"
        )
        col_sentence.write("_Statement:_")
        col_result.write("_Statement Evaluation:_")
        col_validity.write("_Resolution:_")
        kb: PropKB = PropKB()
        for statement in logical_statement.split("\n"):
            # display and List KB
            symp_statement = sp.sympify(statement)
            col_sentence.latex(sp.latex(symp_statement))
            symp_result = symp_statement.subs(
                {f"{k}": validites[f"{k}"] for k in symp_statement.atoms()}
            )
            col_result.latex(symp_result)
            if valid(symp_statement):
                col_validity.success("Valid in all Worlds")
            else:
                models = satisfiable(symp_statement, all_models=True)
                if all(models):
                    with col_validity.popover(
                        "Valid in some Worlds", use_container_width=True
                    ):
                        for model in satisfiable(symp_statement, all_models=True):
                            st.latex(model if model else "Impossible")
                            # st.latex(satisfiable(symp_statement, all_models=False))
                else:
                    col_validity.error("Invalid in all Worlds")
            kb.tell(symp_statement)

        # buil and stantment between logical_statement
        global_statement = sp.sympify(
            " & ".join(
                [
                    "(" + str(symp_statement) + ")"
                    for symp_statement in logical_statement.split("\n")
                ]
            )
        )
        col_sentence.write("---")
        col_sentence.latex(sp.latex(global_statement))
        col_result.write("---")
        global_symp_result = global_statement.subs(
            {f"{k}": validites[f"{k}"] for k in global_statement.atoms()}
        )
        col_result.latex(global_symp_result)
        col_validity.write("---")
        if valid(global_statement):
            col_validity.success("Valid in all Worlds")
        else:
            models_for_global = satisfiable(global_statement, all_models=True)
            if all(models_for_global):
                with col_validity.popover(
                    "Valid in some possibilities", use_container_width=True
                ):
                    for model in satisfiable(global_statement, all_models=True):
                        st.latex(model if model else "Impossible")
                        # st.latex(satisfiable(symp_statement, all_models=False))
            else:
                col_validity.error("Invalid in all Worlds")

        st.write("---")
        col_kb, col_entails, col_result = container.columns(
            3, gap="small", vertical_alignment="center"
        )
        col_entails.write(
            f"### Knowledge Base being TRUE entails {symbol_to_entail} is "
        )
        col_kb.dataframe({"Knowledge Base": kb.clauses}, hide_index=True)
        col_result.latex(
            kb.ask(symbol_to_entail)
        )  # alternative : col_result.latex(entails(symbol_to_entail, kb.clauses))
