# Health Trend Analyzer - Analysis Algorithms Guide

This document provides detailed descriptions of the various analysis algorithms used by the Health Trend Analyzer, including time series analysis, correlation analysis, change point detection, and predictive insight generation.

## Algorithm Overview

| Algorithm Type | Purpose | Data Requirements | Output |
|---------|------|---------|------|
| Linear Regression | Trend detection | ≥3 data points | Slope, intercept, R² |
| Moving Average | Smoothing | ≥5 data points | Smoothed curve |
| Pearson Correlation | Continuous variable correlation | ≥30 data points | Correlation coefficient (-1~1) |
| Spearman Correlation | Ordinal variable correlation | ≥30 data points | Correlation coefficient (-1~1) |
| CUSUM | Change point detection | ≥10 data points | Change point locations |
| Percentile | Outlier detection | ≥20 data points | Outlier list |
| Time Series Decomposition | Seasonality analysis | ≥12 data points | Trend + Seasonal + Residual |

---

## 1. Time Series Analysis

### 1.1 Trend Detection (Linear Regression)

**Purpose**: Identify the direction and strength of a linear trend in data over time.

**Algorithm**: Ordinary least squares linear regression

```javascript
function linearRegression(timeSeries) {
  // timeSeries: [{date: '2025-10-01', value: 70.8}, ...]

  const n = timeSeries.length;

  // Convert dates to numeric values (days since the first date)
  const baseline = new Date(timeSeries[0].date);
  const x = timeSeries.map(d => (new Date(d.date) - baseline) / (1000 * 60 * 60 * 24));
  const y = timeSeries.map(d => d.value);

  // Calculate means
  const meanX = x.reduce((a, b) => a + b, 0) / n;
  const meanY = y.reduce((a, b) => a + b, 0) / n;

  // Calculate slope (β1) and intercept (β0)
  let numerator = 0;
  let denominator = 0;

  for (let i = 0; i < n; i++) {
    numerator += (x[i] - meanX) * (y[i] - meanY);
    denominator += Math.pow(x[i] - meanX, 2);
  }

  const slope = numerator / denominator;
  const intercept = meanY - slope * meanX;

  // Calculate R² (coefficient of determination)
  const predictions = x.map(xi => slope * xi + intercept);
  const ssTot = y.reduce((sum, yi) => sum + Math.pow(yi - meanY, 2), 0);
  const ssRes = y.reduce((sum, yi, i) => sum + Math.pow(yi - predictions[i], 2), 0);
  const r2 = 1 - (ssRes / ssTot);

  // Calculate total change
  const firstValue = y[0];
  const lastValue = y[y.length - 1];
  const totalChange = lastValue - firstValue;
  const percentChange = (totalChange / firstValue) * 100;

  return {
    slope: slope,              // Slope (change per day)
    intercept: intercept,      // Intercept
    r2: r2,                    // Coefficient of determination (0~1, closer to 1 = better fit)
    direction: slope > 0.001 ? 'increasing' : slope < -0.001 ? 'decreasing' : 'stable',
    totalChange: totalChange,
    percentChange: percentChange,
    trendStrength: Math.abs(r2) > 0.7 ? 'strong' : Math.abs(r2) > 0.4 ? 'moderate' : 'weak'
  };
}
```

**Result Interpretation**:
- `slope > 0`: Upward trend
- `slope < 0`: Downward trend
- `slope ≈ 0`: Stable
- `r2 > 0.7`: Strong trend (good fit)
- `r2 < 0.4`: Weak trend (poor fit)

**Example**:
```javascript
const weightTrend = linearRegression(weightHistory);
// Result:
{
  slope: -0.018,           // Decreasing 0.018 kg per day
  r2: 0.82,               // Strong trend
  direction: 'decreasing',
  totalChange: -2.3,      // Lost 2.3 kg over 90 days
  percentChange: -3.2,    // Decreased by 3.2%
  trendStrength: 'strong'
}
```

### 1.2 Moving Average (Smoothing)

**Purpose**: Smooth short-term fluctuations to highlight long-term trends.

