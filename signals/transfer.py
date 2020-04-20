from typing import Callable, Tuple
Node = 'signals.node.Node'


def identity(inputs: Tuple[Node], child: Node, _) -> None:
    # assumes one input only
    val = inputs[0].value
    if val:
        child.value = val


def mapn(inputs: Tuple[Node], child: Node, f: Callable) -> None:
    inpvals = [n.value for n in inputs]
    if not all(inpvals):
        return
    try:
        child.value = f(*inpvals)  # TODO use setter (could warn of type changes)?
    except Exception:
        raise Exception('Error in map function')


def merge(inputs: Tuple[Node], child: Node, _) -> None:
    for inp in inputs:
        v = inp.value
        if inp.queued:  # if working value set
            child.value = v
            return


def latch(inputs: Tuple[Node], child: Node, _) -> None:
    # always assumes two inputs: (arm, release)
    arm_val = inputs[0].value
    arm_set = arm_val is not None  # TODO is this necessary?
    release_val = inputs[1].value
    release_set = release_val is not None
    # current state:
    # armed = false when currently released, armed = true when currently armed
    armed = child.value

    try_arm = arm_set and arm_val
    try_release = release_set and release_val

    if try_release and (try_arm or armed):
        # new arm *and* new release signals -> new
        # - OR -
        # previously armed *and* new release -> new release
        child.value = False
    elif not armed and try_arm:
        # previously not armed *and* new arm -> new armed
        child.value = True
    else:
        pass  # no latch state change
