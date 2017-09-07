(* ::Package:: *)

Print["proportionOfTrialsSpiking"];
dir=StringJoin[Directory[],"/../"];
currentDataset = Import[StringJoin[dir,"currentDataset.txt"]];
rawDataDirectory=StringJoin[dir,"datasets/",currentDataset,"/"];
outputDirectory=StringJoin[dir,"analyzedDatasets/",currentDataset,"/"];
files=FileNames["*",StringJoin[outputDirectory,"proportion_of_trials_spiking/"]];
files=Select[files,First@Characters@Last[StringSplit[#,"/"]]!="."&&
Last@Characters@Last[StringSplit[#,"/"]]!="p"&];

rawNeurons=Import[StringJoin[rawDataDirectory,"centers.txt"]];
neurons=ToExpression/@StringSplit[#,"\t"]&/@StringSplit[rawNeurons,"\n"];
getSigs[file_]:=ToExpression/@StringSplit[#,","]&/@StringSplit[Import[StringJoin[file]],"\n"];
makeFrame[frames_]:=Graphics[{
Table[{
EdgeForm[Thin],Disk[neurons[[n]],6],EdgeForm[None],
Table[{
Switch[frames[[n]][[x]],1,Red,-1,Blue,0,White]
,
Disk[neurons[[n]],6,{0+(x-1) 2Pi/Length[frames[[n]]],(x)2Pi/Length[frames[[n]]]}]},{x,1,Length[frames[[n]]]}]},
{n,1,Length@neurons}]

}];

makeIt[file_]:=Module[{data,NewData,safeData},
data=getSigs[file];
makeFrame[data]

];
Export[StringJoin[outputDirectory,"/proportion_of_trials_spiking_figs/",StringSplit[StringDrop[#,-4],"/"][[-1]],".pdf"],
makeIt[#]]&/@files;
