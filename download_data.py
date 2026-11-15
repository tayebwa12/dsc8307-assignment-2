"""Fetch public benchmark copies; verify they match the supplied assignment data.

Data stay local and are excluded from Git. Public sources:
https://www.tensorflow.org/tutorials/structured_data/imbalanced_data
https://archive.ics.uci.edu/dataset/292/wholesale+customers
"""
from pathlib import Path
import gzip
import hashlib
import io
import shutil
import urllib.request
import zipfile
import pandas as pd

CREDIT_SHA256 = '76274b691b16a6c49d3f159c883398e03ccd6d1ee12d9d8ee38f4b4b98551a89'
WHOLESALE_NORMALIZED_SHA256 = '8f79c9a3e0bc677502d545f986bc42a5cd4dc73ddb6c33044b1a2cc14ed0aaba'
CREDIT_URL = 'https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv'
WHOLESALE_URL = 'https://archive.ics.uci.edu/static/public/292/wholesale%2Bcustomers.zip'


def _open(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'DSC8307-reproducible-analysis'}), timeout=60)


def _wholesale_valid(path):
    frame = pd.read_csv(path).rename(columns={'Delicassen': 'Delicatessen'})
    normalized = frame.to_csv(index=False, lineterminator='\n').encode()
    if hashlib.sha256(normalized).hexdigest() != WHOLESALE_NORMALIZED_SHA256:
        raise ValueError('Wholesale data differ from the supplied assignment records.')
    return normalized


def ensure_data(name, directory=None):
    """Return a verified local CSV path, downloading only when absent.

    Internet is needed on first execution, unless assignment CSVs have been
    copied into data/. After caching, notebook execution is offline.
    """
    directory = Path(directory) if directory else Path(__file__).resolve().parent / 'data'
    directory.mkdir(parents=True, exist_ok=True)
    if name == 'wholesale':
        target = directory / 'wholesale-customers.csv'
        if not target.exists():
            print('Downloading public UCI Wholesale Customers benchmark...')
            with _open(WHOLESALE_URL) as response:
                payload = response.read()
            with zipfile.ZipFile(io.BytesIO(payload)) as archive:
                member = next(n for n in archive.namelist() if n.lower().endswith('.csv'))
                frame = pd.read_csv(io.BytesIO(archive.read(member))).rename(columns={'Delicassen': 'Delicatessen'})
            normalized = frame.to_csv(index=False, lineterminator='\n').encode()
            if hashlib.sha256(normalized).hexdigest() != WHOLESALE_NORMALIZED_SHA256:
                raise ValueError('Downloaded wholesale records do not match the assignment.')
            target.write_bytes(normalized)
        _wholesale_valid(target)
        return target
    if name != 'creditcard':
        raise ValueError('Expected wholesale or creditcard.')
    target = directory / 'creditcard.csv'
    compressed = directory / 'creditcard.csv.gz'
    if compressed.exists() and not target.exists():
        with gzip.open(compressed, 'rb') as stream:
            actual = hashlib.file_digest(stream, 'sha256').hexdigest()
        if actual != CREDIT_SHA256:
            raise ValueError('Compressed credit-card data do not match assignment.')
        return compressed
    if not target.exists():
        print('Downloading public credit-card benchmark (about 151 MB)...')
        temporary = target.with_suffix('.csv.partial')
        try:
            with _open(CREDIT_URL) as response, temporary.open('wb') as stream:
                shutil.copyfileobj(response, stream, length=1024 * 1024)
            with temporary.open('rb') as stream:
                actual = hashlib.file_digest(stream, 'sha256').hexdigest()
            if actual != CREDIT_SHA256:
                raise ValueError('Downloaded credit-card file does not match assignment.')
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
    with target.open('rb') as stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    if actual != CREDIT_SHA256:
        raise ValueError('Credit-card file does not match supplied assignment.')
    return target


if __name__ == '__main__':
    print(ensure_data('wholesale'))
    print(ensure_data('creditcard'))
