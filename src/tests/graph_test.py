
from src.graph import workflow
from IPython.display import display ,Image

def test_show_graph():
    graph = workflow.create_financial_workflow()
    display(Image(graph.get_graph().draw_mermaid_png()))