resultdict = {}

# dirac job created by ganga
from DIRAC.Core.Base.Script import parseCommandLine
parseCommandLine()
from LHCbDIRAC.Interfaces.API.DiracLHCb import DiracLHCb
from LHCbDIRAC.Interfaces.API.LHCbJob import LHCbJob
dirac = DiracLHCb()
sjNo='500.0'

j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.0)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.0_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000059_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000019_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000014_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.1'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.1)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.1_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000062_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000008_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000006_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.2'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.2)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.2_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000057_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000091_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000016_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.3'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.3)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.3_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000086_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.4'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.4)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.4_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000082_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.5'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.5)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.5_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000056_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000024_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000001_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.6'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.6)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.6_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000074_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000002_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000089_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.7'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.7)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.7_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000085_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000032_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000039_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.8'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.8)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.8_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000049_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000050_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000038_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.9'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.9)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.9_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000064_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000025_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000018_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.10'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.10)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.10_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000066_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000040_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000070_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.11'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.11)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.11_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000054_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.12'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.12)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.12_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000020_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000058_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000080_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.13'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.13)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.13_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000034_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.14'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.14)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.14_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000090_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000027_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000079_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.15'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.15)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.15_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000076_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.16'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.16)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.16_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000017_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.17'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.17)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.17_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000003_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000051_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000083_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.18'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.18)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.18_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000007_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000081_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.19'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.19)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.19_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000048_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.20'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.20)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.20_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000060_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.21'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.21)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.21_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000065_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000063_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
sjNo='500.22'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12675402--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(500.22)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_500.22_8a75fd92-f9de-49f4-9868-0f8bb3727444_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/diracInputFiles_500_8a75fd92-f9de-49f4-9868-0f8bb3727444.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_500/InputFiles/jobScripts-500_6166e190-03dd-4584-8df3-ada073c45fec.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000073_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140822/0000/00140822_00000088_1.d0taunu.safestriptrig.dst'])

j.setOutputData(['*.root'], OutputPath='', OutputSE=[])


# <-- user settings
j.setCPUTime(1000000)

# user settings -->

# diracOpts added by user


# submit the job to dirac
j.setDIRACPlatform()

try:
	j.setNumberOfProcessors(minNumberOfProcessors=1, maxNumberOfProcessors=1)
except (AttributeError, TypeError):
	pass

j._addParameter(j.workflow, 'GangaVersion', 'JDL', '8.7.12', 'The version of ganga used to submit this job')

result = dirac.submitJob(j)
if isinstance(result, dict) and 'Value' in result:
	resultdict.update({sjNo : result['Value']})
else:
	resultdict.update({sjNo : result['Message']})
output(resultdict)
