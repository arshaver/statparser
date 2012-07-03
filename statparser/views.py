import csv
import datetime
from django.http import HttpResponse
from statparser.forms import UploadFileForm
from django.shortcuts import render

INTERVENTIONS = ["ABX","AMINO","ANTICOAG","CARBA","CODE","DIGOXIN","DRUGS","ELECTROLYT","INSULIN","LITHIUM","MISC","PAIN","PHENOBARB","PHENYTOIN","PRADAXA","SENTOUT","THEOPHYL","TPN","VALPROIC","VANCO","WARFARIN","OTHER"]
NEW_INTERVENTIONS = ["AMINOG", "ANTICOAG", "CARBA", "CODE", "DIGOXIN", "DRUGS", "ELECTROLYT", "FOLLOWUP", "INSULIN", "LITHIUM", "MONITOR", "PAIN", "PHENOBARB", "PRADAXA", "REGIONAL", "RIVAROXABA", "SENTOUT", "THEOPHYL", "TPN", "VALPROIC", "VANCO", "WARFARIN", "WEIGHT"]

def parse_stats(file):
	lines = file.readlines()
	data = {}
	
	for line in lines:
		if "DATE" in line:
			date_string = line.split(" ")[1]
			date_list = date_string.split("/")
			month = int(date_list[0])
			day = int(date_list[1])
			year = int("20"+date_list[2])
			date = datetime.date(month=month, day=day, year=year)
			data[date] = {}
		if any(intervention in line for intervention in INTERVENTIONS):
			split_line = line.split(" ")
			split_line = filter(None,split_line)

			intervention = split_line[0]
			count = split_line[1]
			data[date][intervention] = int(count)

	#if an intervention from INTERVENTIONS wasn't done on that day, add an entry to say so
	for intervention in INTERVENTIONS:
		for date in data:
			try:
				data[date][intervention]
			except KeyError:
				data[date][intervention] = 0
	
	return data
	
def main(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			file_name = request.FILES['file'].name.split(".")[0]
			data = parse_stats(request.FILES['file'])
			
			response = HttpResponse(mimetype='text/csv')
			response['Content-Disposition'] = 'attachment; filename=%s parsed.csv' %file_name

			writer = csv.writer(response)
			
			dates = data.keys()
			dates.sort()
			writer.writerow([" "]+dates)

			for intervention in INTERVENTIONS:
				row = []
				row.append(intervention)
				for date in dates:
					row.append(data[date][intervention])
				writer.writerow(row)
			return response
	else:
		form = UploadFileForm()
	return render(request, 'upload.html', {'form': form})