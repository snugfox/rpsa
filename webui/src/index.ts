import { updateKeyTermsAll, KeyTerm } from "./term-table";
import { addCandidates, CandidateRecord } from "./candidates";

const sentimentChart = document.getElementById("sentiment-chart")!;
const dummyData = <Plotly.Data>{
    x:["2020-10-04", "2021-11-04", "2023-12-04"],
    y: new Float32Array([90, 40, 60]),
    type: "scatter",
};
const layout = <Partial<Plotly.Layout>>{
    showlegend: true,
    legend: {
        title: {
            text: "Foo",
        },
    },
    margin: {
        l: 0,
        r: 0,
        t: 0,
        b: 0,
    },
    xaxis: {
        automargin: true,
    },
    yaxis: {
        automargin: true,
    },
};
const config = <Partial<Plotly.Config>>{
    responsive: true,
};
Plotly.newPlot(sentimentChart, [dummyData], layout, config);

const candidates: CandidateRecord[] = [
    {
        name: "Donald Trump",
        id: "0",
    },
    {
        name: "Joe Biden",
        id: "1",
    },
];
const keyTermsRec: Record<string, KeyTerm[]> = {
    "0": [
        {
            term: "test",
            popularity: 0.03,
            sentiment: 1,
        },
        {
            term: "foo",
            popularity: 0.25,
            sentiment: 0,
        },
    ],
    "1": [
        {
            term: "wat",
            popularity: 0.02,
            sentiment: 0,
        }, {
            term: "doo",
            popularity: 0.4,
            sentiment: 1,
        }
    ]
};
addCandidates(candidates);
updateKeyTermsAll(keyTermsRec);
