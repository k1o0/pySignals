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


def latch(inputs, node, _):
    # always assumes two inputs: (arm, release)
    arm = inputs[0].get_value()
    arm_set = arm is not None  # TODO is this necessary?
    release = inputs[1].get_value()
    release_set = release is not None
    # current state:
    # armed = false when currently released, armed = true when currently armed
    armed = node.get_value()

    try_arm = arm_set and arm
    try_release = release_set and release

    if try_release and (try_arm or armed):
        # new arm *and* new release signals -> new
        # - OR -
        # previously armed *and* new release -> new release
        node.set_value(False)
    elif not armed and try_arm:
        # previously not armed *and* new arm -> new armed
        node.set_value(True)
    else:
        # no latch state change
        pass
