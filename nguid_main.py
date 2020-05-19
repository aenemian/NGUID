import nguid
from nguid import *

nguid.setWorkspace(r'S:\mapdata\Vestamap Local Data\HCTX911_May_18_2020_Submission\HCTX911_May_18_2020_VML_Submission.gdb')
nguid.getWorkspace()

#add fields ABBREVIATION, OID_TAG, AGENCY_ID
field_list = ['ABBREVIATION', 'OID_TAG', 'AGENCY_ID', 'NGUID']
field_dict = {'AGENCY_ID':'@hctx911.org'}
FC_list = arcpy.ListFeatureClasses()


for field in field_list:
    #MIGHT WANT TO DESIGNATE DATASET FOR SIMPLICITY
    addFieldToAll(field)

#populate AGENCY_ID
for FC in FC_list:
    fillFields(FC, field_dict)

#populate ABBREVIATIONS
createAbbreviations(FC_list)

#populate OID_TAG
createOIDTag(FC_list)

#create NGUID
createNGUID(FC_list)
