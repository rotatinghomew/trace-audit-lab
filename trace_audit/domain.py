"""独立业务规则，仅依赖冻结资料。"""
def quote(data, request):
    node = request['node']
    unit = request['unit']
    draw = int(request['draw'])
    if node not in data['nodes'] or draw < 0:
        raise ValueError('节点或抽取序号非法')
    rule = data['nodes'][node]
    if not rule['active']:
        raise ValueError('节点已被替代')
    eligible = rule['eligible_units']
    if unit not in eligible:
        return {'eligible': False, 'probability': 0, 'node_revision': rule['revision']}
    weights = [1 + (index + draw) % 3 for index in range(len(eligible))]
    position = eligible.index(unit)
    return {'eligible': True, 'probability': weights[position] / sum(weights),
            'node_revision': rule['revision'], 'physical_unit': unit,
            'draw': draw, 'receipt': f'{node}:{rule["revision"]}:{draw}:{unit}'}

def ancestry(data, request):
    node = request['node']
    if node not in data['nodes']:
        raise ValueError('节点不存在')
    seen, parents = set(), []
    current = node
    while data['nodes'][current]['parent'] is not None:
        current = data['nodes'][current]['parent']
        if current in seen:
            raise ValueError('追溯关系出现环')
        seen.add(current)
        parents.append(current)
    return {'node': node, 'ancestors': parents, 'tree_version': data['tree_version']}

detail = ancestry