**Algorithm**: Simple Moving Average (SMA)

```javascript
function movingAverage(timeSeries, windowSize = 7) {
  // timeSeries: [{date: '2025-10-01', value: 70.8}, ...]
  // windowSize: window size (days)

  const smoothed = [];

  for (let i = 0; i < timeSeries.length; i++) {
    const start = Math.max(0, i - Math.floor(windowSize / 2));
    const end = Math.min(timeSeries.length, i + Math.floor(windowSize / 2) + 1);

    const window = timeSeries.slice(start, end);
    const avg = window.reduce((sum, point) => sum + point.value, 0) / window.length;

    smoothed.push({
      date: timeSeries[i].date,
      value: timeSeries[i].value,
      smoothed: avg
    });
  }

  return smoothed;
}
```

**Window Size Selection**:
- 7 days: Weekly smoothing (eliminate within-week fluctuations)
- 30 days: Monthly smoothing (eliminate within-month fluctuations)
- 90 days: Quarterly smoothing (eliminate quarterly fluctuations)

### 1.3 Weighted Moving Average

**Purpose**: Give more weight to recent data for faster response to trend changes.

```javascript
function weightedMovingAverage(timeSeries, windowSize = 7) {
  const weights = [];
  for (let i = 1; i <= windowSize; i++) {
    weights.push(i); // Linear weights: 1, 2, 3, ..., 7
  }

  const smoothed = [];

  for (let i = windowSize - 1; i < timeSeries.length; i++) {
    let sum = 0;
    let weightSum = 0;

    for (let j = 0; j < windowSize; j++) {
      sum += timeSeries[i - j].value * weights[j];
      weightSum += weights[j];
    }

    smoothed.push({
      date: timeSeries[i].date,
      value: timeSeries[i].value,
      smoothed: sum / weightSum
    });
  }

  return smoothed;
}
```

### 1.4 Time Series Decomposition

**Purpose**: Decompose a time series into three components: trend, seasonality, and residual.

**Algorithm**: STL decomposition (Seasonal-Trend decomposition using Loess)

```javascript
function decomposeTimeSeries(timeSeries, period = 7) {
  // Simplified version: additive model Y = Trend + Seasonal + Residual

  const n = timeSeries.length;
  const values = timeSeries.map(d => d.value);

  // 1. Extract trend (using moving average)
  const trend = movingAverage(timeSeries, period).map(d => d.smoothed);

  // 2. Extract seasonality
  const seasonal = [];
  for (let i = 0; i < n; i++) {
    const detrended = values[i] - trend[i];
    const seasonIndex = i % period;
    seasonal.push(detrended);
  }

  // Calculate average seasonality
  const avgSeasonal = Array(period).fill(0);
  const seasonCount = Array(period).fill(0);

  for (let i = 0; i < n; i++) {
    const seasonIndex = i % period;
    avgSeasonal[seasonIndex] += seasonal[i];
    seasonCount[seasonIndex]++;
  }

  for (let s = 0; s < period; s++) {
    avgSeasonal[s] = avgSeasonal[s] / seasonCount[s];
  }

  // 3. Calculate residual
  const residual = values.map((v, i) => v - trend[i] - avgSeasonal[i % period]);

  return {
    trend: trend,
    seasonal: avgSeasonal,
    residual: residual,
    hasSeasonality: Math.max(...avgSeasonal) - Math.min(...avgSeasonal) > 0.5 * Math.std(values)
  };
}
```

---

## 2. Correlation Analysis

### 2.1 Pearson Correlation Coefficient

**Purpose**: Measure the strength of linear correlation between two continuous variables.

**Formula**:
```
r = Σ[(xi - x̄)(yi - ȳ)] / √[Σ(xi - x̄)² × Σ(yi - ȳ)²]
```

**Range**: -1 (perfect negative correlation) to 1 (perfect positive correlation), 0 indicates no linear correlation

