
# Pilot Calculation Algorithms – Specification Sheet

This document consolidates **12 core aviation calculators** with precise *inputs → outputs*, step‑by‑step formulas, and edge‑case notes.  
Feed any section directly into an LLM to generate production‑ready code for a web or mobile app.

---

## 1. True Airspeed (TAS)

```text
Inputs
    IAS : knots  (Indicated Airspeed)
    PA  : ft     (Pressure Altitude)
    OAT : °C     (Outside‑Air Temperature)

Steps
    1. σ = (1 – 6.875 × 10⁻⁶ · PA) ^ 5.2559
    2. TK  = OAT + 273.15
       T_ISA = 288.15 – 0.0019812 · PA
       δ = TK / T_ISA
    3. TAS = IAS / √σ · √δ
       (For IAS > ≈250 kt apply CAS → EAS → TAS chain)

Outputs
    TAS : knots

Edge cases
    • Negative OAT allowed.
    • Above 10 000 ft & IAS>200 kt, include compressibility.
```

---

## 2. Ground Speed (GS) & Track

```text
Inputs
    TAS, WindDir (°T), WindSpd (kts), Course (°T)

Steps
    Resolve vectors, sum, then:
        GS    = √(Gx² + Gy²)
        Track = atan2(Gx, Gy) °T

Outputs
    GS, Track

Edge cases
    • Normalize angles to [0,360).
```

---

## 3. Wind Correction Angle (WCA) & Corrected Heading

```text
Inputs
    Same as #2

Steps
    β   = WindDir – Course
    WCA = asin((WindSpd / TAS) · sin β)
    Heading = Course + WCA

Outputs
    WCA (±°), Heading (°T)

Edge cases
    • If |WindSpd / TAS × sin β| > 1 → flag “untrackable”.
```

---

## 4. Pressure Altitude (PA)

```text
Inputs
    Elevation (ft), QNH (hPa)

Steps
    PA = Elevation + 27 × (1013.25 – QNH)

Outputs
    PA

Edge cases
    • Prompt when QNH outside 850–1080 hPa.
```

---

## 5. Density Altitude (DA)

```text
Inputs
    PA (ft), OAT (°C)

Steps
    σ = (1 – 6.875e‑6 · PA)^5.2559
    ISA_T = 15 – PA/1000 × 2
    DA = PA + 120 × (OAT – ISA_T)

Outputs
    DA

Edge cases
    • Warn when DA exceeds service ceiling.
```

---

## 6. Crosswind & Head/Tailwind Components

```text
Inputs
    WindDir, WindSpd, RunwayHDG

Steps
    θ       = WindDir – RunwayHDG
    Cross   = WindSpd × sin θ
    Head    = WindSpd × cos θ

Outputs
    Crosswind (±), Head/Tailwind (±)

Edge cases
    • Round Crosswind up to next knot for limits.
```

---

## 7. Time‑Distance‑Speed Calculator

```text
Inputs
    Any two of Distance (NM), Speed (kts), Time (min)

Steps
    • Distance & Speed ➜ Time = 60·D / S
    • Distance & Time  ➜ Speed = 60·D / T
    • Speed & Time     ➜ Distance = S·T / 60

Edge cases
    • Reject zero/negative inputs.
```

---

## 8. Fuel Burn, Endurance & Reserve

```text
Inputs
    FuelFlow (L/h or GPH)
    FuelOnBoard
    TaxiFuel
    ReservePolicy (minutes or %)

Steps
    Usable      = FuelOnBoard – TaxiFuel
    Endurance   = Usable / FuelFlow
    ReserveFuel = (minutes) FuelFlow·(Res/60)  OR  (%) Usable·(Res/100)
    MaxLegTime  = Endurance – ReserveFuel / FuelFlow

Outputs
    Endurance (hr), ReserveFuel, MaxLegTime (hr)

Edge cases
    • Negative Usable ➜ “Insufficient fuel”.
```

---

## 9. Weight‑and‑Balance (CG)

```text
Inputs
    Array {item, weight_lb, arm_in}
    AircraftEmpty {weight, arm}
    CG_limits {forward_in, aft_in}

Steps
    Append empty weight.
    Sum weights & moments.
    CG = ΣMoment / ΣWeight
    WithinLimits = CG ∈ [fwd, aft]

Outputs
    TakeoffWeight, CG, WithinLimits

Edge cases
    • Flag when ΣWeight > MTOW.
    • Metric support via unit conversion.
```

---

## 10. Top‑of‑Descent (TOD)

```text
Inputs
    CruiseAlt, TargetAlt (ft)
    GS (kts), DescentRate (ft/min)
    ExtraMiles (NM)

Steps
    ΔAlt    = CruiseAlt – TargetAlt
    TimeMin = ΔAlt / DescentRate
    Distance = GS · TimeMin / 60
    TOD = Distance + ExtraMiles

Edge cases
    • ΔAlt ≤ 0 ➜ TOD = 0.
```

---

## 11. Glide Distance & Glide Ratio

```text
Inputs
    Option A: GlideRatio
    Option B: SinkRate & Airspeed
    AltitudeAGL (ft), WindComp (kts)

Steps
    A. Distance = AltitudeAGL/1000 × GlideRatio / 6076 NM
    B. GlideRatio = (Airspeed·101.27)/SinkRate
       then Distance as above.
    Wind‑adjusted = Distance × (TAS + WindComp)/TAS

Outputs
    DistanceAdj (NM), GlideRatio

Edge cases
    • SinkRate ≤ 0 ➜ invalid.
```

---

## 12. Mach Number & Equivalent Airspeed (EAS)

```text
Inputs
    TAS (kts), Altitude (ft), OAT (°C)

Steps
    Temp_K = OAT + 273.15
    a  = 38.967854·√Temp_K  (m/s) ➜ knots
    Mach = TAS / a
    EAS  ≈ TAS × √σ  (σ from §1)

Outputs
    Mach, EAS

Edge cases
    • Validate TAS < 0.95 a (subsonic).
```

---

## Implementation Notes

| Aspect | Recommendation |
|--------|----------------|
| **Units** | Build a lightweight conversion utility; store SI internally. |
| **Errors** | Throw descriptive domain errors (e.g., “Negative altitude”). |
| **Testing** | Fixture values from POH or E6‑B tables. |
| **Frontend** | Wrap each calc in memoized React hooks; display via cards/forms. |

---

## Prompt Template for Code Generation

> **System/Pre‑prompt**  
> “You are a senior front‑end/full‑stack developer. Generate modular, type‑safe JavaScript functions plus unit tests for the following specs.”  
>
> **✂️ Paste selected calculator spec(s) here ✂️**  
>
> **Optional Post‑prompt**  
> “Wrap each function in a React hook, export from `/lib/aviation.ts`, and write Jest tests. Use SI units internally; expose both metric and imperial helpers.”

Copy any block above into your LLM workflow to bootstrap accurate, pilot‑ready code.

---
