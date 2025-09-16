resultdict = {}

# dirac job created by ganga
from DIRAC.Core.Base.Script import parseCommandLine
parseCommandLine()
from LHCbDIRAC.Interfaces.API.DiracLHCb import DiracLHCb
from LHCbDIRAC.Interfaces.API.LHCbJob import LHCbJob
dirac = DiracLHCb()
sjNo='513.0'

j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894400--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(513.0)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_513.0_7f5e3e5e-06b7-4152-b8da-bd764075dc4e_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/diracInputFiles_513_7f5e3e5e-06b7-4152-b8da-bd764075dc4e.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/jobScripts-513_13432129-e077-46df-bfb2-517456949223.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000006_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000020_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000025_1.d0taunu.safestriptrig.dst'])

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
sjNo='513.1'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894400--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(513.1)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_513.1_7f5e3e5e-06b7-4152-b8da-bd764075dc4e_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/diracInputFiles_513_7f5e3e5e-06b7-4152-b8da-bd764075dc4e.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/jobScripts-513_13432129-e077-46df-bfb2-517456949223.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000016_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000024_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000008_1.d0taunu.safestriptrig.dst'])

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
sjNo='513.2'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894400--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(513.2)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_513.2_7f5e3e5e-06b7-4152-b8da-bd764075dc4e_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/diracInputFiles_513_7f5e3e5e-06b7-4152-b8da-bd764075dc4e.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/jobScripts-513_13432129-e077-46df-bfb2-517456949223.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000005_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000013_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000018_1.d0taunu.safestriptrig.dst'])

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
sjNo='513.3'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894400--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(513.3)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_513.3_7f5e3e5e-06b7-4152-b8da-bd764075dc4e_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/diracInputFiles_513_7f5e3e5e-06b7-4152-b8da-bd764075dc4e.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/jobScripts-513_13432129-e077-46df-bfb2-517456949223.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000010_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000001_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000002_1.d0taunu.safestriptrig.dst'])

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
sjNo='513.4'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894400--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(513.4)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_513.4_7f5e3e5e-06b7-4152-b8da-bd764075dc4e_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/diracInputFiles_513_7f5e3e5e-06b7-4152-b8da-bd764075dc4e.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/jobScripts-513_13432129-e077-46df-bfb2-517456949223.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000019_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000014_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000009_1.d0taunu.safestriptrig.dst'])

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
sjNo='513.5'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894400--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(513.5)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_513.5_7f5e3e5e-06b7-4152-b8da-bd764075dc4e_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/diracInputFiles_513_7f5e3e5e-06b7-4152-b8da-bd764075dc4e.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/jobScripts-513_13432129-e077-46df-bfb2-517456949223.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000004_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000015_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000023_1.d0taunu.safestriptrig.dst'])

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
sjNo='513.6'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894400--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(513.6)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_513.6_7f5e3e5e-06b7-4152-b8da-bd764075dc4e_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/diracInputFiles_513_7f5e3e5e-06b7-4152-b8da-bd764075dc4e.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/jobScripts-513_13432129-e077-46df-bfb2-517456949223.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000029_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000022_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000033_1.d0taunu.safestriptrig.dst'])

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
sjNo='513.7'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894400--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(513.7)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_513.7_7f5e3e5e-06b7-4152-b8da-bd764075dc4e_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/diracInputFiles_513_7f5e3e5e-06b7-4152-b8da-bd764075dc4e.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/jobScripts-513_13432129-e077-46df-bfb2-517456949223.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000007_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000017_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000028_1.d0taunu.safestriptrig.dst'])

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
sjNo='513.8'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894400--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(513.8)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_513.8_7f5e3e5e-06b7-4152-b8da-bd764075dc4e_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/diracInputFiles_513_7f5e3e5e-06b7-4152-b8da-bd764075dc4e.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/jobScripts-513_13432129-e077-46df-bfb2-517456949223.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000011_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000003_1.d0taunu.safestriptrig.dst'])

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
sjNo='513.9'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894400--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(513.9)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_513.9_7f5e3e5e-06b7-4152-b8da-bd764075dc4e_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/diracInputFiles_513_7f5e3e5e-06b7-4152-b8da-bd764075dc4e.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/jobScripts-513_13432129-e077-46df-bfb2-517456949223.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000021_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000032_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000027_1.d0taunu.safestriptrig.dst'])

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
sjNo='513.10'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894400--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(513.10)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_513.10_7f5e3e5e-06b7-4152-b8da-bd764075dc4e_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/diracInputFiles_513_7f5e3e5e-06b7-4152-b8da-bd764075dc4e.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/jobScripts-513_13432129-e077-46df-bfb2-517456949223.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000030_1.d0taunu.safestriptrig.dst'])

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
sjNo='513.11'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894400--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(513.11)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_513.11_7f5e3e5e-06b7-4152-b8da-bd764075dc4e_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/diracInputFiles_513_7f5e3e5e-06b7-4152-b8da-bd764075dc4e.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/jobScripts-513_13432129-e077-46df-bfb2-517456949223.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000012_1.d0taunu.safestriptrig.dst'])

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
sjNo='513.12'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894400--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(513.12)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_513.12_7f5e3e5e-06b7-4152-b8da-bd764075dc4e_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/diracInputFiles_513_7f5e3e5e-06b7-4152-b8da-bd764075dc4e.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/jobScripts-513_13432129-e077-46df-bfb2-517456949223.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000026_1.d0taunu.safestriptrig.dst'])

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
sjNo='513.13'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894400--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(513.13)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_513.13_7f5e3e5e-06b7-4152-b8da-bd764075dc4e_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/diracInputFiles_513_7f5e3e5e-06b7-4152-b8da-bd764075dc4e.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_513/InputFiles/jobScripts-513_13432129-e077-46df-bfb2-517456949223.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00219701/0000/00219701_00000031_1.d0taunu.safestriptrig.dst'])

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
