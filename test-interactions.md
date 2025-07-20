# Testing Supplement Interaction Warnings

## Test Scenarios

### Scenario 1: Levothyroxine + Fiber Supplement
**Expected**: High severity warning with 4-hour separation requirement

**Steps**:
1. Add Levothyroxine as medication
2. Add Fiber Supplement (Psyllium, Inulina, Salvado de avena)
3. Verify warning appears with:
   - Separation time: 4 hours
   - Severity: High (red badge)
   - Clear recommendation

### Scenario 2: Levothyroxine + Magnesium
**Expected**: High severity warning with 4-hour separation requirement

**Steps**:
1. Add Levothyroxine as medication
2. Add Magnesium supplement
3. Verify warning appears

### Scenario 3: Metformin + Vitamin B12
**Expected**: Moderate severity warning about B12 monitoring

**Steps**:
1. Add Metformin as medication
2. Add Vitamin B12 (if available)
3. Verify monitoring recommendation appears

### Scenario 4: Collagen + Vitamin C Synergy
**Expected**: Positive synergy notification

**Steps**:
1. Add Collagen Hydrolyzed
2. Add Vitamin C
3. Verify synergy benefit appears

### Scenario 5: High Dose Warning
**Expected**: Dose warning when exceeding limits

**Steps**:
1. Add Vitamin C with custom dose > 2000mg
2. Verify dose warning appears
3. Check for side effect mention (diarrhea)

## Deployment Commands

```bash
cd /opt/apps/mealplan
git pull origin main
docker-compose down
docker-compose build --no-cache
docker-compose up -d
docker-compose logs -f
```

## Verification Checklist

- [ ] Interaction warnings display correctly
- [ ] Severity badges show appropriate colors
- [ ] Separation times are accurate
- [ ] Synergies display in green
- [ ] Dose warnings show when limits exceeded
- [ ] General information panel appears
- [ ] Warnings update dynamically when selections change