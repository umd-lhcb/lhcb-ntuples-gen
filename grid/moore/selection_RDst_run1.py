# Stolen from:
#   https://gitlab.cern.ch/snippets/704
#
# Usage:
#   export CMTCONFIG=x86_64-centos7-gcc62-opt
#   lb-run -c best Moore/v28r3p1 python <this_script>

import sys

from TCKUtils.utils import getProperties


def describe(tck, name, props, indentation=0):
    """Recurse down into this algorithm's properties, printing information on
    its inputs."""
    indent = indentation*' '

    def iprint(s):
        print('{}{}'.format(indent, s))

    if 'Particle' in props:
        # Have a Particle maker, no need to descend further
        iprint(props['Output'])
        return

    header_name = '\n{0}{1}\n{0}{2}'.format(indent, name, len(name)*'=')
    print(header_name)

    header_sel = '\n{0}Selection\n{0}---------'.format(indent)
    print(header_sel)

    if 'Code' in props:
        # We have a FilterDesktop
        iprint('Code: {}'.format(props['Code']))
    elif 'DaughtersCuts' in props:
        # We have a CombineParticles
        preambulo = eval(props['Preambulo'])
        iprint('DecayDescriptors: {}'.format(props['DecayDescriptors']))
        if preambulo:
            iprint('Preambulo:        {}'.format(preambulo))
        iprint('DaughtersCuts:    {}'.format(props['DaughtersCuts']))
        iprint('CombinationCut:   {}'.format(props['CombinationCut']))
        iprint('MotherCut:        {}'.format(props['MotherCut']))
    elif 'TisTosSpecs' in props:
        # We have a TisTosTagger
        iprint('TisTosSpecs:  {}'.format(props['TisTosSpecs']))
    else:
        assert False, 'Do not know the type of {}'.format(props)

    header_inputs = '\n{0}Inputs\n{0}------'.format(indent)
    print(header_inputs)

    inputs = eval(props['Inputs'])
    for input_name in inputs:
        assert input_name.startswith('Hlt2/')
        input_name = '.*/{}$'.format(input_name[len('Hlt2/'):])
        input_props = getProperties(tck, input_name)
        assert len(input_props) == 1
        input_name, input_props = getProperties(tck, input_name).items()[0]
        describe(tck, input_name, input_props, indentation + 4)


def selections(tck, line):
    assert line.startswith('Hlt2') and line.endswith('Turbo')

    mover_name = '^FilterDesktop/{}Mover$'.format(line)
    mover_props = getProperties(tck, mover_name).values()[0]
    mover_inputs = eval(mover_props['Inputs'])
    assert len(mover_inputs) == 1

    filter_name = mover_inputs[0]
    assert filter_name.startswith('Hlt2/')
    filter_name = '.*/{}$'.format(filter_name[len('Hlt2/'):])
    filter_props = getProperties(tck, filter_name)
    assert len(filter_props) == 1
    filter_name, filter_props = filter_props.items()[0]
    describe(tck, filter_name, filter_props, indentation=0)


if __name__ == '__main__':
    tck = 0x217718a2
    lines = [
        'Hlt2CharmHadDpToKmKpPipTurbo',
        'Hlt2CharmHadDstp2D0Pip_D02KmKpPimPipTurbo',
        'Hlt2CharmHadDstp2D0Pip_D02KS0PimPip_KS0DDTurbo',
        'Hlt2CharmHadDstp2D0Pip_D02KS0PimPip_KS0LLTurbo',
        'Hlt2CharmHadDstp2D0Pip_D02KS0PimPip_KS0DD_LTUNBTurbo',
        'Hlt2CharmHadDstp2D0Pip_D02KS0PimPip_KS0LL_LTUNBTurbo',
        'Hlt2CharmHadDstp2D0Pip_D02KS0KmKp_KS0DDTurbo',
        'Hlt2CharmHadDstp2D0Pip_D02KS0KmKp_KS0LLTurbo',
        'Hlt2CharmHadDstp2D0Pip_D02KS0KmKp_KS0DD_LTUNBTurbo',
        'Hlt2CharmHadDstp2D0Pip_D02KS0KmKp_KS0LL_LTUNBTurbo'
    ]

    for line in lines:
        with open('{}.selections.txt'.format(line), 'w') as f:
            sys.stdout = f
            selections(tck, line)
