// ============================================================
// RAZORPAY AI RISK MANAGER
// Frontend Risk Dashboard
// Data-Driven Analytics
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {


        // ========================================================
        // ELEMENTS
        // ========================================================

        const form =
            document.getElementById(
                "riskForm"
            );

        const analyzeButton =
            document.getElementById(
                "analyzeButton"
            );

        const buttonText =
            document.getElementById(
                "buttonText"
            );


        const emptyState =
            document.getElementById(
                "emptyState"
            );

        const resultContent =
            document.getElementById(
                "resultContent"
            );


        const scoreRing =
            document.getElementById(
                "scoreRing"
            );

        const riskScore =
            document.getElementById(
                "riskScore"
            );

        const riskLevel =
            document.getElementById(
                "riskLevel"
            );


        const recommendation =
            document.getElementById(
                "recommendation"
            );

        const riskDescription =
            document.getElementById(
                "riskDescription"
            );


        const fraudProbability =
            document.getElementById(
                "fraudProbability"
            );

        const fraudProgress =
            document.getElementById(
                "fraudProgress"
            );


        const decisionCard =
            document.getElementById(
                "decisionCard"
            );

        const decisionIcon =
            document.getElementById(
                "decisionIcon"
            );

        const decisionText =
            document.getElementById(
                "decisionText"
            );


        const factorList =
            document.getElementById(
                "factorList"
            );

        const factorCount =
            document.getElementById(
                "factorCount"
            );


        const analysisTime =
            document.getElementById(
                "analysisTime"
            );


        const resultTransactionId =
            document.getElementById(
                "resultTransactionId"
            );

        const resultAmount =
            document.getElementById(
                "resultAmount"
            );

        const resultPayment =
            document.getElementById(
                "resultPayment"
            );

        const resultDevice =
            document.getElementById(
                "resultDevice"
            );


        const currentDate =
            document.getElementById(
                "currentDate"
            );


        const toast =
            document.getElementById(
                "toast"
            );

        const toastMessage =
            document.getElementById(
                "toastMessage"
            );


        // ========================================================
        // DATA-DRIVEN KPI ELEMENTS
        // ========================================================

        const transactionsAnalyzed =
            document.getElementById(
                "transactionsAnalyzed"
            );

        const fraudDetected =
            document.getElementById(
                "fraudDetected"
            );

        const fraudCount =
            document.getElementById(
                "fraudCount"
            );

        const blockedValue =
            document.getElementById(
                "blockedValue"
            );

        const blockedTransactions =
            document.getElementById(
                "blockedTransactions"
            );

        const modelAccuracy =
            document.getElementById(
                "modelAccuracy"
            );

        const transactionStatus =
            document.getElementById(
                "transactionStatus"
            );

        const modelStatus =
            document.getElementById(
                "modelStatus"
            );


        // ========================================================
        // DONUT
        // ========================================================

        const donut =
            document.getElementById(
                "decisionDonut"
            );

        const donutTotal =
            document.getElementById(
                "donutTotal"
            );

        const approvePercentage =
            document.getElementById(
                "approvePercentage"
            );

        const reviewPercentage =
            document.getElementById(
                "reviewPercentage"
            );

        const blockPercentage =
            document.getElementById(
                "blockPercentage"
            );


        // ========================================================
        // MODEL METRICS
        // ========================================================

        const rocAuc =
            document.getElementById(
                "rocAuc"
            );

        const prAuc =
            document.getElementById(
                "prAuc"
            );

        const precisionMetric =
            document.getElementById(
                "precisionMetric"
            );

        const recallMetric =
            document.getElementById(
                "recallMetric"
            );

        const f1Metric =
            document.getElementById(
                "f1Metric"
            );


        // ========================================================
        // CHART
        // ========================================================

        const riskChartLine =
            document.getElementById(
                "riskChartLine"
            );

        const riskChartFill =
            document.getElementById(
                "riskChartFill"
            );

        const activityMode =
            document.getElementById(
                "activityMode"
            );


        // ========================================================
        // CURRENT DATA
        // ========================================================

        let dashboardData = null;


        // ========================================================
        // CURRENT DATE
        // ========================================================

        function updateDate() {

            if (!currentDate) {
                return;
            }

            const now =
                new Date();

            currentDate.textContent =
                now.toLocaleDateString(
                    "en-IN",
                    {
                        day:
                            "2-digit",

                        month:
                            "short",

                        year:
                            "numeric"
                    }
                );
        }


        updateDate();


        // ========================================================
        // TOAST
        // ========================================================

        function showToast(
            message,
            type = "success"
        ) {

            if (!toast) {
                return;
            }

            if (toastMessage) {

                toastMessage.textContent =
                    message;
            }

            toast.className =
                `toast ${type} show`;


            setTimeout(
                () => {

                    toast.classList.remove(
                        "show"
                    );

                },
                3000
            );
        }


        // ========================================================
        // LOADING STATE
        // ========================================================

        function setLoading(
            loading
        ) {

            if (!analyzeButton) {
                return;
            }


            if (loading) {

                analyzeButton.disabled =
                    true;


                if (buttonText) {

                    buttonText.innerHTML =
                        `<span class="button-spinner"></span> Analyzing...`;
                }

            } else {

                analyzeButton.disabled =
                    false;


                if (buttonText) {

                    buttonText.textContent =
                        "Analyze Transaction";
                }
            }
        }


        // ========================================================
        // GET INPUT VALUE
        // ========================================================

        function value(id) {

            const element =
                document.getElementById(
                    id
                );

            return element
                ? element.value
                : "";
        }


        // ========================================================
        // GET CHECKBOX VALUE
        // ========================================================

        function checked(id) {

            const element =
                document.getElementById(
                    id
                );

            return element
                ? element.checked
                : false;
        }


        // ========================================================
        // COLLECT TRANSACTION
        // ========================================================

        function collectTransaction() {

            return {

                transaction_id:
                    value(
                        "transactionId"
                    )
                    ||
                    `TXN_${Date.now()}`,

                amount:
                    Number(
                        value("amount")
                    ),

                location_match:
                    checked(
                        "locationMatch"
                    ),

                previous_fraud:
                    checked(
                        "previousFraud"
                    ),

                payment_method:
                    value(
                        "paymentMethod"
                    ),

                device_type:
                    value(
                        "deviceType"
                    ),

                transactions_last_1h:
                    Number(
                        value(
                            "transactions1h"
                        )
                    ),

                transactions_last_24h:
                    Number(
                        value(
                            "transactions24h"
                        )
                    ),

                transaction_hour:
                    Number(
                        value(
                            "transactionHour"
                        )
                    ),

                merchant_category:
                    value(
                        "merchantCategory"
                    ),

                account_age_days:
                    Number(
                        value(
                            "accountAge"
                        )
                    ),

                is_international:
                    checked(
                        "international"
                    )
            };
        }


        // ========================================================
        // CURRENCY FORMATTER
        // ========================================================

        function formatCurrency(
            amount
        ) {

            return new Intl.NumberFormat(
                "en-IN",
                {
                    style:
                        "currency",

                    currency:
                        "INR",

                    maximumFractionDigits:
                        2
                }
            ).format(
                Number(amount) || 0
            );
        }


        // ========================================================
        // COMPACT INR FORMAT
        // ========================================================

        function formatCompactINR(
            amount
        ) {

            const value =
                Number(amount) || 0;


            if (value >= 10000000) {

                return (
                    "₹" +
                    (
                        value /
                        10000000
                    ).toFixed(2) +
                    "Cr"
                );
            }


            if (value >= 100000) {

                return (
                    "₹" +
                    (
                        value /
                        100000
                    ).toFixed(2) +
                    "L"
                );
            }


            if (value >= 1000) {

                return (
                    "₹" +
                    (
                        value /
                        1000
                    ).toFixed(1) +
                    "K"
                );
            }


            return (
                "₹" +
                value.toFixed(0)
            );
        }


        // ========================================================
        // FORMAT NUMBER
        // ========================================================

        function formatNumber(
            value
        ) {

            return new Intl.NumberFormat(
                "en-IN"
            ).format(
                Number(value) || 0
            );
        }


        // ========================================================
        // DISPLAY RESULT PANEL
        // ========================================================

        function showResults() {

            if (emptyState) {

                emptyState.classList.add(
                    "hidden"
                );
            }


            if (resultContent) {

                resultContent.classList.remove(
                    "hidden"
                );
            }
        }


        // ========================================================
        // RISK SCORE
        // ========================================================

        function updateRiskScore(
            score,
            level
        ) {

            const numericScore =
                Math.min(
                    Math.max(
                        Number(score) || 0,
                        0
                    ),
                    100
                );


            if (riskScore) {

                riskScore.textContent =
                    numericScore.toFixed(
                        2
                    );
            }


            if (scoreRing) {

                scoreRing.style.setProperty(
                    "--risk-score",
                    `${numericScore}%`
                );


                scoreRing.style.background = `
                    conic-gradient(
                        var(--accent)
                        0deg
                        ${numericScore * 3.6}deg,

                        #edf0f5
                        ${numericScore * 3.6}deg
                        360deg
                    )
                `;


                scoreRing.setAttribute(
                    "data-risk",
                    level
                );
            }


            if (riskLevel) {

                riskLevel.textContent =
                    `${level} RISK`;

                riskLevel.className =
                    `risk-level ${level.toLowerCase()}`;
            }
        }


        // ========================================================
        // FRAUD PROBABILITY
        // ========================================================

        function updateFraudProbability(
            probability
        ) {

            let percentage =
                Number(probability) || 0;


            if (percentage <= 1) {

                percentage *= 100;
            }


            percentage =
                Math.min(
                    Math.max(
                        percentage,
                        0
                    ),
                    100
                );


            if (fraudProbability) {

                fraudProbability.textContent =
                    `${percentage.toFixed(2)}%`;
            }


            if (fraudProgress) {

                fraudProgress.style.width =
                    `${percentage}%`;
            }
        }


        // ========================================================
        // RECOMMENDATION
        // ========================================================

        function updateRecommendation(
            recommendationValue,
            level
        ) {

            const decision =
                String(
                    recommendationValue || ""
                ).toUpperCase();


            if (recommendation) {

                if (
                    decision ===
                    "BLOCK"
                ) {

                    recommendation.textContent =
                        "BLOCK TRANSACTION";

                } else if (
                    decision ===
                    "REVIEW"
                ) {

                    recommendation.textContent =
                        "REVIEW TRANSACTION";

                } else {

                    recommendation.textContent =
                        "APPROVE TRANSACTION";
                }


                recommendation.className =
                    `recommendation ${level.toLowerCase()}`;
            }


            if (riskDescription) {

                if (
                    decision ===
                    "BLOCK"
                ) {

                    riskDescription.textContent =
                        "High-risk signals detected. The transaction should be blocked automatically.";

                } else if (
                    decision ===
                    "REVIEW"
                ) {

                    riskDescription.textContent =
                        "Potential risk signals detected. Additional verification is recommended.";

                } else {

                    riskDescription.textContent =
                        "Transaction appears to have a low-risk profile and can be approved.";
                }
            }


            if (decisionCard) {

                decisionCard.className =
                    `decision-card ${level.toLowerCase()}`;
            }


            if (decisionIcon) {

                if (
                    decision ===
                    "BLOCK"
                ) {

                    decisionIcon.textContent =
                        "×";

                } else if (
                    decision ===
                    "REVIEW"
                ) {

                    decisionIcon.textContent =
                        "⚠";

                } else {

                    decisionIcon.textContent =
                        "✓";
                }
            }


            if (decisionText) {

                if (
                    decision ===
                    "BLOCK"
                ) {

                    decisionText.textContent =
                        "Transaction should be blocked due to high-risk behavior.";

                } else if (
                    decision ===
                    "REVIEW"
                ) {

                    decisionText.textContent =
                        "Transaction requires additional verification before approval.";

                } else {

                    decisionText.textContent =
                        "Transaction can be approved.";
                }
            }
        }


        // ========================================================
        // ESCAPE HTML
        // ========================================================

        function escapeHtml(
            text
        ) {

            return String(text)

                .replace(
                    /&/g,
                    "&amp;"
                )

                .replace(
                    /</g,
                    "&lt;"
                )

                .replace(
                    />/g,
                    "&gt;"
                )

                .replace(
                    /"/g,
                    "&quot;"
                )

                .replace(
                    /'/g,
                    "&#039;"
                );
        }


        // ========================================================
        // RISK FACTOR ICON
        // ========================================================

        function getFactorIcon(
            severity
        ) {

            switch (severity) {

                case "HIGH":
                    return "×";

                case "MEDIUM":
                    return "⚠";

                default:
                    return "✓";
            }
        }


        // ========================================================
        // RISK FACTOR CLASS
        // ========================================================

        function getSeverityClass(
            severity
        ) {

            switch (
                String(
                    severity || "LOW"
                ).toUpperCase()
            ) {

                case "HIGH":
                    return "danger";

                case "MEDIUM":
                    return "warning";

                default:
                    return "safe";
            }
        }


        // ========================================================
        // RENDER RISK FACTORS
        // ========================================================

        function renderRiskFactors(
            factors
        ) {

            if (!factorList) {
                return;
            }


            factorList.innerHTML =
                "";


            if (
                !Array.isArray(
                    factors
                )
                ||
                factors.length === 0
            ) {

                if (factorCount) {

                    factorCount.textContent =
                        "0 detected";
                }


                factorList.innerHTML = `

                    <div class="factor-row">

                        <div class="factor-left">

                            <span class="factor-status safe">
                                ✓
                            </span>

                            <div>

                                <strong>
                                    No significant risk factors
                                </strong>

                                <small>
                                    Transaction behavior appears normal
                                </small>

                            </div>

                        </div>

                        <span class="factor-value safe-text">
                            LOW
                        </span>

                    </div>
                `;


                return;
            }


            if (factorCount) {

                factorCount.textContent =
                    `${factors.length} detected`;
            }


            factors.forEach(
                factor => {

                    const severity =
                        String(
                            factor.severity ||
                            "LOW"
                        ).toUpperCase();


                    const severityClass =
                        getSeverityClass(
                            severity
                        );


                    const icon =
                        getFactorIcon(
                            severity
                        );


                    const row =
                        document.createElement(
                            "div"
                        );


                    row.className =
                        "factor-row";


                    row.innerHTML = `

                        <div class="factor-left">

                            <span
                                class="factor-status ${severityClass}"
                            >
                                ${icon}
                            </span>

                            <div>

                                <strong>
                                    ${escapeHtml(
                                        factor.name ||
                                        "Risk Signal"
                                    )}
                                </strong>

                                <small>
                                    ${escapeHtml(
                                        factor.message ||
                                        "Risk signal detected"
                                    )}
                                </small>

                            </div>

                        </div>

                        <span
                            class="factor-value ${severityClass}-text"
                        >
                            ${escapeHtml(
                                severity
                            )}
                        </span>
                    `;


                    factorList.appendChild(
                        row
                    );
                }
            );
        }


        // ========================================================
        // TRANSACTION SNAPSHOT
        // ========================================================

        function updateSnapshot(
            data,
            transaction
        ) {

            if (resultTransactionId) {

                resultTransactionId.textContent =
                    data.transaction_id ||
                    transaction.transaction_id;
            }


            if (resultAmount) {

                resultAmount.textContent =
                    formatCurrency(
                        transaction.amount
                    );
            }


            if (resultPayment) {

                const method =
                    transaction.payment_method ||
                    "";


                resultPayment.textContent =
                    method
                        .charAt(0)
                        .toUpperCase()
                    +
                    method.slice(1);
            }


            if (resultDevice) {

                const device =
                    transaction.device_type ||
                    "";


                resultDevice.textContent =
                    device
                        .charAt(0)
                        .toUpperCase()
                    +
                    device.slice(1);
            }
        }


        // ========================================================
        // ANALYSIS TIMESTAMP
        // ========================================================

        function updateTimestamp() {

            if (!analysisTime) {
                return;
            }


            const now =
                new Date();


            analysisTime.textContent =
                `Analyzed ${
                    now.toLocaleTimeString(
                        "en-IN",
                        {
                            hour:
                                "2-digit",

                            minute:
                                "2-digit",

                            second:
                                "2-digit"
                        }
                    )
                }`;
        }


        // ========================================================
        // RISK SCORE ANIMATION
        // ========================================================

        function animateScore(
            targetScore,
            level
        ) {

            const target =
                Number(
                    targetScore
                ) || 0;


            if (!riskScore) {

                updateRiskScore(
                    target,
                    level
                );

                return;
            }


            const duration =
                700;


            const startTime =
                performance.now();


            function animate(
                currentTime
            ) {

                const elapsed =
                    currentTime -
                    startTime;


                const progress =
                    Math.min(
                        elapsed /
                        duration,
                        1
                    );


                const eased =
                    1 -
                    Math.pow(
                        1 - progress,
                        3
                    );


                const current =
                    target *
                    eased;


                riskScore.textContent =
                    current.toFixed(
                        2
                    );


                if (scoreRing) {

                    scoreRing.style.background = `
                        conic-gradient(
                            var(--accent)
                            0deg
                            ${current * 3.6}deg,

                            #edf0f5
                            ${current * 3.6}deg
                            360deg
                        )
                    `;
                }


                if (
                    progress <
                    1
                ) {

                    requestAnimationFrame(
                        animate
                    );

                } else {

                    updateRiskScore(
                        target,
                        level
                    );
                }
            }


            requestAnimationFrame(
                animate
            );
        }


        // ========================================================
        // UPDATE TRANSACTION RESULT
        // ========================================================

        function updateDashboard(
            data,
            transaction
        ) {

            const score =
                Number(
                    data.risk_score ||
                    0
                );


            const probability =
                Number(
                    data.fraud_probability ||
                    0
                );


            const level =
                String(
                    data.risk_level ||
                    "LOW"
                ).toUpperCase();


            const decision =
                String(
                    data.recommendation ||
                    "APPROVE"
                ).toUpperCase();


            showResults();


            animateScore(
                score,
                level
            );


            updateFraudProbability(
                probability
            );


            updateRecommendation(
                decision,
                level
            );


            renderRiskFactors(
                data.risk_factors
            );


            updateSnapshot(
                data,
                transaction
            );


            updateTimestamp();


            console.log(
                "Risk Engine Response:",
                data
            );
        }


        // ========================================================
        // UPDATE DECISION DONUT
        // ========================================================

        function updateDecisionDonut(
            decisions,
            total
        ) {

            const approve =
                Number(
                    decisions.approve
                ) || 0;


            const review =
                Number(
                    decisions.review
                ) || 0;


            const block =
                Number(
                    decisions.block
                ) || 0;


            const calculatedTotal =
                approve +
                review +
                block;


            const safeTotal =
                Number(total) ||
                calculatedTotal;


            if (
                !safeTotal
            ) {
                return;
            }


            const approvePercent =
                approve /
                safeTotal *
                100;


            const reviewPercent =
                review /
                safeTotal *
                100;


            const blockPercent =
                block /
                safeTotal *
                100;


            const approveDegrees =
                approvePercent *
                3.6;


            const reviewDegrees =
                reviewPercent *
                3.6;


            const reviewEnd =
                approveDegrees +
                reviewDegrees;


            if (donut) {

                donut.style.background = `
                    conic-gradient(

                        var(--green)
                        0deg
                        ${approveDegrees}deg,

                        #f59e0b
                        ${approveDegrees}deg
                        ${reviewEnd}deg,

                        var(--red)
                        ${reviewEnd}deg
                        360deg

                    )
                `;
            }


            if (donutTotal) {

                donutTotal.textContent =
                    safeTotal >= 1000
                        ? `${(
                            safeTotal /
                            1000
                        ).toFixed(1)}K`
                        : formatNumber(
                            safeTotal
                        );
            }


            if (approvePercentage) {

                approvePercentage.textContent =
                    `${approvePercent.toFixed(
                        1
                    )}%`;
            }


            if (reviewPercentage) {

                reviewPercentage.textContent =
                    `${reviewPercent.toFixed(
                        1
                    )}%`;
            }


            if (blockPercentage) {

                blockPercentage.textContent =
                    `${blockPercent.toFixed(
                        1
                    )}%`;
            }


            // Store counts for tooltip/debugging
            donut?.setAttribute(
                "data-approve",
                approve
            );

            donut?.setAttribute(
                "data-review",
                review
            );

            donut?.setAttribute(
                "data-block",
                block
            );
        }


        // ========================================================
        // UPDATE MODEL METRICS
        // ========================================================

        function updateModelMetrics(
            metrics
        ) {

            if (!metrics) {
                return;
            }


            if (rocAuc) {

                rocAuc.textContent =
                    Number(
                        metrics.roc_auc
                    ).toFixed(4);
            }


            if (prAuc) {

                prAuc.textContent =
                    Number(
                        metrics.pr_auc
                    ).toFixed(4);
            }


            if (precisionMetric) {

                precisionMetric.textContent =
                    `${Number(
                        metrics.precision
                    ).toFixed(2)}%`;
            }


            if (recallMetric) {

                recallMetric.textContent =
                    `${Number(
                        metrics.recall
                    ).toFixed(2)}%`;
            }


            if (f1Metric) {

                f1Metric.textContent =
                    `${Number(
                        metrics.f1
                    ).toFixed(2)}%`;
            }
        }


        // ========================================================
        // BUILD SVG CHART
        // ========================================================

        function buildChartPath(
            values
        ) {

            if (
                !Array.isArray(values)
                ||
                values.length === 0
            ) {

                return null;
            }


            const width =
                800;

            const height =
                230;

            const paddingX =
                8;

            const paddingY =
                15;


            const points =
                values.map(
                    (
                        value,
                        index
                    ) => {

                        const x =
                            paddingX
                            +
                            (
                                index /
                                Math.max(
                                    values.length -
                                    1,
                                    1
                                )
                            )
                            *
                            (
                                width -
                                paddingX *
                                2
                            );


                        const normalized =
                            Math.min(
                                Math.max(
                                    Number(
                                        value
                                    ) ||
                                    0,
                                    0
                                ),
                                100
                            );


                        const y =
                            height
                            -
                            paddingY
                            -
                            (
                                normalized /
                                100
                            )
                            *
                            (
                                height -
                                paddingY *
                                2
                            );


                        return {
                            x,
                            y
                        };
                    }
                );


            let linePath =
                "";


            points.forEach(
                (
                    point,
                    index
                ) => {

                    if (
                        index ===
                        0
                    ) {

                        linePath +=
                            `M${point.x},${point.y}`;

                        return;
                    }


                    const previous =
                        points[
                            index - 1
                        ];


                    const controlX =
                        (
                            previous.x +
                            point.x
                        )
                        /
                        2;


                    linePath += `
                        C
                        ${controlX},${previous.y}
                        ${controlX},${point.y}
                        ${point.x},${point.y}
                    `;
                }
            );


            const fillPath = `
                ${linePath}

                L${width},${height}

                L0,${height}

                Z
            `;


            return {
                linePath,
                fillPath
            };
        }


        // ========================================================
        // UPDATE RISK ACTIVITY
        // ========================================================

        function updateRiskActivity(
            activity
        ) {

            if (
                !Array.isArray(
                    activity
                )
            ) {
                return;
            }


            const mode =
                activityMode
                    ? activityMode.value
                    : "risk";


            let values;


            if (
                mode ===
                "transactions"
            ) {

                const max =
                    Math.max(
                        ...activity.map(
                            item =>
                                Number(
                                    item.transactions
                                ) ||
                                0
                        ),
                        1
                    );


                values =
                    activity.map(
                        item => {

                            const count =
                                Number(
                                    item.transactions
                                ) ||
                                0;


                            return (
                                count /
                                max *
                                100
                            );
                        }
                    );

            } else {

                values =
                    activity.map(
                        item =>
                            Number(
                                item.average_risk
                            ) ||
                            0
                    );
            }


            const chart =
                buildChartPath(
                    values
                );


            if (!chart) {
                return;
            }


            if (riskChartLine) {

                riskChartLine.setAttribute(
                    "d",
                    chart.linePath
                );
            }


            if (riskChartFill) {

                riskChartFill.setAttribute(
                    "d",
                    chart.fillPath
                );
            }
        }


        // ========================================================
        // LOAD DASHBOARD METRICS
        // ========================================================

        async function loadDashboardMetrics() {

            try {

                const response =
                    await fetch(
                        "/api/v1/dashboard-metrics",
                        {
                            method:
                                "GET",

                            cache:
                                "no-store"
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.error ||
                        "Unable to load dashboard metrics."
                    );
                }


                dashboardData =
                    data;


                // =================================================
                // KPI — TRANSACTIONS
                // =================================================

                if (transactionsAnalyzed) {

                    transactionsAnalyzed.textContent =
                        formatNumber(
                            data.transactions_analyzed
                        );
                }


                if (transactionStatus) {

                    transactionStatus.textContent =
                        "LIVE DATA";
                }


                // =================================================
                // KPI — FRAUD
                // =================================================

                if (fraudDetected) {

                    fraudDetected.textContent =
                        `${Number(
                            data.fraud_rate
                        ).toFixed(2)}%`;
                }


                if (fraudCount) {

                    fraudCount.textContent =
                        formatNumber(
                            data.fraud_count
                        );
                }


                // =================================================
                // KPI — BLOCKED VALUE
                // =================================================

                if (blockedValue) {

                    blockedValue.textContent =
                        formatCompactINR(
                            data.blocked_value
                        );
                }


                if (blockedTransactions) {

                    blockedTransactions.textContent =
                        formatNumber(
                            data.decisions.block
                        );
                }


                // =================================================
                // KPI — ACCURACY
                // =================================================

                if (modelAccuracy) {

                    modelAccuracy.textContent =
                        `${Number(
                            data.model_metrics.accuracy
                        ).toFixed(2)}%`;
                }


                if (modelStatus) {

                    modelStatus.textContent =
                        "RANDOM FOREST";
                }


                // =================================================
                // DONUT
                // =================================================

                updateDecisionDonut(
                    data.decisions,
                    data.transactions_analyzed
                );


                // =================================================
                // MODEL
                // =================================================

                updateModelMetrics(
                    data.model_metrics
                );


                // =================================================
                // RISK ACTIVITY
                // =================================================

                updateRiskActivity(
                    data.risk_activity
                );


                console.log(
                    "Dashboard analytics:",
                    data
                );


                return data;


            } catch (error) {

                console.error(
                    "Dashboard metrics error:",
                    error
                );


                if (
                    transactionStatus
                ) {

                    transactionStatus.textContent =
                        "DATA ERROR";
                }


                showToast(
                    error.message ||
                    "Unable to load dashboard analytics.",
                    "error"
                );
            }
        }


        // ========================================================
        // ANALYZE TRANSACTION
        // ========================================================

        async function analyzeTransaction() {

            const transaction =
                collectTransaction();


            if (
                !transaction.amount ||
                transaction.amount <= 0
            ) {

                showToast(
                    "Please enter a valid transaction amount.",
                    "error"
                );

                return;
            }


            setLoading(
                true
            );


            try {

                const response =
                    await fetch(
                        "/api/v1/risk-score",
                        {

                            method:
                                "POST",

                            headers: {

                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    transaction
                                )
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.error ||
                        "Risk analysis failed."
                    );
                }


                updateDashboard(
                    data,
                    transaction
                );


                showToast(
                    `Analysis complete — ${data.risk_level} risk`,
                    "success"
                );


            } catch (error) {

                console.error(
                    "Risk Engine Error:",
                    error
                );


                showToast(
                    error.message ||
                    "Unable to connect to the risk engine.",
                    "error"
                );


            } finally {

                setLoading(
                    false
                );
            }
        }


        // ========================================================
        // FORM SUBMIT
        // ========================================================

        if (form) {

            form.addEventListener(
                "submit",
                event => {

                    event.preventDefault();

                    analyzeTransaction();
                }
            );
        }


        // ========================================================
        // CHART MODE
        // ========================================================

        if (activityMode) {

            activityMode.addEventListener(
                "change",
                () => {

                    if (
                        dashboardData
                    ) {

                        updateRiskActivity(
                            dashboardData.risk_activity
                        );
                    }
                }
            );
        }


        // ========================================================
        // INITIALIZATION
        // ========================================================

        function initialize() {

            if (resultContent) {

                resultContent.classList.add(
                    "hidden"
                );
            }


            if (emptyState) {

                emptyState.classList.remove(
                    "hidden"
                );
            }


            if (factorCount) {

                factorCount.textContent =
                    "0 detected";
            }


            // ====================================================
            // LOAD REAL ANALYTICS
            // ====================================================

            loadDashboardMetrics();


            // ====================================================
            // REFRESH DATA EVERY 60 SECONDS
            // ====================================================

            setInterval(
                loadDashboardMetrics,
                60000
            );
        }


        initialize();

    }
);
