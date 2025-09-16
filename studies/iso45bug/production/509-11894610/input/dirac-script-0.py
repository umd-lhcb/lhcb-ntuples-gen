resultdict = {}

# dirac job created by ganga
from DIRAC.Core.Base.Script import parseCommandLine
parseCommandLine()
from LHCbDIRAC.Interfaces.API.DiracLHCb import DiracLHCb
from LHCbDIRAC.Interfaces.API.LHCbJob import LHCbJob
dirac = DiracLHCb()
sjNo='509.0'

j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.0)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.0_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000024_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000127_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000252_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.1'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.1)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.1_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000014_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000033_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000187_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.2'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.2)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.2_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000087_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.3'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.3)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.3_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000053_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000074_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000125_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.4'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.4)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.4_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000071_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000012_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.5'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.5)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.5_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000142_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.6'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.6)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.6_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000069_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000149_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000171_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.7'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.7)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.7_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000135_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000206_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000221_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.8'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.8)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.8_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000159_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000200_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000145_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.9'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.9)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.9_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000146_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000090_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.10'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.10)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.10_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000170_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000004_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000021_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.11'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.11)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.11_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000180_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000213_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000160_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.12'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.12)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.12_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000223_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.13'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.13)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.13_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000204_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000194_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000018_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.14'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.14)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.14_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000044_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000230_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.15'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.15)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.15_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000013_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000030_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000105_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.16'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.16)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.16_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000039_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.17'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.17)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.17_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000073_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.18'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.18)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.18_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000078_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.19'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.19)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.19_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000131_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000109_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000220_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.20'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.20)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.20_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000111_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.21'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.21)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.21_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000123_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.22'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.22)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.22_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000243_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000154_1.d0taunu.safestriptrig.dst'])

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
sjNo='509.23'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11894610--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(509.23)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_509.23_1c52fda8-fffc-48c0-a287-433c29024e7d_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/diracInputFiles_509_1c52fda8-fffc-48c0-a287-433c29024e7d.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_509/InputFiles/jobScripts-509_ba586c58-83a5-4360-ab84-2c49524e6417.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140810/0000/00140810_00000239_1.d0taunu.safestriptrig.dst'])

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