```javascript
function pearsonCorrelation(x, y) {
  // x, y: numeric arrays
  // Must be of equal length

  const n = x.length;
  if (n !== y.length || n < 2) {
    return null; // Invalid data
  }

  // Calculate means
  const meanX = x.reduce((a, b) => a + b, 0) / n;
  const meanY = y.reduce((a, b) => a + b, 0) / n;

  // Calculate numerator and denominator
  let numerator = 0;
  let sumX2 = 0;
  let sumY2 = 0;

  for (let i = 0; i < n; i++) {
    const dx = x[i] - meanX;
    const dy = y[i] - meanY;
    numerator += dx * dy;
    sumX2 += dx * dx;
    sumY2 += dy * dy;
  }

  const denominator = Math.sqrt(sumX2 * sumY2);

  if (denominator === 0) {
    return 0; // Avoid division by zero
  }

  const r = numerator / denominator;

  // Calculate significance (p-value)
  const t = r * Math.sqrt((n - 2) / (1 - r * r));
  const pValue = 2 * (1 - studentTCDF(Math.abs(t), n - 2));

  return {
    coefficient: r,
    significance: pValue < 0.05 ? 'significant' : pValue < 0.1 ? 'marginal' : 'not_significant',
    pValue: pValue,
    strength: Math.abs(r) > 0.7 ? 'strong' : Math.abs(r) > 0.4 ? 'moderate' : Math.abs(r) > 0.2 ? 'weak' : 'very_weak',
    direction: r > 0.3 ? 'positive' : r < -0.3 ? 'negative' : 'none'
  };
}
```

**Result Interpretation**:
- `r > 0.7`: Strong positive correlation
- `0.4 < r ≤ 0.7`: Moderate positive correlation
- `0.2 < r ≤ 0.4`: Weak positive correlation
- `-0.2 ≤ r ≤ 0.2`: No correlation
- `-0.4 ≤ r < -0.2`: Weak negative correlation
- `-0.7 ≤ r < -0.4`: Moderate negative correlation
- `r < -0.7`: Strong negative correlation

**Example**:
```javascript
const sleepHours = [7.5, 6.2, 5.8, 7.0, 6.5, 8.0, 6.8];
const moodScores = [8, 6, 5, 7, 6, 9, 7];

const correlation = pearsonCorrelation(sleepHours, moodScores);
// Result:
{
  coefficient: 0.78,
  significance: 'significant',
  pValue: 0.03,
  strength: 'strong',
  direction: 'positive'
}
// Interpretation: Sleep duration and mood score show a strong positive correlation (r=0.78), statistically significant (p<0.05)
```

### 2.2 Spearman Rank Correlation

**Purpose**: Measure the monotonic relationship between two ordinal variables or non-normally distributed variables.

**Characteristics**:
- Robust to outliers
- Can detect non-linear monotonic relationships
- Applicable to ordinal categorical data

```javascript
function spearmanCorrelation(x, y) {
  const n = x.length;
  if (n !== y.length || n < 2) {
    return null;
  }

  // Convert data to ranks
  const rank = (arr) => {
    const sorted = arr.map((v, i) => ({ value: v, index: i }))
                          .sort((a, b) => a.value - b.value);
    const ranks = Array(n);
    sorted.forEach((item, i) => {
      ranks[item.index] = i + 1;
    });
    return ranks;
  };

  const rankX = rank(x);
  const rankY = rank(y);

  // Calculate Pearson correlation coefficient (based on ranks)
  const meanRankX = rankX.reduce((a, b) => a + b, 0) / n;
  const meanRankY = rankY.reduce((a, b) => a + b, 0) / n;

  let numerator = 0;
  let sumX2 = 0;
  let sumY2 = 0;

  for (let i = 0; i < n; i++) {
    const dx = rankX[i] - meanRankX;
    const dy = rankY[i] - meanRankY;
    numerator += dx * dy;
    sumX2 += dx * dx;
    sumY2 += dy * dy;
  }

  const denominator = Math.sqrt(sumX2 * sumY2);

  if (denominator === 0) {
    return { coefficient: 0 };
  }

  const rho = numerator / denominator;

  return {
    coefficient: rho,
    strength: Math.abs(rho) > 0.7 ? 'strong' : Math.abs(rho) > 0.4 ? 'moderate' : 'weak',
    direction: rho > 0.3 ? 'positive' : rho < -0.3 ? 'negative' : 'none'
  };
}
```

