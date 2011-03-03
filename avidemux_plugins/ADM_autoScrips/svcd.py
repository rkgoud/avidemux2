###############################################
#      Convert to SVCD adm tinypy script
#      Mean 2011
###############################################

import ADM_resize
import ADM_image
finalSizeWidth=720               # Start with DVD target, we'll adjust later
finalSizeHeight=[ 480,576]
#
aspectRatio=[
	(1.,0.888888,1.19), # NTSC 1:1 4:3 16:9
        (1.,1.066667,1.43),  # PAL  1:1 4:3 16:9
	(1.,0.888888,1.19), # FILM 1:1 4:3 16:9
]
fps_predef=[ 29970, 25000, 23976]
#
MP2=80
supported=[MP2]
adm=Avidemux()
##########################
# Compute resize...
##########################
source=ADM_image.image()
dest=ADM_image.image()

fps=adm.getFps1000()
fmt=source.getFormat(fps)
true_fmt=fmt
print("Fps    : "+str(fps))
print("Format : "+str(fmt))
if(fmt==ADM_image.FMT_UNKNOWN):
    exit()
source.width=adm.getWidth()
source.height=adm.getHeight()
desc="NTSC"
if(fmt==ADM_image.FMT_FILM):
    fmt=ADM_image.FMT_NTSC
    desc="FILM"
if(fmt==ADM_image.FMT_PAL):
    desc="PAL"
source.fmt=fmt
dest.fmt=fmt
print("Format : "+str(fmt))
dest.width=16
dest.height=16
#*****************************
# Dialog...
#*****************************
#
mnuResolution = DFMenu("Resolution:");
mnuSourceRatio = DFMenu("Source Aspect Ratio:");
mnuSourceRatio.addItem("1:1")
mnuSourceRatio.addItem("4:3")
mnuSourceRatio.addItem("16:9")
mnuDestRatio = DFMenu("Destination Aspect Ratio:");
mnuDestRatio.addItem("4:3")
mnuDestRatio.addItem("16:9")

dlgWizard = DialogFactory("auto SVCD ("+desc+")");
dlgWizard.addControl(mnuSourceRatio);
dlgWizard.addControl(mnuDestRatio);
res=dlgWizard.show()
if res!=1:
    exit()
source.ar=mnuSourceRatio.index
dest.ar=mnuDestRatio.index+1
resizer=source.compute_resize(source,dest,finalSizeWidth,finalSizeHeight,aspectRatio)
if(resizer is None):
    exit()
print("Resize to "+str(resizer.width)+"x"+str(resizer.height))
# Correct so that result is 2/3 D1 i.e. 480xxxx
newW=resizer.width
newW=(newW*480)/720
newW=newW&0xffc
resizer.width=newW
resizer.leftright=(480-newW)/2
source.apply_resize(resizer)
############################
# Handle audio....
############################
encoding=adm.audioEncoding
fq=adm.audioEncoding
channels=adm.audioChannels
reencode=False
# 1 check frequency
if(fq != 44100):
    adm.audioResample=44100
    reencode=True
if(not(encoding in supported)):
    reencode=True
if(channels!=2):
    adm.audioMixer="STEREO"
    reencode=True
if(True==reencode):
    adm.audioCodec("TwoLame",160)
##################################
#  Video
##################################
ff_ar=0
if(resizer.ar==ADM_image.AR_16_9):
    ff_ar=1
#
adm.videoCodec("ffMpeg2","params=CQ=4","lavcSettings=:version=2:MultiThreaded=2:me_method=5:_GMC=0:_4MV=0:_QPEL=0:_TRELLIS_QUANT=1:qmin=2:qmax=31:max_qdiff=3:max_b_frames=2:mpeg_quant=1:is_luma_elim_threshold=1:luma_elim_threshold=4294967294:is_chroma_elim_threshold=1:chroma_elim_threshold=4294967291:lumi_masking=0.050000:is_lumi_masking=1:dark_masking=0.010000:is_dark_masking=1:qcompress=0.500000:qblur=0.500000:minBitrate=0:maxBitrate=2400:user_matrix=1:gop_size=18:interlaced=0:bff=0:widescreen="+str(ff_ar)+":mb_eval=2:vratetol=8000:is_temporal_cplx_masking=0:temporal_cplx_masking=0.000000:is_spatial_cplx_masking=0:spatial_cplx_masking=0.000000:_NORMALIZE_AQP=0:use_xvid_ratecontrol=0:bufferSize=112:override_ratecontrol=0:dummy=0","matrix=1")

###################################
# Container = Mpeg PS/DVD
###################################
#
adm.setContainer("ffPS","muxingType=1","acceptNonCompliant=False","muxRatekBits=2800","videoRatekBits=2400","bufferSizekBytes=112")
#

    
