import { updateKeyTermsAll, KeyTerm } from "./term-table";
import { addCandidates, CandidateRecord } from "./candidates";
import { Sentiment, updateSentiment } from "./sentiment";

const urlParams = new URLSearchParams(window.location.search);
const apiOrigin = urlParams.get("api_origin") || `${window.location.origin}/`;


function keyTermsHandler() {
    fetch(`${apiOrigin}api/terms`).then((res) => {
        return res.json()
    }).then((keyTermsRec: Record<string, KeyTerm[]>) => {
        updateKeyTermsAll(keyTermsRec);
    });
}


function sentimentHandler() {
    fetch(`${apiOrigin}api/sentiment`).then((res) => {
        return res.json()
    }).then((sentiment: Sentiment) => {
        updateSentiment(sentiment);
    });
}

fetch(`${apiOrigin}api/candidates`).then((res) => {
    return res.json();
}).then((candidates: CandidateRecord[]) => {
    addCandidates(candidates);
    keyTermsHandler();
    setInterval(keyTermsHandler, 60 * 1000);
    sentimentHandler();
    setInterval(sentimentHandler, 60 * 1000);
});

