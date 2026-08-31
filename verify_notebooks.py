import json

for nb in [
    '03_agentic_ai/02_langgraph/05_streaming/01_stream_basics.ipynb',
    '03_agentic_ai/03_rag_advanced/10_rag_evaluation/01_evaluation_metrics.ipynb',
    '01_data_science_foundations/01_numpy/01_numpy_foundations.ipynb'
]:
    d = json.load(open(nb, encoding='utf-8'))
    print(f'=== {nb} ===')
    for i, c in enumerate(d['cells'][:10]):
        src = ''.join(c.get('source', [])).strip()
        first = src.splitlines()[0] if src else ''
        print(f'  Cell {i}: {c["cell_type"]} | {first[:80]}')
    print()