### 2.3 Cross-Correlation

**Purpose**: Detect lagged relationships between two time series.

**Example**: Analyze whether today's sleep affects tomorrow's mood

```javascript
function crossCorrelation(x, y, maxLag = 7) {
  // x, y: time series arrays
  // maxLag: maximum lag in days

  const correlations = [];

  for (let lag = -maxLag; lag <= maxLag; lag++) {
    let xShifted, yShifted;

    if (lag >= 0) {
      // x lagged by lag days: correlation of x(t) with y(t-lag)
      xShifted = x.slice(lag);
      yShifted = y.slice(0, y.length - lag);
    } else {
      // y lagged by |lag| days: correlation of x(t) with y(t+lag)
      xShifted = x.slice(0, x.length + lag);
      yShifted = y.slice(-lag);
    }

    if (xShifted.length < 10) continue; // Too few data points

    const corr = pearsonCorrelation(xShifted, yShifted);
    if (corr) {
      correlations.push({
        lag: lag,
        coefficient: corr.coefficient,
        significance: corr.significance
      });
    }
  }

  // Find the strongest correlation
  const maxCorr = correlations.reduce((max, curr) =>
    Math.abs(curr.coefficient) > Math.abs(max.coefficient) ? curr : max
  );

  return {
    correlations: correlations,
    maxCorrelation: maxCorr,
    bestLag: maxCorr.lag,
    interpretation: maxCorr.lag > 0 ?
      `Today's ${maxCorr.lag === 1 ? '' : maxCorr.lag + '-day later '}${y} correlates with current x` :
      maxCorr.lag < 0 ?
      `Today's x correlates with ${-maxCorr.lag === 1 ? '' : -maxCorr.lag + '-day later '}y` :
      'x and y are synchronously correlated'
  };
}
```

**Example**:
```javascript
const sleepHours = [7, 6, 8, 5, 7, 6, 8, ...];
const moodScores = [8, 6, 9, 5, 7, 6, 8, ...];

