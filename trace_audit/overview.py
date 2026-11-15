"""已有资料的描述性概览。"""
def summarize(data):
    rows = data["rows"]
    return {'inspection_receipts': len(rows), 'unique_physical_units': len({row['unit'] for row in rows}), 'directed_tests': sum(row['selection'] == 'directed' for row in rows), 'revocations': sum(row['revokes'] is not None for row in rows)}
