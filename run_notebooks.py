"""Execute each notebook from a fresh kernel and save outputs and HTML reports."""
from pathlib import Path
import os
import time
import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter

ROOT = Path(__file__).resolve().parent
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.cache' / 'matplotlib'))
os.environ.setdefault('IPYTHONDIR', str(ROOT / '.cache' / 'ipython'))
os.environ.setdefault('JUPYTER_RUNTIME_DIR', str(ROOT / '.cache' / 'jupyter'))
for key in ['MPLCONFIGDIR', 'IPYTHONDIR', 'JUPYTER_RUNTIME_DIR']:
    Path(os.environ[key]).mkdir(parents=True, exist_ok=True)

def main():
    for path in sorted(ROOT.glob('0*.ipynb')):
        started = time.monotonic()
        book = nbformat.read(path, as_version=4)
        # Never use an already-running interactive kernel.
        client = NotebookClient(book, timeout=1800, kernel_name='python3',
                                resources={'metadata': {'path': str(ROOT)}},
                                on_cell_executed=lambda cell_index, **kw: print(f'  cell {cell_index}: done', flush=True))
        try:
            client.execute()
        finally:
            nbformat.write(book, path)
        errors = [o for c in book.cells if c.cell_type == 'code'
                  for o in c.get('outputs', []) if o.output_type == 'error']
        assert not errors, errors
        report_dir = ROOT / 'reports'
        report_dir.mkdir(exist_ok=True)
        body, _ = HTMLExporter(template_name='lab').from_notebook_node(book)
        (report_dir / (path.stem + '.html')).write_text(body, encoding='utf-8')
        print(f'PASS {path.name}: {time.monotonic()-started:.1f}s', flush=True)

if __name__ == '__main__':
    main()
