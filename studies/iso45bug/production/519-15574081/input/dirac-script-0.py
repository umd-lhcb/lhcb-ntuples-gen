resultdict = {}

# dirac job created by ganga
from DIRAC.Core.Base.Script import parseCommandLine
parseCommandLine()
from LHCbDIRAC.Interfaces.API.DiracLHCb import DiracLHCb
from LHCbDIRAC.Interfaces.API.LHCbJob import LHCbJob
dirac = DiracLHCb()
sjNo='519.0'

j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.0)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.0_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000193_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000203_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000239_7.AllStreams.dst'])

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
sjNo='519.1'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.1)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.1_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000084_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000235_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000180_7.AllStreams.dst'])

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
sjNo='519.2'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.2)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.2_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000072_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000111_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000057_7.AllStreams.dst'])

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
sjNo='519.3'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.3)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.3_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000206_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000137_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000133_7.AllStreams.dst'])

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
sjNo='519.4'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.4)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.4_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000194_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000195_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000077_7.AllStreams.dst'])

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
sjNo='519.5'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.5)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.5_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000104_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000188_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000088_7.AllStreams.dst'])

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
sjNo='519.6'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.6)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.6_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000217_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000154_7.AllStreams.dst'])

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
sjNo='519.7'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.7)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.7_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000059_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000210_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000226_7.AllStreams.dst'])

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
sjNo='519.8'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.8)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.8_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000018_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000097_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000096_7.AllStreams.dst'])

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
sjNo='519.9'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.9)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.9_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000035_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000050_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000148_7.AllStreams.dst'])

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
sjNo='519.10'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.10)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.10_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000068_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000123_7.AllStreams.dst'])

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
sjNo='519.11'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.11)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.11_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000284_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000164_7.AllStreams.dst'])

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
sjNo='519.12'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.12)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.12_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000085_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000029_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000039_7.AllStreams.dst'])

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
sjNo='519.13'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.13)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.13_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000014_7.AllStreams.dst'])

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
sjNo='519.14'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.14)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.14_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000016_7.AllStreams.dst'])

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
sjNo='519.15'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.15)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.15_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000004_7.AllStreams.dst'])

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
sjNo='519.16'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.16)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.16_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000198_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000300_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000091_7.AllStreams.dst'])

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
sjNo='519.17'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.17)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.17_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000089_7.AllStreams.dst'])

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
sjNo='519.18'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.18)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.18_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000162_7.AllStreams.dst'])

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
sjNo='519.19'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.19)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.19_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000167_7.AllStreams.dst'])

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
sjNo='519.20'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.20)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.20_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000301_7.AllStreams.dst'])

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
sjNo='519.21'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.21)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.21_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000093_7.AllStreams.dst', 'LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000026_7.AllStreams.dst'])

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
sjNo='519.22'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.22)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.22_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000215_7.AllStreams.dst'])

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
sjNo='519.23'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--15574081--MC_2016_Beam6500GeV-2016-MagDown-Nu__{Ganga_GaudiExec_(519.23)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_519.23_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/diracInputFiles_519_95ac0898-b1e3-4ba2-8db7-a0e9916ec57f.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_519/InputFiles/jobScripts-519_65f62a0d-2c50-4891-ab75-3af88186799e.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00173814/0000/00173814_00000222_7.AllStreams.dst'])

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
