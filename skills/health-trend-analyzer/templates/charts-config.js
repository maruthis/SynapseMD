/**
 * ECharts chart configuration file
 * Health Trend Analysis Report - Complete configuration for 6 chart types
 *
 * Usage:
 * 1. Include this file in HTML
 * 2. Call the corresponding chart initialization function
 * 3. Pass in actual data
 */

// ===== 1. Weight/BMI Trend Chart Configuration =====

/**
 * Initialize Weight/BMI trend chart (dual-axis line chart)
 * @param {Array} weightData - Weight data [{date: '2025-10', weight: 60.8}, ...]
 * @param {Array} bmiData - BMI data [{date: '2025-10', bmi: 22.3}, ...]
 */
function initWeightChart(weightData, bmiData) {
    const chart = echarts.init(document.getElementById('weight-chart'));

    const dates = weightData.map(d => d.date);
    const weights = weightData.map(d => d.weight);
    const bmis = bmiData.map(d => d.bmi);

    const option = {
        title: {
            text: 'Weight/BMI Change Trend',
            left: 'center',
            textStyle: { fontSize: 18, fontWeight: 'bold' }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'cross' }
        },
        legend: {
            data: ['Weight (kg)', 'BMI'],
            top: 40
        },
        grid: {
            left: '3%',
            right: '3%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: dates,
            boundaryGap: false
        },
        yAxis: [
            {
                type: 'value',
                name: 'Weight (kg)',
                position: 'left',
                axisLabel: { formatter: '{value} kg' }
            },
            {
                type: 'value',
                name: 'BMI',
                position: 'right',
                axisLabel: { formatter: '{value}' }
            }
        ],
        series: [
            {
                name: 'Weight',
                type: 'line',
                data: weights,
                smooth: true,
                yAxisIndex: 0,
                itemStyle: { color: '#3b82f6' },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
                        { offset: 1, color: 'rgba(59, 130, 246, 0.05)' }
                    ])
                },
                markLine: {
                    data: [
                        { type: 'average', name: 'Average' }
                    ]
                }
            },
            {
                name: 'BMI',
                type: 'line',
                data: bmis,
                smooth: true,
                yAxisIndex: 1,
                itemStyle: { color: '#8b5cf6' },
                markLine: {
                    data: [
                        { yAxis: 18.5, name: 'BMI Lower Limit', lineStyle: { type: 'dashed', color: '#22c55e' } },
                        { yAxis: 24, name: 'BMI Upper Limit', lineStyle: { type: 'dashed', color: '#f59e0b' } },
                        { yAxis: 28, name: 'Overweight Line', lineStyle: { type: 'dashed', color: '#ef4444' } }
                    ]
                }
            }
        ]
    };

    chart.setOption(option);
    return chart;
}

// ===== 2. Symptom Frequency Chart Configuration =====

/**
 * Initialize symptom frequency bar chart
 * @param {Array} symptomsData - Symptom data [{name: 'headache', count: 4, severity: 'high'}, ...]
 */
function initSymptomsChart(symptomsData) {
    const chart = echarts.init(document.getElementById('symptoms-chart'));

    const names = symptomsData.map(d => d.name);
    const counts = symptomsData.map(d => d.count);

    // Set color based on frequency/severity
    const colors = symptomsData.map(d => {
        if (d.severity === 'high') return '#ef4444';
        if (d.severity === 'medium') return '#f59e0b';
        return '#22c55e';
    });

    const option = {
        title: {
            text: 'Symptom Frequency Statistics',
            left: 'center',
            textStyle: { fontSize: 18, fontWeight: 'bold' }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' }
        },
        xAxis: {
            type: 'category',
            data: names,
            axisLabel: { interval: 0, rotate: 30 }
        },
        yAxis: {
            type: 'value',
            name: 'Occurrences'
        },
        series: [{
            type: 'bar',
            data: symptomsData.map((d, i) => ({
                value: d.count,
                itemStyle: { color: colors[i] }
            })),
            label: {
                show: true,
                position: 'top',
                formatter: '{c} times'
            },
            itemStyle: {
                borderRadius: [4, 4, 0, 0]
            }
        }]
    };

    chart.setOption(option);
    return chart;
}

