import arcpy
import os

def getWorkspace():
    """Returns the current arcpy workspace."""
    return arcpy.env.workspace

def setWorkspace(workspace):
    """Sets the arcpy workspace and prints the current workspace."""
    arcpy.env.workspace = workspace
    print(arcpy.env.workspace)

def addFieldToAll(field_name, data_type="TEXT", wild_card=None, feature_dataset=None):
    """Adds a specified field name to each feature class in the current workspace set with setWorkspace().
    Default data type is TEXT. Default wildcard is None, default feature dataset is None."""
    workspace = getWorkspace()
    print('Current workspace is {}'.format(workspace))

    for FC in arcpy.ListFeatureClasses(wild_card, feature_dataset):
        arcpy.AddField_management(FC, field_name, data_type)
        print('Field {0} added to {1}'.format(field_name, FC))

    print('add field task completed')

def fillFields(in_FC, in_dict):
    """Function uses a dictionary where the field is the key and the associated value is the parameter the
    field is filled with. This function currently fills each field with a single value."""
    workspace = getWorkspace()
    print('Current workspace is {}'.format(workspace))

    if in_dict and in_FC:
        for item in in_dict.items():
            field = item[0]
            fill_value = item[1]

            with arcpy.da.UpdateCursor(in_FC, field) as cursor:
                for row in cursor:
                    row[0] = fill_value

                    cursor.updateRow(row)

    print('fillFields task completed.')


def createAbbreviations(FC_list):
    """This function takes in a list of feature classes and compares each value in the list to the key of a
    dictionary named abbrev_dict. Feature classes that have the same name as a key in the dictionary will have
    an abbreviation field created and filled with the corresponding abbreviation."""

    abbrev_dict = {'ADDRESS_POINTS':'ADDR', 'HENDERSON_COUNTY':'PROVIS_BOUND','ROAD_CENTERLINE':'RCL',
                   'EMERGENCYSERVICEZONES':'EMERG_BOUND', 'EMS':'EMS', 'PSAP_BOUNDARY':'PSAP_BOUND',
                   'FIREDEPTS':'FDEPT', 'HYDRANTS':'FHYD', 'CEMETERIES':'CEMTY', 'SCHOOL':'SCHL',
                   'HOSPITAL':'HSPTL', 'HENDERSON_COUNTY_CITY_LIMITS_TXDOT':'MUNCPL', 'RAILROAD':'RR'}

    for FC in FC_list:
        #match the feature class to the dictionary key
        if str(FC.upper()) in abbrev_dict.keys():
            print('feature class {} paired'.format(FC))

            #create the appropriate fill dictionary for each feature class
            fill_dict = {'Abbreviation': abbrev_dict[FC.upper()]}
            fillFields(FC, fill_dict)


def objectID_adjust(in_num):
    """This function takes in a number, converts it to a string,
    and then pads the number with zeroes (padded from left) until it
    is at least 6 digits."""

    new_num = str(in_num)

    while len(new_num) < 6:
        new_num = '0' + new_num

    return new_num


def createOIDTag(FC_list):
    """This function uses the objectID_adjust function to add a unique tag based
     on the ObjectID for each record in each feature class contained in FC_list."""

    origin_field = "OBJECTID"
    target_field = "OID_Tag"
    fields = [origin_field, target_field]

    for FC in FC_list:
        with arcpy.da.UpdateCursor(FC, fields) as cursor:
            for row in cursor:
                row[1] = objectID_adjust(row[0])
                cursor.updateRow(row)

    print("OID tags added successfully")


def createNGUID(FC_list):
    """This function creates a globally unique NENA ID for each record in each feature class of the
    input dataset or workspace by taking in the feature class abbreviation, adjusted object ID, and
    the agency identifier."""

    nguid_field = "NGUID"
    objectID_field = "OID_TAG"
    abbrev_field = "ABBREVIATION"
    agency_field = 'AGENCY_ID'
    fields = [nguid_field, abbrev_field, objectID_field, agency_field]

    for FC in FC_list:
        with arcpy.da.UpdateCursor(FC, fields) as cursor:
            for row in cursor:
                if row[1] == None:
                    print("Feature class {} has no NGUID abbreviation set.".format(FC))
                    break
                row[0] = row[1] + row[2] + row[3]
                cursor.updateRow(row)

    print("Nena unique IDs successfully created")
