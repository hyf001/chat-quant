
from src.graph import builder
from IPython.display import display ,Image

def test_show_graph():
    graph = builder.create_financial_workflow()
    display(Image(graph.get_graph().draw_mermaid_png()))