/**
 * Initialize symptom timeline chart (stacked area chart)
 * @param {Array} timelineData - Timeline data [{date: '2025-10-01', symptoms: ['headache', 'fatigue']}, ...]
 */
function initSymptomsTimelineChart(timelineData) {
    const chart = echarts.init(document.getElementById('symptoms-timeline-chart'));

    // Aggregate symptom data
    const symptomTypes = [...new Set(timelineData.flatMap(d => d.symptoms))];
    const dates = [...new Set(timelineData.map(d => d.date))].sort();

    const series = symptomTypes.map(symptom => {
        const data = dates.map(date => {
            const dayData = timelineData.find(d => d.date === date);
            return dayData && dayData.symptoms.includes(symptom) ? 1 : 0;
        });

        return {
            name: symptom,
            type: 'line',
            data: data,
            stack: 'symptoms',
            areaStyle: {},
            emphasis: { focus: 'series' }
        };
    });

    const option = {
        title: {
            text: 'Symptom Timeline',
            left: 'center',
            textStyle: { fontSize: 18, fontWeight: 'bold' }
        },
        tooltip: {
            trigger: 'axis',
            formatter: function(params) {
                const symptoms = params.filter(p => p.value > 0).map(p => p.seriesName);
                return `${params[0].axisValue}<br/>Symptoms: ${symptoms.join(', ') || 'None'}`;
            }
        },
        legend: {
            data: symptomTypes,
            top: 40
        },
        xAxis: {
            type: 'category',
            data: dates,
            boundaryGap: false
        },
        yAxis: {
            type: 'value',
            max: 1,
            axisLabel: { show: false }
        },
        series: series
    };

    chart.setOption(option);
    return chart;
}

// ===== 3. Medication Adherence Chart Configuration =====

/**
 * Initialize medication adherence gauge
 * @param {number} adherenceRate - Adherence percentage (0-100)
 */
function initMedicationGauge(adherenceRate) {
    const chart = echarts.init(document.getElementById('medication-gauge'));

    const option = {
        title: {
            text: 'Overall Adherence',
            left: 'center',
            textStyle: { fontSize: 18, fontWeight: 'bold' }
        },
        series: [{
            type: 'gauge',
            startAngle: 180,
            endAngle: 0,
            min: 0,
            max: 100,
            splitNumber: 5,
            axisLine: {
                lineStyle: {
                    width: 20,
                    color: [
                        [0.6, '#ef4444'],
                        [0.8, '#f59e0b'],
                        [1, '#22c55e']
                    ]
                }
            },
            pointer: {
                icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
                length: '12%',
                width: 20,
                offsetCenter: [0, '-60%'],
                itemStyle: { color: 'auto' }
            },
            axisTick: { length: 12, lineStyle: { color: 'auto', width: 2 } },
            splitLine: { length: 20, lineStyle: { color: 'auto', width: 5 } },
            axisLabel: { color: '#464646', fontSize: 14, distance: -60 },
            detail: {
                valueAnimation: true,
                formatter: '{value}%',
                color: 'auto',
                fontSize: 30,
                offsetCenter: [0, '-20%']
            },
            data: [{ value: adherenceRate }]
        }]
    };

    chart.setOption(option);
    return chart;
}

/**
 * Initialize medication record pie chart
 * @param {Object} medicationStats - Medication statistics {taken: 26, missed: 2, pending: 0}
 */
