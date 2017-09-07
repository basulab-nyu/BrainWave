(* ::Package:: *)

Print["histograms"];
dir=StringJoin[Directory[],"/../"];
currentDataset = Import[StringJoin[dir,"currentDataset.txt"]];
rawDataDirectory=StringJoin[dir,"datasets/",currentDataset,"/"];
outputDirectory=StringJoin[dir,"analyzedDatasets/",currentDataset,"/"];


files=FileNames["*",StringJoin[outputDirectory,"exportingN/"]];
files=Select[files,First@Characters@Last[StringSplit[#,"/"]]!="."&&
Last@Characters@Last[StringSplit[#,"/"]]!="p"&];
settings=<||>;
Map[(Module[{temp},
temp=StringSplit[#[[1]],":"];
settings[temp[[1]]]=temp[[2]];])&,
Import[StringJoin[outputDirectory,"mathematicaConfig.txt"],"Data"]];


getPositiveSigs[file_]:=
Block[{vals},
vals=ToExpression/@StringSplit[#,","]&/@StringSplit[
Import[StringJoin[file]],"\n"];
(vals)/.-1->0

];

getNegativeSigs[file_]:=
Block[{vals},
vals=ToExpression/@StringSplit[#,","]&/@StringSplit[
Import[StringJoin[file]],"\n"];
-1*((vals)/.+1->0)

];

makePositiveHistogram[directory_]:=Block[{vals},
vals=Transpose@getPositiveSigs[directory];
BarChart[N@(Total/@vals)/Length@vals[[1]],ChartLabels->
Flatten[{(Table[x->x+ToExpression[settings["group_size"]]-1,
{x,1,ToExpression@settings["number_of_frames_after"],ToExpression[settings["group_size"]]}])}],

PlotLabel->
Style[StringJoin[StringDrop[StringSplit[directory,"/"][[-1]],-4],
" Percent Neurons Significantly Increasing Over ",settings["number_of_frames_after"]," Frames After Stimulus"],30],

PlotRange->{Automatic,{-0.05,1}}]
];

makeNegativeHistogram[directory_]:=Block[{vals},
vals=Transpose@getNegativeSigs[directory];
BarChart[N@(Total/@vals)/Length@vals[[1]],ChartLabels->
Flatten[{(Table[x->x+ToExpression[settings["group_size"]]-1,
{x,1,ToExpression@settings["number_of_frames_after"],ToExpression[settings["group_size"]]}])}],

PlotLabel->
Style[StringJoin[StringDrop[StringSplit[directory,"/"][[-1]],-4],
" Percent Neurons Significantly Decreasing Over ",settings["number_of_frames_after"]," Frames After Stimulus"],30],

PlotRange->{Automatic,{-0.05,1}}]
];

Export[StringJoin[outputDirectory,"histograms/",StringSplit[StringDrop[#,-4],"/"][[-1]],"Negative.pdf"],
makeNegativeHistogram[#],ImageSize->1200]&/@files;
Export[StringJoin[outputDirectory,"histograms/",StringSplit[StringDrop[#,-4],"/"][[-1]],"Positive.pdf"],
makePositiveHistogram[#],ImageSize->1200]&/@files;




