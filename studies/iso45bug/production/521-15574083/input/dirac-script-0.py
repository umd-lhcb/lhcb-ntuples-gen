resultdict = {}

# dirac job created by ganga
from DIRAC.Core.Base.Script import parseCommandLine
parseCommandLine()
from LHCbDIRAC.Interfaces.API.DiracLHCb import DiracLHCb
from LHCbDIRAC.Interfaces.API.LHCbJob import LHCbJob
dirac = DiracLHCb()
sjNo='521.0'

j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.0)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.0_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000160_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000161_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000285_7.AllStreams.dst'])

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
sjNo='521.1'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.1)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.1_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000145_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000009_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000277_7.AllStreams.dst'])

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
sjNo='521.2'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.2)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.2_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000079_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000030_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000100_7.AllStreams.dst'])

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
sjNo='521.3'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.3)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.3_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000008_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000182_7.AllStreams.dst'])

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
sjNo='521.4'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.4)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.4_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000069_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000005_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000032_7.AllStreams.dst'])

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
sjNo='521.5'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.5)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.5_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000176_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000124_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000191_7.AllStreams.dst'])

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
sjNo='521.6'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.6)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.6_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000143_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000058_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000264_7.AllStreams.dst'])

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
sjNo='521.7'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.7)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.7_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000171_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000299_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000002_7.AllStreams.dst'])

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
sjNo='521.8'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.8)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.8_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000083_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000010_7.AllStreams.dst'])

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
sjNo='521.9'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.9)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.9_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000061_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000246_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000261_7.AllStreams.dst'])

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
sjNo='521.10'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.10)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.10_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000011_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000268_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000119_7.AllStreams.dst'])

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
sjNo='521.11'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.11)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.11_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000279_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000188_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000157_7.AllStreams.dst'])

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
sjNo='521.12'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.12)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.12_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000253_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000289_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000217_7.AllStreams.dst'])

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
sjNo='521.13'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.13)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.13_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000175_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000111_7.AllStreams.dst'])

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
sjNo='521.14'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.14)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.14_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000040_7.AllStreams.dst'])

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
sjNo='521.15'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.15)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.15_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000179_7.AllStreams.dst'])

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
sjNo='521.16'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.16)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.16_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000115_7.AllStreams.dst'])

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
sjNo='521.17'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.17)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.17_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000112_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000284_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000292_7.AllStreams.dst'])

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
sjNo='521.18'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.18)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.18_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000062_7.AllStreams.dst'])

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
sjNo='521.19'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.19)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.19_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000101_7.AllStreams.dst'])

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
sjNo='521.20'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.20)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.20_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000114_7.AllStreams.dst'])

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
sjNo='521.21'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.21)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.21_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000142_7.AllStreams.dst'])

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
sjNo='521.22'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574083--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(521.22)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_521.22_17b524e5-0a01-4861-83f0-5e39600385b7_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/diracInputFiles_521_17b524e5-0a01-4861-83f0-5e39600385b7.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_521/InputFiles/jobScripts-521_24e104c0-7e95-4cdb-bc95-0a85c0fa779e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173808/0000/00173808_00000209_7.AllStreams.dst'])

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
