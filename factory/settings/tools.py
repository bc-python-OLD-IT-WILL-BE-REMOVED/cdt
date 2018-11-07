# --------------- #
# -- CONSTANTS -- #
# --------------- #

CHECK_TAG = "check"
NAMES_TAG = "names"

BLOCKS_TAG      = "blocks"
MULTIKEYVAL_TAG = "multikeyval"
KEYVAL_TAG      = "keyval"
SPECIAL_TAG     = "special"

XTRAS_TAGS = ["cdt", "newctxt"]
XTRAS_TAGS = {
    f"[{tag}]": (tag, len(tag) + 2)
    for tag in XTRAS_TAGS
}
# ---------------------- #
# -- OUR LITTLE TOOLS -- #
# ---------------------- #

def verbatim(content):
    return "\n".join(content)


def findextra(infos):
    xtras          = []
    somethingfound = True

    while somethingfound:
        somethingfound = False

        for tag in XTRAS_TAGS:
            if infos.startswith(tag):
                somethingfound = True

                xtras.append(XTRAS_TAGS[tag][0])
                infos = infos[XTRAS_TAGS[tag][1]:].lstrip()

    return xtras, infos


def check(infos):
    if infos[0] != '<' or infos[-1] != '>':
        raise ValueError(f"wrong function identificator : {infos}")

    _infos = infos[1:-1].split('/')

    if len(_infos) != 2:
        raise ValueError(f"wrong function identificator : {infos}")

    pyfilename, funcname = _infos

    return {
        "file"    : pyfilename,
        "funcname": funcname
    }


def names(infos):
    return infos.split()


def choices(infos):
    _infos = []

    for word in infos.split():
        if word[0] != '"' or word[-1] != '"':
            raise ValueError(f"wrong use of list of words : {infos}")

        word = word[1:-1].strip()

        _infos.append(word)

    return {":listofwords:": _infos}


def peufmode(infos):
    peufmodedict = {}
    checkers     = {}

    for tag in (KEYVAL_TAG, MULTIKEYVAL_TAG):
        if tag in infos:
            peufmodedict[f"{tag}:: {infos[tag]['sep']}"] \
            = infos[tag][NAMES_TAG]

    if SPECIAL_TAG in infos:
        names      = infos[SPECIAL_TAG][NAMES_TAG]
        onechecker = infos[SPECIAL_TAG][CHECK_TAG]

        peufmodedict["verbatim"] = names

        for onename in names:
            checkers[onename] = onechecker

    return {
        "peuf" : peufmodedict,
        "check": checkers
    }


# --------------- #
# -- NORMALIZE -- #
# --------------- #

VALIDATORS = {
    CHECK_TAG: check,
    NAMES_TAG: names
}


def findvalidators(infos):
    for validatortag in VALIDATORS:
        if validatortag in infos:
            infos[validatortag] = VALIDATORS[validatortag](
                infos[validatortag]
            )

    return infos


def normalize_specs(specs):
    for dir_n_file, localspecs in specs.items():
        for blockname, infos in localspecs.items():
            if blockname == "doc":
                infos = verbatim(infos)

            elif blockname == "blocks":   # SPECIAL_TAG
                for tag in infos:
                    infos[tag] = findvalidators(infos[tag])

            elif blockname == "keys-vals":
                for blocks, subinfos in infos.items():
                    _subinfos = {}

                    for key, valcheck in subinfos.items():
                        xtras, valcheck = findextra(valcheck)

                        if valcheck[0] == '<':
                            validator = check

                        else:
                            validator = choices

                        valcheck = validator(valcheck)

                        if xtras:
                            valcheck[":extras:"] = xtras

                        for realkey in key.split():
                            _subinfos[realkey] = valcheck

                    infos[blocks] = _subinfos

            else:
                infos = findvalidators(infos)

            localspecs[blockname] = infos

        localspecs[BLOCKS_TAG] = peufmode(localspecs[BLOCKS_TAG])

        specs[dir_n_file] = localspecs

    return specs
