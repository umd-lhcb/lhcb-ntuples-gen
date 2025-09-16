import os
# import sys

def scp_jobs(nums, names):
    # print('scp -r afernez@lxplus.cern.ch:~/eos-user/ganga_output/afernez/LocalXML/\{' + f'{",".join(nums)}' + '\} ./')
    os.system('scp -r afernez@lxplus.cern.ch:~/eos-user/ganga_output/afernez/LocalXML/\{' + f'{",".join(nums)}' + '\} ./')
    for i in range(len(nums)): os.system(f'mv {nums[i]} {nums[i]}-{names[i]}')

jobs = '''
Job 486: Dst_D0-testIso45Bug--25_08_27--std--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r2_90000000_SEMILEPTONIC.DST.root, status completed
Job 487: Dst_D0-testIso45Bug--25_08_27--mu_misid--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r2_90000000_SEMILEPTONIC.DST.root, status failed
Job 488: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_11574011_D0TAUNU.SAFESTRIPTRIG.DST.root, status failed
Job 489: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root, status completed
Job 490: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_12573012_D0TAUNU.SAFESTRIPTRIG.DST.root, status submitted
Job 494: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_11874430_D0TAUNU.SAFESTRIPTRIG.DST.root, status failed
Job 496: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_12873450_D0TAUNU.SAFESTRIPTRIG.DST.root, status failed
Job 497: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_12873460_D0TAUNU.SAFESTRIPTRIG.DST.root, status failed
Job 500: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_12675402_D0TAUNU.SAFESTRIPTRIG.DST.root, status failed
Job 501: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_11676012_D0TAUNU.SAFESTRIPTRIG.DST.root, status completed
Job 504: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_13674000_D0TAUNU.SAFESTRIPTRIG.DST.root, status completed
Job 505: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_11894600_D0TAUNU.SAFESTRIPTRIG.DST.root, status failed
Job 509: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_11894610_D0TAUNU.SAFESTRIPTRIG.DST.root, status completed
Job 510: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_12895400_D0TAUNU.SAFESTRIPTRIG.DST.root, status failed
Job 511: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_11894210_D0TAUNU.SAFESTRIPTRIG.DST.root, status completed
Job 512: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_12895000_D0TAUNU.SAFESTRIPTRIG.DST.root, status failed
Job 513: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_11894400_D0TAUNU.SAFESTRIPTRIG.DST.root, status completed
Job 514: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_12895410_D0TAUNU.SAFESTRIPTRIG.DST.root, status failed
Job 519: Dst_D0-testIso45Bug--25_08_27--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim10b_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_15574081_ALLSTREAMS.DST.root, status completed
Job 520: Dst_D0-testIso45Bug--25_08_27--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim10b_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_15574082_ALLSTREAMS.DST.root, status running
Job 521: Dst_D0-testIso45Bug--25_08_27--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim10b_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_15574083_ALLSTREAMS.DST.root, status failed
Job 522: Dst_D0-testIso45Bug--25_08_27--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim10b_Reco16_CustomFiltered_11895400_D0TAUNU.SAFESTRIPTRIG.DST.root, status completed
'''
nums = []
names = []
for job in jobs.split('\n'):
    if not 'Job ' in job: continue
    num = job.split('ob ')[1][:3]
    name = job.split('--')[2]
    if name=='mc':
        if 'tracker_only' in job: name = job.split('Filtered_')[1][:8]
        else: name = name = job.split('Flagged_')[1][:8]
    nums.append(num)
    names.append(name)
    # print(f'Copying {job}, from lxplus to {num}-{name}')
scp_jobs(nums, names)