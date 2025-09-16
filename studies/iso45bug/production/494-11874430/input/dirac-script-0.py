resultdict = {}

# dirac job created by ganga
from DIRAC.Core.Base.Script import parseCommandLine
parseCommandLine()
from LHCbDIRAC.Interfaces.API.DiracLHCb import DiracLHCb
from LHCbDIRAC.Interfaces.API.LHCbJob import LHCbJob
dirac = DiracLHCb()
sjNo='494.0'

j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.0)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.0_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000084_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.1'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.1)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.1_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000078_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000181_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000199_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.2'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.2)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.2_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000146_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000031_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000204_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.3'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.3)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.3_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000122_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000010_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000067_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.4'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.4)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.4_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000006_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000021_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000250_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.5'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.5)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.5_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000035_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000296_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000387_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.6'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.6)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.6_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000019_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000156_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.7'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.7)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.7_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000136_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000124_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000231_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.8'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.8)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.8_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000176_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.9'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.9)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.9_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000191_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000508_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000444_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.10'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.10)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.10_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000211_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000218_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000222_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.11'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.11)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.11_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000254_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000348_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000401_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.12'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.12)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.12_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000200_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000482_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000491_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.13'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.13)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.13_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000266_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000297_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000434_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.14'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.14)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.14_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000277_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000397_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000414_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.15'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.15)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.15_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000318_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.16'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.16)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.16_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000337_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.17'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.17)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.17_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000441_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000379_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.18'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.18)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.18_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000343_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000405_1.d0taunu.safestriptrig.dst', 'LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000349_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.19'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.19)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.19_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000312_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.20'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.20)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.20_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000413_1.d0taunu.safestriptrig.dst'])

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
sjNo='494.21'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--mc--11874430--tracker_only--MC_2016_Beam6500GeV-2__{Ganga_GaudiExec_(494.21)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_494.21_f13e03bc-78a2-4569-adcf-4f9bdb2798a3_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/diracInputFiles_494_f13e03bc-78a2-4569-adcf-4f9bdb2798a3.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_494/InputFiles/jobScripts-494_6df2b5e1-8db5-4ac4-b6f9-bc26878b3964.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/MC/2016/D0TAUNU.SAFESTRIPTRIG.DST/00140840/0000/00140840_00000560_1.d0taunu.safestriptrig.dst'])

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