function initMedicationPie(medicationStats) {
    const chart = echarts.init(document.getElementById('medication-pie'));

    const option = {
        title: {
            text: 'Medication Record Distribution',
            left: 'center',
            textStyle: { fontSize: 18, fontWeight: 'bold' }
        },
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        series: [{
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
            },
            label: {
                show: true,
                formatter: '{b}: {c} times\n({d}%)'
            },
            emphasis: {
                label: { show: true, fontSize: 16, fontWeight: 'bold' }
            },
            data: [
                { value: medicationStats.taken, name: 'Taken', itemStyle: { color: '#22c55e' } },
                { value: medicationStats.missed, name: 'Missed', itemStyle: { color: '#ef4444' } },
                { value: medicationStats.pending, name: 'Pending', itemStyle: { color: '#f59e0b' } }
            ]
        }]
    };

    chart.setOption(option);
    return chart;
}

// ===== 4. Lab Results Trend Chart Configuration =====

/**
 * Initialize lab results trend chart (multi-series line chart)
 * @param {Object} labData - Lab data
 * @param {Array} labData.dates - Date array
 * @param {Array} labData.series - Indicator series [{name: 'Cholesterol', data: [240, 230, 210], unit: 'mg/dL', range: [0, 200]}, ...]
 */
function initLabChart(labData) {
    const chart = echarts.init(document.getElementById('lab-chart'));

    const series = labData.series.map(s => ({
        name: s.name,
        type: 'line',
        data: s.data,
        smooth: true,
        yAxisIndex: s.name === 'Blood Glucose' ? 1 : 0,
        markLine: {
            silent: true,
            lineStyle: { type: 'dashed' },
            data: [
                { yAxis: s.range[1], name: 'Reference Upper Limit', label: { formatter: `${s.range[1]} ${s.unit}` } }
            ]
        }
    }));

    const option = {
        title: {
            text: 'Lab Indicator Changes',
            left: 'center',
            textStyle: { fontSize: 18, fontWeight: 'bold' }
        },
        tooltip: {
            trigger: 'axis',
            formatter: function(params) {
                let result = params[0].axisValue + '<br/>';
                params.forEach(p => {
                    result += `${p.seriesName}: ${p.value} ${labData.series.find(s => s.name === p.seriesName).unit}<br/>`;
                });
                return result;
            }
        },
        legend: {
            data: labData.series.map(s => s.name),
            top: 40
        },
        xAxis: {
            type: 'category',
            data: labData.dates,
            boundaryGap: false
        },
        yAxis: [
            {
                type: 'value',
                name: 'mg/dL',
                position: 'left'
            },
            {
                type: 'value',
                name: 'mmol/L',
                position: 'right'
            }
        ],
        series: series
    };

    chart.setOption(option);
    return chart;
}

// ===== 5. Correlation Heatmap Configuration =====

/**
 * Initialize correlation heatmap
 * @param {Object} correlationData - Correlation data
 * @param {Array} correlationData.xAxis - X-axis labels
 * @param {Array} correlationData.yAxis - Y-axis labels
 * @param {Array} correlationData.data - Correlation matrix [[x, y, value], ...]
 */
