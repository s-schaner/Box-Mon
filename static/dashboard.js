(function () {
    const expandClass = "open";

    function toggleCard(card) {
        const isOpen = card.classList.contains(expandClass);
        const details = card.querySelector(".node-details");
        const header = card.querySelector(".node-header");

        if (!details || !header) {
            return;
        }

        if (isOpen) {
            card.classList.remove(expandClass);
            details.style.maxHeight = "0px";
            details.setAttribute("aria-hidden", "true");
            header.setAttribute("aria-expanded", "false");
        } else {
            const currentOpen = card.parentElement?.querySelectorAll(`.${expandClass}`) || [];
            currentOpen.forEach((openCard) => {
                if (openCard === card) {
                    return;
                }
                openCard.classList.remove(expandClass);
                const openDetails = openCard.querySelector(".node-details");
                const openHeader = openCard.querySelector(".node-header");
                if (openDetails && openHeader) {
                    openDetails.style.maxHeight = "0px";
                    openDetails.setAttribute("aria-hidden", "true");
                    openHeader.setAttribute("aria-expanded", "false");
                }
            });

            card.classList.add(expandClass);
            details.style.maxHeight = `${details.scrollHeight}px`;
            details.setAttribute("aria-hidden", "false");
            header.setAttribute("aria-expanded", "true");
        }
    }

    function initCards() {
        const cards = document.querySelectorAll(".node-card");
        cards.forEach((card, index) => {
            const header = card.querySelector(".node-header");
            const details = card.querySelector(".node-details");
            if (!header || !details) {
                return;
            }

            details.style.maxHeight = "0px";

            header.addEventListener("click", () => toggleCard(card));
            header.addEventListener("keydown", (event) => {
                if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    toggleCard(card);
                }
            });

            if (index === 0) {
                setTimeout(() => toggleCard(card), 200);
            }
        });
    }

    function logDiagnostics() {
        if (!Array.isArray(window.NODE_PAYLOAD)) {
            return;
        }
        console.groupCollapsed("4G Node Pulse Mock Data");
        window.NODE_PAYLOAD.forEach((node) => {
            console.log(`${node.name} (${node.ip}) → ${node.overall_status}`);
        });
        console.log(
            "Use /api/nodes and /api/node/<name> for raw JSON. Update NODES in app.py to simulate new hardware."
        );
        console.groupEnd();
    }

    document.addEventListener("DOMContentLoaded", () => {
        initCards();
        logDiagnostics();
    });
})();