const cc = crossCorrelation(sleepHours, moodScores, 3);
// Result: Strongest correlation at lag 0 days (r=0.78)
// Interpretation: Today's sleep is most correlated with today's mood
```

---

## 3. Change Point Detection

### 3.1 CUSUM Algorithm (Cumulative Sum)

**Purpose**: Detect significant change points in a time series.

**Principle**: Accumulate deviations from the mean; when the cumulative sum exceeds a threshold, a change point is detected.

```javascript
function detectChangePointsCUSUM(timeSeries, threshold = 5) {
  const values = timeSeries.map(d => d.value);
  const n = values.length;

  // Calculate global mean
  const mean = values.reduce((a, b) => a + b, 0) / n;

  // Calculate CUSUM
  const cusum = [0];
  let s = 0;

  for (let i = 0; i < n; i++) {
    s += values[i] - mean;
    cusum.push(s);
  }

  // Detect change points: CUSUM changes from positive to negative or vice versa
  const changePoints = [];

  for (let i = 1; i < cusum.length - 1; i++) {
    const prev = cusum[i - 1];
    const curr = cusum[i];
    const next = cusum[i + 1];

    // Sign change or exceeds threshold
    if ((prev > 0 && curr < 0) || (prev < 0 && curr > 0) || Math.abs(curr) > threshold) {
      // Calculate mean difference before and after the change
      const before = values.slice(Math.max(0, i - 5), i);
      const after = values.slice(i, Math.min(n, i + 5));
      const meanBefore = before.reduce((a, b) => a + b, 0) / before.length;
      const meanAfter = after.reduce((a, b) => a + b, 0) / after.length;
      const change = meanAfter - meanBefore;

      changePoints.push({
        index: i,
        date: timeSeries[i].date,
        change: change,
        type: change > 0 ? 'increase' : change < 0 ? 'decrease' : 'no_change',
        magnitude: Math.abs(change)
      });
    }
  }

  return changePoints;
}
```

### 3.2 Sliding Window t-Test

**Purpose**: Detect whether the means of two adjacent time periods are significantly different.

```javascript
function detectChangePointsTTest(timeSeries, windowSize = 7) {
  const values = timeSeries.map(d => d.value);
  const n = values.length;
  const changePoints = [];

  for (let i = windowSize; i < n - windowSize; i++) {
    // Before and after windows
    const before = values.slice(i - windowSize, i);
    const after = values.slice(i, i + windowSize);

    // Calculate means and standard deviations
    const meanBefore = before.reduce((a, b) => a + b, 0) / windowSize;
    const meanAfter = after.reduce((a, b) => a + b, 0) / windowSize;

    const varBefore = before.reduce((a, b) => a + Math.pow(b - meanBefore, 2), 0) / (windowSize - 1);
    const varAfter = after.reduce((a, b) => a + Math.pow(b - meanAfter, 2), 0) / (windowSize - 1);

    // t-test
    const pooledStdDev = Math.sqrt(varBefore + varAfter);
    const tStat = (meanAfter - meanBefore) / (pooledStdDev * Math.sqrt(2 / windowSize));

    // Degrees of freedom
    const df = 2 * windowSize - 2;

    // Critical value (α=0.05, two-tailed test)
    const criticalValue = df > 30 ? 1.96 : 2.0; // Simplified

    if (Math.abs(tStat) > criticalValue) {
      changePoints.push({
        index: i,
        date: timeSeries[i].date,
        tStatistic: tStat,
        pValue: 2 * (1 - normalCDF(Math.abs(tStat))),
        change: meanAfter - meanBefore,
        type: meanAfter > meanBefore ? 'increase' : 'decrease'
      });
    }
  }

  return changePoints;
}
```

---

## 4. Outlier Detection

### 4.1 Percentile Method

**Purpose**: Identify extreme values that fall outside the normal range.

```javascript
function detectOutliersPercentile(timeSeries, lower = 5, upper = 95) {
  const values = timeSeries.map(d => d.value);
  const n = values.length;

  // Calculate percentiles
  const sorted = [...values].sort((a, b) => a - b);
  const lowerPercentile = sorted[Math.floor(n * lower / 100)];
  const upperPercentile = sorted[Math.floor(n * upper / 100)];

  // Detect outliers
  const outliers = timeSeries.filter((d, i) => {
    const value = d.value;
    return value < lowerPercentile || value > upperPercentile;
  });

  return {
    lowerBound: lowerPercentile,
    upperBound: upperPercentile,
    outliers: outliers.map(o => ({
      date: o.date,
      value: o.value,
      type: o.value < lowerPercentile ? 'low' : 'high'
    })),
    outlierCount: outliers.length,
    outlierRate: outliers.length / n
  };
}
```

### 4.2 IQR Method (Interquartile Range)

**Purpose**: Detect outliers using the box plot rule.

```javascript
function detectOutliersIQR(timeSeries, multiplier = 1.5) {
  const values = timeSeries.map(d => d.value);
  const n = values.length;

  // Calculate quartiles
  const sorted = [...values].sort((a, b) => a - b);
  const q1 = sorted[Math.floor(n * 0.25)];
  const q2 = sorted[Math.floor(n * 0.5)]; // Median
  const q3 = sorted[Math.floor(n * 0.75)];

  const iqr = q3 - q1;
  const lowerFence = q1 - multiplier * iqr;
  const upperFence = q3 + multiplier * iqr;

  // Detect outliers
  const outliers = timeSeries.filter(d => {
    return d.value < lowerFence || d.value > upperFence;
  });

  return {
    q1: q1,
    q2: q2,
    q3: q3,
    iqr: iqr,
    lowerFence: lowerFence,
    upperFence: upperFence,
    outliers: outliers.map(o => ({
      date: o.date,
      value: o.value,
      type: o.value < lowerFence ? 'low' : 'high',
      severity: o.value < lowerFence - 2 * iqr || o.value > upperFence + 2 * iqr ? 'extreme' : 'mild'
    }))
  };
}
```

---

## 5. Statistical Metric Calculations

### 5.1 Descriptive Statistics

```javascript
function descriptiveStats(timeSeries) {
  const values = timeSeries.map(d => d.value);
  const n = values.length;

  // Central tendency
  const mean = values.reduce((a, b) => a + b, 0) / n;
  const sorted = [...values].sort((a, b) => a - b);
  const median = sorted[Math.floor(n / 2)];

  // Dispersion
  const variance = values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / (n - 1);
  const stdDev = Math.sqrt(variance);
  const range = sorted[n - 1] - sorted[0];

  // Percentiles
  const percentiles = {
    p25: sorted[Math.floor(n * 0.25)],
    p50: median,
    p75: sorted[Math.floor(n * 0.75)]
  };

  // Coefficient of variation (CV = σ/μ, used for comparing data of different scales)
  const cv = mean !== 0 ? (stdDev / mean) * 100 : 0;

  return {
    count: n,
    mean: mean,
    median: median,
    mode: calculateMode(sorted),
    stdDev: stdDev,
    variance: variance,
    range: range,
    min: sorted[0],
    max: sorted[n - 1],
    percentiles: percentiles,
    iqr: percentiles.p75 - percentiles.p25,
    cv: cv
  };
}

