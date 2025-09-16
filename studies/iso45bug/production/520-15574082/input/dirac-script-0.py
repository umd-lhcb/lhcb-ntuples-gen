resultdict = {}

# dirac job created by ganga
from DIRAC.Core.Base.Script import parseCommandLine
parseCommandLine()
from LHCbDIRAC.Interfaces.API.DiracLHCb import DiracLHCb
from LHCbDIRAC.Interfaces.API.LHCbJob import LHCbJob
dirac = DiracLHCb()
sjNo='520.0'

j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.0)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.0_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000147_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000066_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000215_7.AllStreams.dst'])

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
sjNo='520.1'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.1)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.1_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000022_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000006_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000004_7.AllStreams.dst'])

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
sjNo='520.2'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.2)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.2_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000190_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000285_7.AllStreams.dst'])

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
sjNo='520.3'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.3)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.3_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000107_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000070_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000138_7.AllStreams.dst'])

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
sjNo='520.4'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.4)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.4_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000116_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000179_7.AllStreams.dst'])

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
sjNo='520.5'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.5)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.5_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000139_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000212_7.AllStreams.dst'])

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
sjNo='520.6'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.6)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.6_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000113_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000101_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000278_7.AllStreams.dst'])

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
sjNo='520.7'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.7)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.7_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000060_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000131_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000209_7.AllStreams.dst'])

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
sjNo='520.8'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.8)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.8_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000241_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000214_7.AllStreams.dst'])

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
sjNo='520.9'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.9)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.9_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000144_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000163_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000046_7.AllStreams.dst'])

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
sjNo='520.10'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.10)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.10_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000037_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000005_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000168_7.AllStreams.dst'])

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
sjNo='520.11'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.11)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.11_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000180_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000087_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000253_7.AllStreams.dst'])

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
sjNo='520.12'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.12)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.12_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000111_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000056_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000226_7.AllStreams.dst'])

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
sjNo='520.13'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.13)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.13_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000047_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000249_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000258_7.AllStreams.dst'])

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
sjNo='520.14'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.14)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.14_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000262_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000260_7.AllStreams.dst'])

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
sjNo='520.15'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.15)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.15_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000161_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000229_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000246_7.AllStreams.dst'])

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
sjNo='520.16'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.16)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.16_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000127_7.AllStreams.dst'])

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
sjNo='520.17'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.17)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.17_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000187_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000251_7.AllStreams.dst'])

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
sjNo='520.18'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.18)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.18_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000059_7.AllStreams.dst'])

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
sjNo='520.19'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.19)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.19_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000017_7.AllStreams.dst'])

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
sjNo='520.20'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.20)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.20_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000264_7.AllStreams.dst'])

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
sjNo='520.21'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574082--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(520.21)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_520.21_d9df1e39-3852-412e-950a-87fad13ae701_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/diracInputFiles_520_d9df1e39-3852-412e-950a-87fad13ae701.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_520/InputFiles/jobScripts-520_326ae3e3-b943-4a42-b176-7e5c4b199944.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173812/0000/00173812_00000250_7.AllStreams.dst'])

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
