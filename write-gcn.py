import os
import argparse
import re
import numpy as np
from astropy.time import Time
from datetime import datetime
# Function to convert AstroSat time to UTC
# Defining default values and constants
Epoch_Time=157766400; # Total numbers of seconds from 2010.00.00.00.00 till 2015.00.00.00.00
Epoch_Date=Time('2010-01-01 00:00:00', scale='utc')
def convertAStoAll(Astrosat_second):
    ND=int((Astrosat_second-Epoch_Time)//86400); # No of days  
    NS=(Astrosat_second-Epoch_Time)%86400;
    NH=int(NS//3600);  # No of hours 
    NHS=NS%3600;
    NM=int(NHS//60); # No of minutes 
    #print NM
    NOS=float(NHS%60); # No of seconds  with fraction 
    #print NOS
    NOSI=str(NOS)[0]
    NOSF=str(NOS)[1:]
    year=2015;
    dayr=ND;
    while (dayr>0):
        if((year%4)==0):
            NDY=366
        else:
            NDY=365
        dayr=dayr-NDY;
        if (dayr>0):
            year=year+1;
        else: 
            DaY=dayr+NDY+1;
    if NH==0 and NM==0 and NOS==0.0:
        Astrosat_Yr=str(year)+str(':')+str(DaY)+str(':')+str(NH)+str(NH)+str(':')+str(NM)+str(NM)+str(':')+NOSI+NOSI+NOSF;
    elif NH==0:
        Astrosat_Yr=str(year)+str(':')+str(DaY)+str(':')+str(NH)+str(NH)+str(':')+str(NM)+str(':')+NOSI+NOSF;
    elif NM==0:
        Astrosat_Yr=str(year)+str(':')+str(DaY)+str(':')+str(NH)+str(':')+str(NM)+str(NM)+str(':')+NOSI+NOSF;
    elif NOS==0.0:      
        Astrosat_Yr=str(year)+str(':')+str(DaY)+str(':')+str(NH)+str(':')+str(NM)+str(':')+NOSI+NOSI+NOSF;
    elif NH==0 and NM==0:
        Astrosat_Yr=str(year)+str(':')+str(DaY)+str(':')+str(NH)+str(NH)+str(':')+str(NM)+str(NM)+str(':')+NOSI+NOSF;
    elif NM==0 and NOS==0.0:
        Astrosat_Yr=str(year)+str(':')+str(DaY)+str(':')+str(NH)+str(':')+str(NM)+str(NM)+str(':')+NOSI+NOSI+NOSF;
    elif NH==0 and NOS==0.0:
        Astrosat_Yr=str(year)+str(':')+str(DaY)+str(':')+str(NH)+str(NH)+str(':')+str(NM)+str(':')+NOSI+NOSI+NOSF;     
    else: 
        Astrosat_Yr=str(year)+str(':')+str(DaY)+str(':')+str(NH)+str(':')+str(NM)+str(':')+NOSI+NOSF;
    Astrosat_yday_obj=Time(Astrosat_Yr, scale='utc')
    Astrosat_iso=Astrosat_yday_obj.iso
    return Astrosat_iso

print("\n------------------------------------------------------------------------------------------")
print("*********  Enter the details to create Detection Mail & GCN Draft  *********\n")
grb_name = str(input('GRB Name: '))
# Read and Scrape GRB_name.txt file
file_path = f"/home/npk/NPKCZTI/testarea/Astrosat-Detected/{grb_name}/{grb_name}.txt"
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
else:
    print("Error: Enter the correct GRB name. Also check the required files are present in the directory or not.\n\n\n")
lines = content.split("\n")
if len(lines) < 17:
    print(f"Content in the {grb_name}.txt file is not in correct order/format. Check it")
line17 = lines[17].split(" ")
astrosat_time = round(float(line17[2]),1)
line0 = lines[0].split(" ")
utc_time = f'{line0[1]} {line0[2]}'
grbout1 = f'Trigger time: {astrosat_time} (UTC: {utc_time})'
grbout2 = f'Observation: {line0[5][0:30]}'
grbout3 = f'Orbit: {line0[6]}'
grbout4 = f'RA: {line0[3]}'
grbout5 = f'Dec: {line0[4]}'
line5 = lines[5].split(" ")
theta = round(float(line5[2]),2)
phi = round(float(line5[4]),2)
grbout6 = f'Theta: {theta}'
grbout7 = f'Phi: {phi}'
section1 = f"\n--- AstroSat Data ---\n{grbout1}\n{grbout2}\n{grbout3}\n{grbout4}\n{grbout5}\n{grbout6}\n{grbout7}"
#Writing the first line of the Mail - Detection status
detect = int(input('\nWhich instrument detected? [CZTI=1; Veto=2; Both=3] '))
czti_key = 0
veto_key = 0
if detect == 1:
    czti_key = 1
    outline1 = 'The GRB is detected in CZTI. Please find the attached spectrograms and T90 result.'
elif detect == 2:
    veto_key = 1
    outline1 = 'The GRB is detected in Veto. Please find the attached spectrograms and T90 result.'
elif detect == 3:
    t90val = int(input('\nWhich instrument used for T90 calculation? [CZTI=1; Veto=2; Both=3] '))
    if t90val == 1:
        czti_key = 1
        veto_key = 2
        outline1 = 'The GRB is detected in CZTI and Veto. Please find the attached spectrograms and T90 result for CZTI.'
    elif t90val == 2:
        veto_key = 1
        czti_key = 2
        outline1 = 'The GRB is detected in CZTI and Veto. Please find the attached spectrograms and T90 result for Veto.'
    elif t90val == 3:
        czti_key = 1
        veto_key = 1
        outline1 = 'The GRB is detected in CZTI and Veto. Please find the attached spectrograms and T90 results for CZTI and Veto.'
    else:
        sys.exit("\nGive only above mentioned values. Try again")
else:
    sys.exit("\nGive only above mentioned values. Try again")
# Read and Scrape T90 files of veto and czti
folder_path = f"/home/npk/NPKCZTI/testarea/Astrosat-Detected/{grb_name}"
# czti_t90data,veto_t90data = "",""
if czti_key == 1:
    keyword1 = 'czt'
    for item in os.listdir(folder_path):
        if keyword1 in item and item.endswith('.txt'):
            with open(f'{folder_path}/{item}','r') as file:
                content1 = file.read()
            break
    else:
        print(f"Error: Check the required CZTI T90 file are present in the GRB directory or not.\n")
    lines = content1.split("\n")
    num_to_letter = {'0':'A','1':'B','2':'C','3':'D'}
    czti_quad_string = str(lines[0])
    czti_quad_numbers = len(re.findall(r'\d+',str(lines[0])))
    for num, letter in num_to_letter.items():
        czti_quad_string = czti_quad_string.replace(num, letter)
    time_to_value = {'1.0e+00':'1.0','1.0e+01':'10.0','1.0e-01':'0.1','2.0e-01':'0.2','2.0e+00':'2.0','5.0e+00':'5.0'}
    czti_binsize_string = str(lines[4])
    for time, value in time_to_value.items():
        czti_binsize_string = czti_binsize_string.replace(time, value)   
    czti_peakratetime_string = str(lines[5])
    peakratetime = re.findall(r'[\d]+\.[\d]+',str(czti_peakratetime_string))
    peaktime = float(peakratetime[0])
    czti_peaktimeAST = convertAStoAll(peaktime)
    bgrateline = str(lines[6])
    bgelements = bgrateline.split(" ")
    bgelem1 = int(round(float(bgelements[3]),0))
    bgelem2 = re.findall(r'[0-9]+\.[0-9]+',bgelements[4])
    bgelem2 = int(round(float(bgelem2[0]),0))
    bgelem3 = re.findall(r'[0-9]+\.[0-9]+',bgelements[5])
    bgelem3 = int(round(float(bgelem3[0]),0))
    czti_bgrate_string = f'Background Rate: {bgelem1} (+{bgelem2}, -{bgelem3}) counts/s'
    peakrateline = str(lines[7])
    peakelements = peakrateline.split(" ")
    peakelem1 = int(round(float(peakelements[5]),0))
    peakelem2 = re.findall(r'[0-9]+\.[0-9]+',peakelements[6])
    peakelem2 = int(round(float(peakelem2[0]),0))
    peakelem3 = re.findall(r'[0-9]+\.[0-9]+',peakelements[7])
    peakelem3 = int(round(float(peakelem3[0]),0))
    czti_peakrate_string = f'Peak Rate above Background: {peakelem1} (+{peakelem2}, -{peakelem3}) counts/s'
    totalline = str(lines[8])
    totalelements = totalline.split(" ")
    totalelements[4] = totalelements[4] + ','
    totalelements = ''.join(map(lambda x: ' ' + x, totalelements))
    czti_totalcount_string = totalelements[1:]
    t90line = str(lines[9])
    t90elements = t90line.split(" ")
    if float(t90elements[2]) > 30.0:
        t90value = int(round(float(t90elements[2]),0))
    else:
        t90value = round(float(t90elements[2]),2)
    t90elem1 = re.findall(r'[0-9]+\.[0-9]+',t90elements[3])
    if float(t90elem1[0]) < 1.0:
        t90elem1 = round(float(t90elem1[0]),2)
    else:
        t90elem1 = int(round(float(t90elem1[0]),0))
    t90elem2 = re.findall(r'[0-9]+\.[0-9]+',t90elements[4])
    if float(t90elem2[0]) < 1.0:
        t90elem2 = round(float(t90elem2[0]),2)
    else:
        t90elem2 = int(round(float(t90elem2[0]),0))
    czti_t90_string = f'T90: {t90value} (+{t90elem1}, -{t90elem2}) s'
    czti_t90data = f"\n--- Parameters of the GRB (from CZTI) ---\n{czti_quad_string}\n{czti_binsize_string}\n{czti_peakratetime_string}\n{czti_bgrate_string}\n{czti_peakrate_string}\n{czti_totalcount_string}\n{czti_t90_string}"
    czti_t90value = t90value
else:
    print(f"There is no CZTI T90 analysis for this GRB.\n")   
if veto_key == 1:
    keyword2 = 'veto'
    for item in os.listdir(folder_path):
        if keyword2 in item and item.endswith('.txt'):
            with open(f'{folder_path}/{item}','r') as file:
                content2 = file.read()
            break
    else:
        print(f"Error: Check the required Veto T90 file are present in the GRB directory or not.\n")    
    lines = content2.split("\n")
    num_to_letter = {'0':'A','1':'B','2':'C','3':'D'}
    veto_quad_string = str(lines[0])
    veto_quad_numbers = len(re.findall(r'\d+',str(lines[0])))
    for num, letter in num_to_letter.items():
        veto_quad_string = veto_quad_string.replace(num, letter)
    time_to_value = {'1.0e+00':'1.0','1.0e+01':'10.0','1.0e-01':'0.1','2.0e-01':'0.2','2.0e+00':'2.0','5.0e+00':'5.0'}
    veto_binsize_string = str(lines[4])
    for time, value in time_to_value.items():
        veto_binsize_string = veto_binsize_string.replace(time, value)   
    veto_peakratetime_string = str(lines[5])
    peakratetime = re.findall(r'[\d]+\.[\d]+',str(veto_peakratetime_string))
    peaktime = float(peakratetime[0])
    veto_peaktimeAST = convertAStoAll(peaktime)
    bgrateline = str(lines[6])
    bgelements = bgrateline.split(" ")
    bgelem1 = int(round(float(bgelements[3]),0))
    bgelem2 = re.findall(r'[0-9]+\.[0-9]+',bgelements[4])
    bgelem2 = int(round(float(bgelem2[0]),0))
    bgelem3 = re.findall(r'[0-9]+\.[0-9]+',bgelements[5])
    bgelem3 = int(round(float(bgelem3[0]),0))
    veto_bgrate_string = f'Background Rate: {bgelem1} (+{bgelem2}, -{bgelem3}) counts/s'
    peakrateline = str(lines[7])
    peakelements = peakrateline.split(" ")
    peakelem1 = int(round(float(peakelements[5]),0))
    peakelem2 = re.findall(r'[0-9]+\.[0-9]+',peakelements[6])
    peakelem2 = int(round(float(peakelem2[0]),0))
    peakelem3 = re.findall(r'[0-9]+\.[0-9]+',peakelements[7])
    peakelem3 = int(round(float(peakelem3[0]),0))
    veto_peakrate_string = f'Peak Rate above Background: {peakelem1} (+{peakelem2}, -{peakelem3}) counts/s'
    totalline = str(lines[8])
    totalelements = totalline.split(" ")
    totalelements[4] = totalelements[4] + ','
    totalelements = ''.join(map(lambda x: ' ' + x, totalelements))
    veto_totalcount_string = totalelements[1:]
    t90line = str(lines[9])
    t90elements = t90line.split(" ")
    if float(t90elements[2]) > 30.0:
        t90value = int(round(float(t90elements[2]),0))
    else:
        t90value = round(float(t90elements[2]),2)
    t90elem1 = re.findall(r'[0-9]+\.[0-9]+',t90elements[3])
    if float(t90elem1[0]) < 1.0:
        t90elem1 = round(float(t90elem1[0]),2)
    else:
        t90elem1 = int(round(float(t90elem1[0]),0))
    t90elem2 = re.findall(r'[0-9]+\.[0-9]+',t90elements[4])
    if float(t90elem2[0]) < 1.0:
        t90elem2 = round(float(t90elem2[0]),2)
    else:
        t90elem2 = int(round(float(t90elem2[0]),0))
    veto_t90_string = f'T90: {t90value} (+{t90elem1}, -{t90elem2}) s'
    veto_t90data = f"\n--- Parameters of the GRB (from Veto) ---\n{veto_quad_string}\n{veto_binsize_string}\n{veto_peakratetime_string}\n{veto_bgrate_string}\n{veto_peakrate_string}\n{veto_totalcount_string}\n{veto_t90_string}"
    veto_t90value = t90value
else:
    print(f"There is no Veto T90 analysis for this GRB.\n")  
#Writing GCN Draft
gcn_section1 = f"\n--- GCN Draft ---\n{grb_name}\nGRB {grb_name[3:]}: AstroSat CZTI detection."
gcn_section2 = f"\nP K. Navaneeth (IUCAA), G. Waratkar (IITB), A. Vibhute (IUCAA), V. Bhalerao (IITB), D. Bhattacharya (Ashoka University/IUCAA), A. R. Rao (IUCAA/TIFR), and S. Vadawale (PRL) report on behalf of the AstroSat CZTI collaboration:"
grb_type = input("\nEnter the characteristics of the GRB [short/long/bright/faint or provide no value]: ")
if grb_type == '':
    gcn_section3 = f"\nAnalysis of AstroSat CZTI data with the CIFT framework (Sharma et al., 2021, JApA, 42, 73) showed the detection of a GRB {grb_name[3:]}"
else:
    gcn_section3 = f"\nAnalysis of AstroSat CZTI data with the CIFT framework (Sharma et al., 2021, JApA, 42, 73) showed the detection of a {grb_type} GRB {grb_name[3:]}"
gcn_count = int(input('\nHow many instrument reported this GRB: '))
if gcn_count == 0:
    gcn_section3 += ""
else:
    gcn_section3 += " which was also detected by "
gcn_ref = []
for i in range(gcn_count):
    instrument, auther, circular = input('\nEnter the GCN detials for the GRB [instrument, auther, circular_number]: ').split(',')
    instrument, auther, circular = instrument.lstrip(), auther.lstrip(), circular.lstrip()
    gcn_refstring = f"{instrument} ({auther} et al., GCN {circular})"
    gcn_ref.append(gcn_refstring)
if len(gcn_ref) == 1:
    gcn_section3 += gcn_ref[0]
else:
    for i in range(len(gcn_ref)):
        if i == len(gcn_ref) - 1:
            gcn_section3 += "and " + gcn_ref[i]
        else:
            gcn_section3 += gcn_ref[i] + ", "
gcn_section3 += "."
#Writing CZTI & Veto Paragraph
multiple_peak = str(input("\nIs there multiple peak in the lightcurve? [yes/no]: "))
if multiple_peak == 'yes':
    peak_info = f"The light curve showed multiple peaks of emission with the strongest peak at"
elif multiple_peak == 'no':
    peak_info = f"The light curve peaks at"
else:
    print("Error: Enter the correct input.")
compton_data = int(input("\nEnter the compton counts [0 = no compton analysis]: "))
if compton_data != 0:
    compton_info = f"In the preliminary analysis, we find {compton_data} Compton events associated with this event."
else:
    compton_info = ""
#Writing CZTI Paragraph
if czti_quad_numbers == 2:
    czti_quad_strip = f"combined data of two quadrants (out of four)"
elif czti_quad_numbers == 3:
    czti_quad_strip = f"combined data of three quadrants (out of four)"
elif czti_quad_numbers == 4:
    czti_quad_strip = f"combined data of all quadrants"
else:
    print("Error: Check the CZTI T90 results #QUAD_INFO.")
if czti_key == 1:
    czti_para = f"\nThe source was clearly detected in the 20-200 keV energy range. {peak_info} {czti_peaktimeAST[:-1]} UTC. The measured peak count rate associated with the burst is {czti_peakrate_string[28:]} above the background in the {czti_quad_strip}, with a total of {czti_totalcount_string[15:]}. The local mean background count rate was {czti_bgrate_string[17:]}. Using cumulative rates, we measure a T90 of {czti_t90_string[5:]}. {compton_info}"
elif czti_key ==2:
    czti_para = f"\nThe source was also clearly detected in the 20-200 keV energy range."
else:
    print(f"There is no CZTI T90 analysis for this GRB.\n")
#Writing Veto Paragraph
if veto_quad_numbers == 2:
    veto_quad_strip = f"combined data of two quadrants (out of four)"
elif veto_quad_numbers == 3:
    veto_quad_strip = f"combined data of three quadrants (out of four)"
elif veto_quad_numbers == 4:
    veto_quad_strip = f"combined data of all quadrants"
else:
    print("Error: Check the CZTI T90 results #QUAD_INFO.")
if veto_key == 1:
    veto_para = f"\nThe source was also clearly detected in the CsI anticoincidence (Veto) detector in the 100-500 keV energy range. {peak_info} {veto_peaktimeAST[:-1]} UTC. The measured peak count rate associated with the burst is {veto_peakrate_string[28:]} above the background in the {veto_quad_strip}, with a total of {veto_totalcount_string[15:]}. The local mean background count rate was {veto_bgrate_string[17:]}. We measure a T90 of {veto_t90_string[5:]} from the cumulative Veto light curve."
elif veto_key ==2:
    veto_para = f"\nThe source was also clearly detected in the CsI anticoincidence (Veto) detector in the 100-500 keV energy range."
else:
    print(f"There is no CZTI T90 analysis for this GRB.\n")
print("\n------------------------------------------------------------------------------------------")
gcn_section4 = czti_para + "\n" + veto_para
gcn_section5 = "\nCZTI is built by a TIFR-led consortium of institutes across India, including VSSC, URSC, IUCAA, SAC, and PRL. The Indian Space Research Organisation funded, managed, and facilitated the project. CZTI GRB detections are reported regularly on the payload site at: http://astrosat.iucaa.in/czti/?q=grb"
grb_detection_mail = outline1 + "\n" + section1 + "\n" + czti_t90data + "\n" + veto_t90data + "\n" + gcn_section1 + "\n" + gcn_section2 + "\n" + gcn_section3 + "\n" + gcn_section4 + "\n" + gcn_section5
save_path = f"/home/npk/NPKCZTI/testarea/Astrosat-Detected/{grb_name}/{grb_name}_DetectionMail.txt"
with open(save_path, "w") as file:
    file.write(grb_detection_mail)
print(f"*** {grb_name}_DetectionMail.txt is created in the GRB folder.")
out = input("\nDo you want to print the Detection Mail [yes/no]: ")
if out == 'yes':
    print("------------------------------------------------------------------------------------------")
    print(grb_detection_mail)
print("------------------------------------------------------------------------------------------")
# print(grb_detection_mail)
# print(outline1)
# print(section1)
# print(czti_t90data)
# print(veto_t90data)
# print(gcn_section1)
# print(gcn_section2)
# print(gcn_section3)
# print(czti_para)
# print(veto_para)