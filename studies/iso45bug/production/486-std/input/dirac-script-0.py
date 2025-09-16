resultdict = {}

# dirac job created by ganga
from DIRAC.Core.Base.Script import parseCommandLine
parseCommandLine()
from LHCbDIRAC.Interfaces.API.DiracLHCb import DiracLHCb
from LHCbDIRAC.Interfaces.API.LHCbJob import LHCbJob
dirac = DiracLHCb()
sjNo='486.0'

j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--std--LHCb_Collision16_Beam6500GeV-VeloClosed-MagD__{Ganga_GaudiExec_(486.0)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_486.0_d8ed90aa-864f-4d26-941f-451bffe1b7f8_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_486/InputFiles/diracInputFiles_486_d8ed90aa-864f-4d26-941f-451bffe1b7f8.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_486/InputFiles/jobScripts-486_5cfbd77a-959f-46c8-8d8e-8a8189e6b019.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00001291_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00001585_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00001391_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00001986_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000213_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000490_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00001676_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002183_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002107_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002542_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00001419_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000352_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00001050_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002350_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002583_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002315_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002930_1.semileptonic.dst'])

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
sjNo='486.1'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--std--LHCb_Collision16_Beam6500GeV-VeloClosed-MagD__{Ganga_GaudiExec_(486.1)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_486.1_d8ed90aa-864f-4d26-941f-451bffe1b7f8_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_486/InputFiles/diracInputFiles_486_d8ed90aa-864f-4d26-941f-451bffe1b7f8.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_486/InputFiles/jobScripts-486_5cfbd77a-959f-46c8-8d8e-8a8189e6b019.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000428_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000064_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00001466_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000559_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002009_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002110_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000102_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00001193_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000622_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000481_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000444_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00001438_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000264_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000674_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000110_1.semileptonic.dst'])

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
sjNo='486.2'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--std--LHCb_Collision16_Beam6500GeV-VeloClosed-MagD__{Ganga_GaudiExec_(486.2)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_486.2_d8ed90aa-864f-4d26-941f-451bffe1b7f8_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_486/InputFiles/diracInputFiles_486_d8ed90aa-864f-4d26-941f-451bffe1b7f8.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_486/InputFiles/jobScripts-486_5cfbd77a-959f-46c8-8d8e-8a8189e6b019.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000654_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002157_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000433_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00001724_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00001786_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000459_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000835_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002603_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002565_1.semileptonic.dst'])

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
sjNo='486.3'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--std--LHCb_Collision16_Beam6500GeV-VeloClosed-MagD__{Ganga_GaudiExec_(486.3)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_486.3_d8ed90aa-864f-4d26-941f-451bffe1b7f8_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_486/InputFiles/diracInputFiles_486_d8ed90aa-864f-4d26-941f-451bffe1b7f8.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_486/InputFiles/jobScripts-486_5cfbd77a-959f-46c8-8d8e-8a8189e6b019.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000664_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00001206_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00000411_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00001593_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00001053_1.semileptonic.dst'])

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
sjNo='486.4'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--std--LHCb_Collision16_Beam6500GeV-VeloClosed-MagD__{Ganga_GaudiExec_(486.4)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_486.4_d8ed90aa-864f-4d26-941f-451bffe1b7f8_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_486/InputFiles/diracInputFiles_486_d8ed90aa-864f-4d26-941f-451bffe1b7f8.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_486/InputFiles/jobScripts-486_5cfbd77a-959f-46c8-8d8e-8a8189e6b019.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002293_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002289_1.semileptonic.dst', 'LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002292_1.semileptonic.dst'])

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
sjNo='486.5'
# dirac job created by ganga




j = LHCbJob()

# default commands added by ganga
j.setName('Dst_D0-testIso45Bug--25_08_27--std--LHCb_Collision16_Beam6500GeV-VeloClosed-MagD__{Ganga_GaudiExec_(486.5)}')


j.setExecutable('jobScript/GaudiExec_afernez_Job_486.5_d8ed90aa-864f-4d26-941f-451bffe1b7f8_script.py','','Ganga_GaudiExec.log', systemConfig='x86_64-centos7-gcc9-opt')
j.setInputSandbox(['LFN:/lhcb/user/a/afernez/GangaJob_486/InputFiles/diracInputFiles_486_d8ed90aa-864f-4d26-941f-451bffe1b7f8.tgz', 'LFN:/lhcb/user/a/afernez/GangaJob_486/InputFiles/jobScripts-486_5cfbd77a-959f-46c8-8d8e-8a8189e6b019.tar.gz'])
j.setOutputSandbox(['__postprocesslocations__'])
j.setInputData(['LFN:/lhcb/LHCb/Collision16/SEMILEPTONIC.DST/00103400/0000/00103400_00002131_1.semileptonic.dst'])

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
