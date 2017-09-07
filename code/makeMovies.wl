(* ::Package:: *)

Print["makeMovies"];
dir=StringJoin[Directory[],"/../"];
currentDataset = Import[StringJoin[dir,"currentDataset.txt"]];
rawDataDirectory=StringJoin[dir,"datasets/",currentDataset,"/"];
outputDirectory=StringJoin[dir,"analyzedDatasets/",currentDataset,"/"];

files=FileNames["*",StringJoin[outputDirectory,"exportingN/"]];
files=Select[files,First@Characters@Last[StringSplit[#,"/"]]!="."&&
Last@Characters@Last[StringSplit[#,"/"]]!="p"&];
rawNeurons=Import[StringJoin[rawDataDirectory,"centers.txt"]];
neurons=ToExpression/@StringSplit[#,"\t"]&/@StringSplit[rawNeurons,"\n"];
getSigs[file_]:=ToExpression/@StringSplit[#,","]&/@StringSplit[
Import[StringJoin[file]],"\n"];
makeFrame[frames_]:=Graphics[{EdgeForm[Thin],
Table[
{Switch[frames[[x]],1,Red,-1,Blue,0,White],
Disk[neurons[[x]],4]}
,{x,1,Length[neurons]}]
}];
makeMovie[file_]:=Module[{data},
data=Transpose[getSigs[file]];
makeFrame/@data
];
exportMovie[file_]:=Module[{frames},
frames=makeMovie[file];
Export[StringJoin[outputDirectory,"movies/",StringDrop[StringSplit[file,"/"][[-1]],-4],".gif"],frames,"DisplayDurations"->.5]
];

exportMovie/@files;



