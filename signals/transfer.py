def identity(inputs, node, _):
    # assumes one input only
    val = inputs[0].get_value()
    if val:
        node.set_value(val)


def mapn(inputs, node, f):
    inpvals = [n.get_value() for n in inputs]
    if not all(inpvals):
        return  # TODO return None?
    try:
        node.set_value(f(*inpvals))  # TODO use setter (could warn of type changes)?
    except Exception:
        raise Exception('Error in map function')
