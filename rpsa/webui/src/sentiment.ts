import { PlotData } from "plotly.js";

export interface Sentiment {
    names: string[];
    times: string[];
    sentiment: number[][]; // number[id][sentiment]
}

export function updateSentiment(sentiment: Sentiment) {
    if (sentiment.times.length > 0) {
        const sentimentChart = document.getElementById("sentiment-chart")!;
        const plotData = sentiment.sentiment.map((_, i) => {
            return <Partial<PlotData>>{
                name: sentiment.names[i],
                x: sentiment.times,
                y: sentiment.sentiment[i],
                type: "scatter"
            }
        });
        const layout = <Partial<Plotly.Layout>>{
            showlegend: true,
            legend: {
                title: {
                    text: "Candidates",
                },
                x: 0.025,
                y: 0.025,
                bgcolor: "rgba(255, 255, 255, 0.5)",
                bordercolor: "black",
                borderwidth: 1,
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
                range: [-1.0, 1.0]
            },
        };
        const config = <Partial<Plotly.Config>>{
            responsive: true,
        };
        Plotly.react(sentimentChart, plotData, layout, config);
    }
}
