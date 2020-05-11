export interface KeyTerm {
    term: string;
    popularity: number;
    sentiment: 0 | 1;
}

export function updateKeyTerms(tableEl: Element, keyTerms: ReadonlyArray<KeyTerm>) {
    const termTableRowTmpl = <HTMLTemplateElement | undefined>document.getElementById("x-term-table-row");
    if (!termTableRowTmpl) {
        throw new Error("no template defined for #x-term-table-row");
    }
    const tableBodyEl = tableEl.querySelector("tbody");
    if (!tableBodyEl) {
        throw new Error("table contained no tbody element");
    }
    
    // Add/remove any rows as needed
    let existingRows = tableBodyEl.querySelectorAll("tr");
    for (let i = existingRows.length; i < keyTerms.length; i++) {
        tableBodyEl.append(termTableRowTmpl.content.cloneNode(true));
    }
    for (let i = keyTerms.length; i < existingRows.length; i++) {
        existingRows[i].remove()
    }
    existingRows = tableBodyEl.querySelectorAll("tr");

    // Set content for each row
    for (let i = 0; i < existingRows.length; i++) {
        const termEl = existingRows[i].querySelector(".term");
        if (!termEl) {
            throw new Error("table row contained no .term element")
        }
        const popularityEl = existingRows[i].querySelector(".popularity");
        if (!popularityEl) {
            throw new Error("table row contained no .popularity element")
        }
        const sentimentEl = existingRows[i].querySelector(".sentiment");
        if (!sentimentEl) {
            throw new Error("table row contained no .sentiment element")
        }
        
        termEl.textContent = keyTerms[i].term
        popularityEl.textContent = keyTerms[i].popularity.toFixed(3).toString()
        if (keyTerms[i].sentiment) {
            sentimentEl.textContent = "Positive";
            sentimentEl.classList.remove("sentiment-negative")
            sentimentEl.classList.add("sentiment-positive")
        } else {
            sentimentEl.textContent = "Negative";
            sentimentEl.classList.remove("sentiment-positive")
            sentimentEl.classList.add("sentiment-negative")
        }
    }
}

export function updateKeyTermsAll(keyTermsRec: Record<string, ReadonlyArray<KeyTerm>>) {
    for (const id in keyTermsRec) {
        const keyTermsTableEl = document.querySelector(`.key-terms[data-candidate-id="${id}"] .key-terms-table`);
        if (!keyTermsTableEl) {
            throw new Error(`no .key-terms-table element found for candidate ${id}`);
        }
        updateKeyTerms(keyTermsTableEl, keyTermsRec[id]);
    }
}
