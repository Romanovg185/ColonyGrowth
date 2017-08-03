run("Duplicate...", "title=WhiteSpace");
run("8-bit");
setThreshold(245, 255);
setOption("BlackBackground", false);
run("Convert to Mask");
run("Analyze Particles...", "exclude clear");

data = 1;
var i = 0;
var sum = 0
while(i < nResults){
	data = getResult("Area", i);
	sum += data;
	i++;
}
close("WhiteSpace");

run("Duplicate...", "title=ParticleSpace");
run("8-bit");
setThreshold(245, 255);
setOption("BlackBackground", false);
run("Convert to Mask");
run("Invert");
run("Create Selection");
run("Measure");

data = getResult("Area", 0);

selectWindow("Results");
run("Close");
close("ParticleSpace");
print(data/(data+sum));
close();
