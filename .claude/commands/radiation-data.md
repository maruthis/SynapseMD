# Radiation Dose Reference Data

## Reference Radiation Dose Values for Common Medical Examinations

### CT Scans (Unit: mSv)
- **Head CT**: 2 mSv
- **Chest CT**: 7 mSv
- **Abdominal CT**: 8 mSv
- **Pelvic CT**: 6 mSv
- **Spinal CT**: 6 mSv
- **Limb CT**: 0.1 mSv

### X-Ray Examinations (Unit: mSv)
- **Chest X-ray**: 0.1 mSv
- **Abdominal X-ray**: 0.7 mSv
- **Limb X-ray**: 0.01 mSv
- **Dental X-ray**: 0.005 mSv

### Other Examinations
- **PET-CT**: 14 mSv
- **Bone Scan**: 6 mSv
- **Angiography**: 5-15 mSv
- **Mammography**: 0.4 mSv

## Radiation Dissipation Patterns

The ionizing radiation produced by medical imaging examinations is metabolized primarily through the following means:

1. **Natural decay**: Contrast agents such as iodine and barium are reduced through natural decay
2. **Human metabolism**: Eliminated through organs such as the kidneys and liver
3. **Physical half-life**: Different radionuclides have different half-lives

### Simplified Calculation Model (Used in This System)

**Half-life model**:
- The radiation effects of most medical examinations essentially dissipate within **1 year**
- Uses an **exponential decay model**: Current dose = Initial dose × (0.5)^(days/365)
- **Annual dissipation rate**: approximately 50% per year

### Radiation Safety Thresholds

- **Average annual natural background radiation**: 2.4 mSv/year
- **Public annual dose limit**: 1 mSv (excluding natural background)
- **Occupational annual dose limit**: 20 mSv/year
- **Medical examination recommendation**: Annual cumulative dose < 10 mSv is considered safe

## Body Surface Area Calculation

Using the Mosteller formula:
```
Body Surface Area (m²) = √(Height(cm) × Weight(kg) / 3600)
```

### Dose Adjustment Factors

Adjusting radiation dose based on body surface area:
- **Standard body surface area**: 1.73 m² (adults)
- **Adjustment factor**: Actual body surface area / 1.73
- **Adjusted dose**: Standard dose × adjustment factor

## Radiation Impact Assessment Criteria

### Low Dose (< 1 mSv)
- Extremely low risk, no special handling required

### Moderate Dose (1-10 mSv)
- Needs to be recorded
- Annual summary recommended

### High Dose (10-50 mSv)
- Requires attention
- Interval examinations recommended
- Record cumulative dose

### Very High Dose (> 50 mSv)
- Requires physician evaluation
- Strict recording required
- Consider alternative examination options