function calculateMode(sortedArray) {
  const frequency = {};
  sortedArray.forEach(val => {
    frequency[val] = (frequency[val] || 0) + 1;
  });

  let maxFreq = 0;
  let mode = null;
  for (const val in frequency) {
    if (frequency[val] > maxFreq) {
      maxFreq = frequency[val];
      mode = Number(val);
    }
  }
  return mode;
}
```

### 5.2 Rate of Change Calculation

```javascript
function calculateChangeRate(timeSeries) {
  const values = timeSeries.map(d => d.value);
  const n = values.length;

  if (n < 2) {
    return null;
  }

  // Simple rate of change (first to last)
  const simpleRate = ((values[n - 1] - values[0]) / values[0]) * 100;

  // Average daily rate of change
  const dailyRates = [];
  for (let i = 1; i < n; i++) {
    const rate = ((values[i] - values[i - 1]) / values[i - 1]) * 100;
    dailyRates.push(rate);
  }

  const avgDailyRate = dailyRates.reduce((a, b) => a + b, 0) / dailyRates.length;
  const stdDailyRate = Math.sqrt(
    dailyRates.reduce((a, b) => a + Math.pow(b - avgDailyRate, 2), 0) / (dailyRates.length - 1)
  );

  return {
    simpleRate: simpleRate,          // Total rate of change (%)
    avgDailyRate: avgDailyRate,     // Average daily rate of change (%)
    stdDailyRate: stdDailyRate,     // Standard deviation of daily rate
    volatility: stdDailyRate,        // Volatility
    maxGain: Math.max(...dailyRates),   // Maximum daily gain (%)
    maxLoss: Math.min(...dailyRates)    // Maximum daily loss (%)
  };
}
```

---

## 6. Predictive Insight Generation

### 6.1 Risk Assessment

```javascript
function assessRisks(trends, thresholds) {
  const risks = [];

  // Weight risk assessment
  if (trends.weight) {
    const bmi = trends.weight.currentBMI;
    if (bmi < 18.5) {
      risks.push({
        type: 'underweight',
        severity: 'moderate',
        factor: 'Low BMI',
        value: bmi,
        message: 'Low BMI may impact immune function'
      });
    } else if (bmi > 28) {
      risks.push({
        type: 'overweight',
        severity: bmi > 30 ? 'high' : 'moderate',
        factor: 'High BMI',
        value: bmi,
        message: 'High BMI increases risk of chronic disease'
      });
    }

    // Rapid weight change
    if (Math.abs(trends.weight.percentChange) > 10) {
      risks.push({
        type: 'rapid_weight_change',
        severity: 'high',
        factor: 'Rapid weight change',
        value: trends.weight.percentChange,
        message: `${Math.abs(trends.weight.percentChange).toFixed(1)}% weight change requires attention`
      });
    }
  }

  // Symptom risk assessment
  if (trends.symptoms) {
    const { mostFrequent, frequency } = trends.symptoms;
    const avgMonthly = frequency / 3; // Assuming 3 months of data

    if (avgMonthly > 10) {
      risks.push({
        type: 'frequent_symptoms',
        severity: 'high',
        factor: 'Frequent symptoms',
        symptom: mostFrequent,
        value: avgMonthly,
        message: `${mostFrequent} occurring ${Math.round(avgMonthly)} times per month, recommend medical consultation`
      });
    }
  }

  // Medication adherence risk
  if (trends.medications) {
    if (trends.medications.adherence < 70) {
      risks.push({
        type: 'poor_adherence',
        severity: 'moderate',
        factor: 'Low medication adherence',
        value: trends.medications.adherence,
        message: 'Low adherence may reduce treatment effectiveness'
      });
    }
  }

  return risks;
}
```

### 6.2 Preventive Recommendation Generation

```javascript
function generateRecommendations(trends, correlations) {
  const recommendations = [];

  // Recommendations based on trends
  if (trends.weight && trends.weight.direction === 'decreasing') {
    recommendations.push({
      type: 'maintain',
      priority: 'low',
      message: 'Weight management is on track, continue current approach'
    });
  }

  if (trends.symptoms && trends.symptoms.trend === 'decreasing') {
    recommendations.push({
      type: 'positive',
      priority: 'low',
      message: 'Symptom frequency declining, continue current care plan'
    });
  }

  // Recommendations based on correlations
  if (correlations.some(c => c.x === 'Sleep Duration' && c.y === 'Mood Score' && c.coefficient > 0.7)) {
    recommendations.push({
      type: 'improvement',
      priority: 'high',
      message: 'Increasing sleep duration to 7-8 hours can improve mood'
    });
  }

  if (correlations.some(c => c.x === 'Medication Adherence' && c.y === 'Symptom Frequency' && c.coefficient < -0.6)) {
    recommendations.push({
      type: 'improvement',
      priority: 'high',
      message: 'Improving medication adherence can reduce symptom occurrences'
    });
  }

  // Recommendations based on risks
  trends.risks.forEach(risk => {
    if (risk.type === 'poor_adherence') {
      recommendations.push({
        type: 'action',
        priority: 'high',
        message: 'Set medication reminders to improve adherence to above 90%'
      });
    }
  });

  return recommendations.sort((a, b) => {
    const priorityOrder = { 'high': 0, 'moderate': 1, 'low': 2 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });
}
```

### 6.3 Early Warnings

```javascript
function generateEarlyWarnings(trends) {
  const warnings = [];

  // Rapid weight loss
  if (trends.weight && trends.weight.percentChange < -10) {
    warnings.push({
      type: 'weight_loss',
      urgency: 'high',
      message: 'Rapid weight loss (>-10%), recommend consulting a doctor',
      indicator: 'weight_percent_change',
      threshold: -10,
      currentValue: trends.weight.percentChange
    });
  }

  // Rising symptom frequency
  if (trends.symptoms && trends.symptoms.frequencyTrend === 'increasing') {
    warnings.push({
      type: 'symptom_increase',
      urgency: 'moderate',
      message: 'Symptom frequency increasing, recommend monitoring and recording triggers',
      indicator: 'symptom_frequency'
    });
  }

  // Worsening blood pressure / lab indicators
  if (trends.labResults) {
    trends.labResults.forEach(indicator => {
      if (indicator.trend === 'worsening' && indicator.severity === 'abnormal') {
        warnings.push({
          type: 'lab_worsening',
          urgency: 'high',
          message: `${indicator.name} indicator worsening and abnormal, recommend medical consultation`,
          indicator: indicator.name,
          currentValue: indicator.value,
          referenceRange: indicator.reference_range
        });
      }
    });
  }

  return warnings;
}
```

---

## 7. Chart Data Preparation

### 7.1 Line Chart Data

```javascript
function prepareLineChartData(timeSeries, yAxisTitle) {
  return {
    xAxis: {
      type: 'category',
      data: timeSeries.map(d => d.date),
      name: 'Date'
    },
    yAxis: {
      type: 'value',
      name: yAxisTitle
    },
    series: [{
      name: yAxisTitle,
      type: 'line',
      data: timeSeries.map(d => d.value),
      smooth: true,
      markLine: {
        data: [{ type: 'average', name: 'Average' }]
      }
    }]
  };
}
```

### 7.2 Heatmap Data

```javascript
function prepareHeatmapData(correlations, xLabels, yLabels) {
  // Convert correlation matrix to ECharts heatmap format
  const data = [];

  correlations.forEach((row, i) => {
    row.forEach((value, j) => {
      data.push([j, i, value]); // [x, y, value]
    });
  });

  return {
    tooltip: {
      position: 'top',
      formatter: (params) => {
        return `${xLabels[params.data[0]]} vs ${yLabels[params.data[1]]}<br/>Correlation Coefficient: ${params.data[2].toFixed(2)}`;
      }
    },
    grid: {
      height: '50%',
      top: '10%'
    },
    xAxis: {
      type: 'category',
      data: xLabels,
      splitArea: { show: true },
      splitLine: { show: false }
    },
    yAxis: {
      type: 'category',
      data: yLabels,
      splitArea: { show: true },
      splitLine: { show: false }
    },
    visualMap: {
      min: -1,
      max: 1,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '15%',
      inRange: {
        color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffcc', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
      },
      textStyle: { color: '#333' }
    },
    series: [{
      name: 'Correlation',
      type: 'heatmap',
      data: data,
      label: {
        show: true,
        formatter: (params) => params.data[2].toFixed(2)
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  };
}
```

---

## Algorithm Selection Guide

### Choose Algorithm by Data Type

| Data Type | Recommended Algorithm | Output |
|---------|---------|------|
| Weight/BMI trend | Linear regression | Slope, R², direction |
| Symptom frequency | Descriptive statistics | Frequency count, percentage |
| Medication adherence | Percentage calculation | Adherence rate % |
| Continuous variable correlation | Pearson correlation | Correlation coefficient |
| Ordinal variable correlation | Spearman correlation | Correlation coefficient |
| Time series patterns | Time series decomposition | Trend + Seasonal + Residual |
| Change detection | CUSUM or t-test | Change point list |
| Extreme value detection | IQR method | Outlier list |

### Choose Algorithm by Data Volume

| Data Volume | Recommended Algorithm | Notes |
|--------|---------|---------|
| < 5 points | Descriptive statistics | Cannot perform trend analysis |
| 5-20 points | Linear regression, moving average | Limited trend reliability |
| 20-60 points | Linear regression, correlation analysis | Preliminary analysis possible |
| > 60 points | All algorithms | Analysis results reliable |

---

## Performance Optimization

### Data Reading Optimization
```javascript
// Only read the necessary files
function readDataForPeriod(startDate, endDate) {
  const pattern = `data/symptoms/${startDate.year}-${startDate.month.toString().padStart(2, '0')}/*.json`;
  const files = glob(pattern);

  // Only read matching files
  return files.map(file => JSON.parse(readFile(file)));
}
```

### Incremental Calculation
```javascript
// Cache intermediate results
const cache = new Map();

function calculateWithCache(key, compute) {
  if (cache.has(key)) {
    return cache.get(key);
  }

  const result = compute();
  cache.set(key, result);
  return result;
}
```

---

## Algorithm Validation

### Validation Methods
- **Cross-validation**: Split data into training and test sets to verify algorithm stability
- **Visual inspection**: Plot data charts and manually verify trend detection accuracy
- **Sensitivity analysis**: Adjust parameters (e.g., window size) and evaluate result stability

### Accuracy Standards
- **Trend detection**: R² > 0.5 indicates a reliable trend
- **Correlation analysis**: p < 0.05 is statistically significant
- **Change point detection**: Requires at least 2 consecutive data points for support
