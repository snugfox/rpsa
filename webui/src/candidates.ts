export interface CandidateRecord {
    name: string;
    id: string;
}

export function addCandidates(candidates: ReadonlyArray<CandidateRecord>) {
    const keyTermsCardTmpl = document.getElementById("x-key-terms-card");
    if (!(keyTermsCardTmpl instanceof HTMLTemplateElement)) {
        throw new Error("no template defined for #x-key-terms-card");
    }
    const mainEl = document.querySelector("main");
    if (!(mainEl instanceof HTMLElement)) {
        throw new Error("no main element");
    }

    for (const candidate of candidates) {
        const keyTermsCard = document.importNode(keyTermsCardTmpl.content, true);
        const cardDiv = keyTermsCard.querySelector(".card");
        if (!(cardDiv instanceof HTMLDivElement)) {
            throw new Error("template contains no div.card element");
        }
        const cardHeading = keyTermsCard.querySelector(".card__heading");
        if (!(cardHeading instanceof HTMLHeadingElement)) {
            throw new Error("template contains no heading element");
        }

        cardDiv.dataset.candidateId = candidate.id;
        cardHeading.textContent = candidate.name;
        mainEl.appendChild(keyTermsCard);
    }
}