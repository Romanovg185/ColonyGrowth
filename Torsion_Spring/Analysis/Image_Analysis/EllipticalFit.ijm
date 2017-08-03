run("Duplicate...", "title=Ellipse");
makeRectangle(750, 130, 1700, 1075);
run("Crop");
run("8-bit");
setThreshold(86, 255);
setOption("BlackBackground", false);
run("Convert to Mask");
run("Analyze Particles...", "  show=Overlay display clear");
run("To ROI Manager");
roiManager("Select", 0);
roiManager("Delete");
selectWindow("Ellipse");
for(i = 0; i < roiManager("Count"); i++){
	roiManager("Select", i);
	setForegroundColor(255, 255, 255);
	run("Fill", "slice");
}
selectWindow("Results");
run("Close");
roiManager("Delete");
roiManager("Deselect");
roiManager("Delete");
selectWindow("ROI Manager");
run("Close");
//Filled colony is now made
run("Invert");
run("Create Selection");
run("Fit Ellipse");

run("ROI Manager...");
roiManager("Add");
run("Select All");
roiManager("Add");
roiManager("XOR");
roiManager("Add");
/*ROI Overview:
0. Elliptical fit of particle
1. Whole screen
2. All but the eliptical fit
*/

//Get area of colony outside ellipse
run("Analyze Particles...", "clear");
var i = 0;
var blackOutside = 0
while(i < nResults){
	data = getResult("Area", i);
	blackOutside += data;
	i++;
}

//Get area of colony inside ellipse
roiManager("Select", 0);
run("Analyze Particles...", "clear");
blackInside = getResult("Area", 0);

//Invert values and make whitespace into data
roiManager("Select", 1);
run("Invert");

//Get area of whitespace within ellipse
roiManager("Select", 0);
run("Analyze Particles...", "clear");
i = 0;
whiteInside = 0;
while(i < nResults){
	whiteInside += getResult("Area", i);
	i++;
}
//Get area of whitespace outside ellipse
roiManager("Select", 2);
run("Analyze Particles...", "show=Overlay display clear");
whiteOutside = getResult("Area", 0);

selectWindow("Results");
run("Close");
selectWindow("ROI Manager");
run("Close");
selectWindow("Ellipse");
run("Close");

total = blackOutside + blackInside + whiteOutside + whiteInside;
tIn = whiteInside + blackInside;
tOut = whiteOutside + blackOutside;
tBlack = blackInside + blackOutside;
tWhite = whiteInside + whiteOutside;
E00 = tIn*tBlack/total;
E10 = tIn*tWhite/total;
E01 = tOut*tBlack/total;
E11 = tOut*tWhite/total;

chisquared = 0;
chisquared += (E00 - blackInside)*(E00 - blackInside)/E00;
chisquared += (E10 - whiteInside)*(E10 - whiteInside)/E10;
chisquared += (E01 - blackOutside)*(E01 - blackOutside)/E01;
chisquared += (E11 - whiteOutside)*(E11 - whiteOutside)/E11; 

print("Null hypothesis: There is no correlation between laying in the ellipse and color");
print("Probability of true positive: " + blackInside/total);
print("Probability of false positive: " + whiteInside/total);
print("Probability of false negative: " + blackOutside/total);
print("Probability of true negative: " + whiteOutside/total);
print("The chi-squared value: " + chisquared/total)