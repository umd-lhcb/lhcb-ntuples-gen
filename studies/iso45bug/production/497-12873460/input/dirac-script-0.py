resultdict = {}

# dirac job created by ganga
from DIRAC.Core.Base.Script import parseCommandLine
parseCommandLine()
from LHCbDIRAC.Interfaces.API.DiracLHCb import DiracLHCb
from LHCbDIRAC.Interfaces.API.LHCbJob import LHCbJob
dirac = DiracLHCb()
sjNo='497.0'

j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12873460--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(497.0)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_497.0_77a35ccd-f9fa-4a45-a85b-2c835de365bf_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_497/InputFiles/diracInputFiles_497_77a35ccd-f9fa-4a45-a85b-2c835de365bf.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_497/InputFiles/jobScripts-497_20ee4985-616c-424a-af68-049e64e2ad70.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000004_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000005_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000016_1.d0taunu.safestriptrig.dst'])

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
sjNo='497.1'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12873460--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(497.1)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_497.1_77a35ccd-f9fa-4a45-a85b-2c835de365bf_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_497/InputFiles/diracInputFiles_497_77a35ccd-f9fa-4a45-a85b-2c835de365bf.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_497/InputFiles/jobScripts-497_20ee4985-616c-424a-af68-049e64e2ad70.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000011_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000002_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000007_1.d0taunu.safestriptrig.dst'])

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
sjNo='497.2'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12873460--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(497.2)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_497.2_77a35ccd-f9fa-4a45-a85b-2c835de365bf_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_497/InputFiles/diracInputFiles_497_77a35ccd-f9fa-4a45-a85b-2c835de365bf.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_497/InputFiles/jobScripts-497_20ee4985-616c-424a-af68-049e64e2ad70.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000006_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000013_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000012_1.d0taunu.safestriptrig.dst'])

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
sjNo='497.3'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12873460--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(497.3)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_497.3_77a35ccd-f9fa-4a45-a85b-2c835de365bf_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_497/InputFiles/diracInputFiles_497_77a35ccd-f9fa-4a45-a85b-2c835de365bf.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_497/InputFiles/jobScripts-497_20ee4985-616c-424a-af68-049e64e2ad70.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000001_1.d0taunu.safestriptrig.dst'])

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
sjNo='497.4'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12873460--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(497.4)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_497.4_77a35ccd-f9fa-4a45-a85b-2c835de365bf_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_497/InputFiles/diracInputFiles_497_77a35ccd-f9fa-4a45-a85b-2c835de365bf.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_497/InputFiles/jobScripts-497_20ee4985-616c-424a-af68-049e64e2ad70.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000015_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000008_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000009_1.d0taunu.safestriptrig.dst'])

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
sjNo='497.5'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12873460--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(497.5)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_497.5_77a35ccd-f9fa-4a45-a85b-2c835de365bf_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_497/InputFiles/diracInputFiles_497_77a35ccd-f9fa-4a45-a85b-2c835de365bf.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_497/InputFiles/jobScripts-497_20ee4985-616c-424a-af68-049e64e2ad70.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000010_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000014_1.d0taunu.safestriptrig.dst'])

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
sjNo='497.6'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--12873460--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(497.6)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_497.6_77a35ccd-f9fa-4a45-a85b-2c835de365bf_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_497/InputFiles/diracInputFiles_497_77a35ccd-f9fa-4a45-a85b-2c835de365bf.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_497/InputFiles/jobScripts-497_20ee4985-616c-424a-af68-049e64e2ad70.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140834/0000/00140834_00000003_1.d0taunu.safestriptrig.dst'])

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
