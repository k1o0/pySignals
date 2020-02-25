def identity(inputs, node, _):
    # assumes one input only
    val = inputs[0].value
    if val:
        node.value = val


def mapn(inputs, node, f):
    inpvals = [n.value for n in inputs]
    if not all(inpvals):
        return  # TODO return None?
    try:
        node.value = f(*inpvals)  # TODO use setter (could warn of type changes)?
    except Exception:
        raise Exception('Error in map function')


def latch(inputs, node, _):
    # always assumes two inputs: (arm, release)
    arm = inputs[0].value
    arm_set = arm is not None  # TODO is this necessary?
    release = inputs[1].value
    release_set = release is not None
    # current state:
    # armed = false when currently released, armed = true when currently armed
    armed = node.value

    try_arm = arm_set and arm
    try_release = release_set and release

    if try_release and (try_arm or armed):
        # new arm *and* new release signals -> new
        # - OR -
        # previously armed *and* new release -> new release
        node.value = False
    elif not armed and try_arm:
        # previously not armed *and* new arm -> new armed
        node.value = True
    else:
        pass  # no latch state change