function initCorrelationHeatmap(correlationData) {
    const chart = echarts.init(document.getElementById('correlation-heatmap'));

    const option = {
        title: {
            text: 'Indicator Correlation Analysis',
            left: 'center',
            textStyle: { fontSize: 18, fontWeight: 'bold' }
        },
        tooltip: {
            position: 'top',
            formatter: function(params) {
                return `${correlationData.xAxis[params.value[0]]} × ${correlationData.yAxis[params.value[1]]}<br/>Correlation coefficient: ${params.value[2].toFixed(2)}`;
            }
        },
        grid: {
            height: '50%',
            top: '15%'
        },
        xAxis: {
            type: 'category',
            data: correlationData.xAxis,
            splitArea: { show: true }
        },
        yAxis: {
            type: 'category',
            data: correlationData.yAxis,
            splitArea: { show: true }
        },
        visualMap: {
            min: -1,
            max: 1,
            calculable: true,
            orient: 'horizontal',
            left: 'center',
            bottom: '5%',
            inRange: {
                color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffcc',
                       '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
            },
            text: ['Positive correlation', 'Negative correlation']
        },
        series: [{
            type: 'heatmap',
            data: correlationData.data,
            label: {
                show: true,
                formatter: function(params) {
                    return params.value[2].toFixed(2);
                }
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    };

    chart.setOption(option);
    return chart;
}

// ===== 6. Mood and Sleep Chart Configuration =====

/**
 * Initialize mood and sleep trend chart (dual-axis area chart)
 * @param {Array} moodSleepData - Mood and sleep data
 * @param {Array} moodSleepData.dates - Date array
 * @param {Array} moodSleepData.moodScores - Mood score array (0-10)
 * @param {Array} moodSleepData.sleepHours - Sleep duration array (hours)
 */
function initMoodSleepChart(moodSleepData) {
    const chart = echarts.init(document.getElementById('mood-chart'));

    const option = {
        title: {
            text: 'Mood and Sleep Trends',
            left: 'center',
            textStyle: { fontSize: 18, fontWeight: 'bold' }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'cross' }
        },
        legend: {
            data: ['Mood Score', 'Sleep Duration'],
            top: 40
        },
        xAxis: {
            type: 'category',
            data: moodSleepData.dates,
            boundaryGap: false
        },
        yAxis: [
            {
                type: 'value',
                name: 'Mood Score',
                position: 'left',
                min: 0,
                max: 10,
                axisLabel: { formatter: '{value}' }
            },
            {
                type: 'value',
                name: 'Sleep Duration (hours)',
                position: 'right',
                min: 0,
                max: 12,
                axisLabel: { formatter: '{value} h' }
            }
        ],
        series: [
            {
                name: 'Mood',
                type: 'line',
                data: moodSleepData.moodScores,
                smooth: true,
                yAxisIndex: 0,
                itemStyle: { color: '#ec4899' },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(236, 72, 153, 0.4)' },
                        { offset: 1, color: 'rgba(236, 72, 153, 0.05)' }
                    ])
                }
            },
            {
                name: 'Sleep',
                type: 'line',
                data: moodSleepData.sleepHours,
                smooth: true,
                yAxisIndex: 1,
                itemStyle: { color: '#6366f1' },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(99, 102, 241, 0.4)' },
                        { offset: 1, color: 'rgba(99, 102, 241, 0.05)' }
                    ])
                },
                markLine: {
                    data: [
                        { yAxis: 7, name: 'Recommended Sleep', lineStyle: { type: 'dashed', color: '#22c55e' } }
                    ]
                }
            }
        ]
    };

    chart.setOption(option);
    return chart;
}

// ===== Unified Initialization Function =====

/**
 * Initialize all charts
 * @param {Object} allData - All chart data
 */
function initAllCharts(allData) {
    const charts = {};

    // 1. Weight/BMI chart
    if (allData.weight && allData.bmi) {
        charts.weight = initWeightChart(allData.weight, allData.bmi);
    }

    // 2. Symptom charts
    if (allData.symptoms) {
        charts.symptoms = initSymptomsChart(allData.symptoms.frequency);
        charts.symptomsTimeline = initSymptomsTimelineChart(allData.symptoms.timeline);
    }

    // 3. Medication adherence charts
    if (allData.medications) {
        charts.medicationGauge = initMedicationGauge(allData.medications.adherenceRate);
        charts.medicationPie = initMedicationPie(allData.medications.stats);
    }

    // 4. Lab results chart
    if (allData.labResults) {
        charts.labResults = initLabChart(allData.labResults);
    }

    // 5. Correlation heatmap
    if (allData.correlations) {
        charts.correlations = initCorrelationHeatmap(allData.correlations);
    }

    // 6. Mood and sleep chart
    if (allData.moodSleep) {
        charts.moodSleep = initMoodSleepChart(allData.moodSleep);
    }

    return charts;
}

// ===== Module Export =====

// If in Node.js environment
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initWeightChart,
        initSymptomsChart,
        initSymptomsTimelineChart,
        initMedicationGauge,
        initMedicationPie,
        initLabChart,
        initCorrelationHeatmap,
        initMoodSleepChart,
        initAllCharts
    };
}
